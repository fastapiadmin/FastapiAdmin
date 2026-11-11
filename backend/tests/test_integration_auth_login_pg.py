"""真实 PostgreSQL + Redis 账号密码登录集成。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

import pytest
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from starlette.requests import Request

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.security import CustomOAuth2PasswordRequestForm
from app.modules.system.auth.service import LoginService
from app.modules.system.user.model import UserModel
from app.utils.password_util import PwdUtil

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL/Redis：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            yield session
    finally:
        await engine.dispose()


def _req() -> Request:
    return Request({"type": "http", "method": "POST", "path": "/", "headers": [(b"user-agent", b"pytest")], "client": ("127.0.0.1", 1)})


def _form(username: str, password: str) -> CustomOAuth2PasswordRequestForm:
    return CustomOAuth2PasswordRequestForm(grant_type="password", scope="", client_id=None, client_secret=None, username=username, password=password, captcha_key="", captcha="", login_type="PC端")


async def _user(password: str = "Abc123!x", status: int = 0) -> tuple[str, int]:
    username = f"it_login_{uuid.uuid4().hex[:10]}"
    hashed = await PwdUtil.ahash_password(password=password)
    async with _db() as db:
        user = UserModel(username=username, password=hashed, name="IT", status=status)
        db.add(user); await db.commit(); await db.refresh(user)
        return username, user.id


async def _cleanup(username: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_user WHERE username=:u"), {"u": username})
        await db.commit()


def _patch_side_effects(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.auth.service as mod
    async def noop(*a, **k): return None
    async def loc(redis, ip): return "test"
    monkeypatch.setattr(mod.LoginService, "_check_login_rate_limit", staticmethod(noop))
    monkeypatch.setattr(mod.IpLocalUtil, "resolve_location", staticmethod(loc))
    monkeypatch.setattr(mod, "_write_login_log", noop)


async def test_login_missing_user(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_side_effects(monkeypatch)
    async with _db() as db, Redis(host="localhost", port=6379, db=1, decode_responses=True) as r:
        with pytest.raises(CustomException, match="用户不存在"):
            await LoginService.authenticate_user(_req(), r, _form("no_such_user_x", "Abc123!x"), db)


async def test_login_wrong_password(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_side_effects(monkeypatch)
    username, _ = await _user()
    try:
        async with _db() as db, Redis(host="localhost", port=6379, db=1, decode_responses=True) as r:
            with pytest.raises(CustomException, match="账号或密码错误"):
                await LoginService.authenticate_user(_req(), r, _form(username, "Wrong123!"), db)
    finally:
        await _cleanup(username)


async def test_login_disabled(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_side_effects(monkeypatch)
    username, _ = await _user(status=1)
    try:
        async with _db() as db, Redis(host="localhost", port=6379, db=1, decode_responses=True) as r:
            with pytest.raises(CustomException, match="停用"):
                await LoginService.authenticate_user(_req(), r, _form(username, "Abc123!x"), db)
    finally:
        await _cleanup(username)


async def test_login_success(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_side_effects(monkeypatch)
    username, uid = await _user()
    try:
        async with _db() as db, Redis(host="localhost", port=6379, db=1, decode_responses=True) as r:
            out = await LoginService.authenticate_user(_req(), r, _form(username, "Abc123!x"), db)
            assert out.access_token and out.user_info["id"] == uid
            from app.core.dependencies import _authenticate
            auth = await _authenticate(out.access_token, db, r)
            assert auth.user.id == uid
            from app.core.security import decode_access_token
            sid = decode_access_token(out.access_token).sub
            from app.core.exceptions import CustomException
            from app.core.dependencies import _authenticate
            from app.common.enums import RedisInitKeyConfig
            await r.delete(f"{RedisInitKeyConfig.USER_SESSION.key}:{sid}")
            with pytest.raises(CustomException):
                await _authenticate(out.access_token, db, r)
            from app.common.enums import RedisInitKeyConfig
            await r.delete(
                f"{RedisInitKeyConfig.USER_SESSION.key}:{sid}",
                f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{sid}",
                f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{sid}",
            )
    finally:
        await _cleanup(username)


async def test_refresh_disabled_user(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_side_effects(monkeypatch)
    username, uid = await _user()
    r = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    try:
        async with _db() as db:
            out = await LoginService.authenticate_user(_req(), r, _form(username, "Abc123!x"), db)
            await db.execute(text("UPDATE sys_user SET status=1 WHERE id=:i"), {"i": uid})
            await db.commit()
            with pytest.raises(CustomException, match="停用"):
                await LoginService.refresh_token(db, r, out.refresh_token)
    finally:
        await _cleanup(username); await r.aclose()


async def test_refresh_invalid_tokens(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_side_effects(monkeypatch)
    username, _ = await _user()
    r = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    try:
        async with _db() as db:
            out = await LoginService.authenticate_user(_req(), r, _form(username, "Abc123!x"), db)
            with pytest.raises(CustomException):
                await LoginService.refresh_token(db, r, out.access_token)
            from app.core.security import decode_access_token
            from app.common.enums import RedisInitKeyConfig
            sid = decode_access_token(out.refresh_token).sub
            await r.delete(f"{RedisInitKeyConfig.USER_SESSION.key}:{sid}")
            with pytest.raises(CustomException):
                await LoginService.refresh_token(db, r, out.refresh_token)
    finally:
        await _cleanup(username); await r.aclose()
