"""真实 PostgreSQL + Redis 认证会话集成：登录令牌、刷新轮换、退出。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

import pytest
from redis.asyncio import Redis
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload
from sqlalchemy.pool import NullPool
from starlette.requests import Request

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.common.enums import RedisInitKeyConfig
from app.modules.system.auth.service import LoginService
from app.modules.system.user.model import UserModel

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


def _request() -> Request:
    return Request({"type": "http", "method": "POST", "path": "/", "headers": [(b"user-agent", b"pytest")], "client": ("127.0.0.1", 1)})


def _username() -> str:
    return f"it_auth_{uuid.uuid4().hex[:10]}"


@asynccontextmanager
async def _user_and_redis() -> AsyncIterator[tuple[UserModel, Redis, int]]:
    username = _username()
    client = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    async with _db() as db:
        user = UserModel(username=username, password="hash", name="IT", status=0)
        db.add(user); await db.commit(); await db.refresh(user)
        uid = user.id
    try:
        async with _db() as db:
            loaded = (await db.execute(
                select(UserModel).options(selectinload(UserModel.roles), selectinload(UserModel.positions)).where(UserModel.id == uid)
            )).scalar_one()
            yield loaded, client, uid
    finally:
        await client.aclose()
        async with _db() as db:
            await db.execute(text("DELETE FROM sys_user WHERE id=:i"), {"i": uid})
            await db.commit()


async def _keys(session_id: str) -> list[str]:
    return [
        f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}",
        f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}",
        f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}",
    ]


async def test_create_token_writes_session(test_client) -> None:
    async with _user_and_redis() as (user, redis, _uid):
        token = await LoginService.create_token(request=_request(), redis=redis, user=user, login_type="password", login_location="test")
        assert token.access_token and token.refresh_token
        from app.core.security import decode_access_token
        sid = decode_access_token(token=token.access_token).sub
        assert await redis.exists(*await _keys(sid)) == 3
        await redis.delete(*await _keys(sid))


async def test_refresh_rotates_and_replay_revokes(test_client) -> None:
    async with _user_and_redis() as (user, redis, _uid):
        token = await LoginService.create_token(request=_request(), redis=redis, user=user, login_type="password", login_location="test")
        from app.core.security import decode_access_token
        sid = decode_access_token(token=token.access_token).sub
        async with _db() as db:
            new = await LoginService.refresh_token(db=db, redis=redis, refresh_token=token.refresh_token)
        assert new.access_token != token.access_token and new.refresh_token != token.refresh_token
        async with _db() as db:
            with pytest.raises(CustomException, match="失效"):
                await LoginService.refresh_token(db=db, redis=redis, refresh_token=token.refresh_token)
        assert await redis.exists(*await _keys(sid)) == 0


async def test_refresh_rejects_access_token(test_client) -> None:
    async with _user_and_redis() as (user, redis, _uid):
        token = await LoginService.create_token(request=_request(), redis=redis, user=user, login_type="password", login_location="test")
        async with _db() as db:
            with pytest.raises(CustomException, match="刷新令牌"):
                await LoginService.refresh_token(db=db, redis=redis, refresh_token=token.access_token)
        from app.core.security import decode_access_token
        sid = decode_access_token(token=token.access_token).sub
        await redis.delete(*await _keys(sid))


async def test_logout_deletes_session(test_client) -> None:
    async with _user_and_redis() as (user, redis, _uid):
        token = await LoginService.create_token(request=_request(), redis=redis, user=user, login_type="password", login_location="test")
        from app.core.security import decode_access_token
        sid = decode_access_token(token=token.access_token).sub
        assert await LoginService.logout(redis, token.access_token) is True
        assert await redis.exists(*await _keys(sid)) == 0
