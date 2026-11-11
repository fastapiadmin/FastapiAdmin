"""用户服务守卫分支（真实 PG）。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.modules.system.user.service import UserService

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    f = async_sessionmaker(e, expire_on_commit=False)
    try:
        async with f() as s:
            yield s
    finally:
        await e.dispose()


def _auth(uid, superuser=True):
    return SimpleNamespace(user=SimpleNamespace(id=uid, is_superuser=superuser))


async def test_user_service_no_id_guards(test_client) -> None:
    async with _db() as db:
        svc = UserService(_auth(None), db)
        with pytest.raises(CustomException):
            await svc.current_info()
        with pytest.raises(CustomException):
            await svc.update_current_info(SimpleNamespace(mobile=None, email=None, name="x", avatar=None))


async def test_forget_password_normal_user(test_client) -> None:
    from app.modules.system.user.schema import UserForgetPasswordSchema
    name = f"it_fp_{uuid.uuid4().hex[:8]}"
    try:
        from app.modules.system.user.schema import UserCreateSchema
        async with _db() as db:
            await UserService(_auth(0), db).create(UserCreateSchema(username=name, password="Abc123!x", name="x"))
            await db.commit()
            svc = UserService(_auth(0), db)
            assert await svc.forget_password(UserForgetPasswordSchema(username=name)) is None
    finally:
        async with _db() as db:
            await db.execute(text("DELETE FROM sys_user WHERE username=:u"), {"u": name})
            await db.commit()
