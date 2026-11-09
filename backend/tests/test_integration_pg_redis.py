"""真实 PostgreSQL / Redis 集成测试（范围 A：排除协议不受影响）。

运行方式：
    TEST_DB_TYPE=postgres TEST_DB_USER=... TEST_DB_PASSWORD=... \
    TEST_DB_NAME=fastapiadmin_test uv run pytest tests/test_integration_pg_redis.py
"""

from __future__ import annotations

import os
import uuid

import pytest
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.modules.system.user.model import UserModel

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL/Redis：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    """每个测试独立引擎 + NullPool，避免绑定到 TestClient 已关闭的事件循环。"""
    engine = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            yield session
    finally:
        await engine.dispose()


def _username() -> str:
    return f"it_{uuid.uuid4().hex[:12]}"


async def _delete_user(user_id: int) -> None:
    async with _db() as db:
        obj = await db.get(UserModel, user_id)
        if obj is not None:
            await db.delete(obj)
            await db.commit()


async def test_postgres_select_one(test_client) -> None:
    async with _db() as db:
        assert (await db.execute(text("SELECT 1"))).scalar_one() == 1


async def test_postgres_user_roundtrip(test_client) -> None:
    username = _username()
    async with _db() as db:
        user = UserModel(username=username, password="hash", name="IT", status=0)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        user_id = user.id
    try:
        async with _db() as db:
            loaded = await db.get(UserModel, user_id)
            assert loaded is not None and loaded.username == username
    finally:
        await _delete_user(user_id)
    async with _db() as db:
        assert await db.get(UserModel, user_id) is None


async def test_postgres_unique_violation_rolls_back(test_client) -> None:
    username = _username()
    async with _db() as db:
        db.add(UserModel(username=username, password="hash", name="IT", status=0))
        await db.commit()
        first = (await db.execute(text("SELECT id FROM sys_user WHERE username=:u"), {"u": username})).scalar_one()
    try:
        with pytest.raises(IntegrityError):
            async with _db() as db:
                db.add(UserModel(username=username, password="hash", name="IT2", status=0))
                await db.commit()
    finally:
        await _delete_user(first)


async def test_redis_real_roundtrip() -> None:
    from redis.asyncio import Redis

    client = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    key = f"it:{uuid.uuid4().hex}"
    try:
        assert await client.set(key, "1", ex=30)
        assert await client.get(key) == "1"
        assert await client.delete(key) == 1
        assert await client.get(key) is None
    finally:
        await client.aclose()


async def test_crud_real_roundtrip_and_explicit_null(test_client) -> None:
    from types import SimpleNamespace
    from app.core.base_crud import CRUDBase
    from app.modules.system.user.model import UserModel
    from app.modules.system.user.schema import UserUpdateSchema

    username = _username()
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            crud = CRUDBase(UserModel, auth, db)
            user = await crud.create({"username": username, "password": "hash", "name": "IT", "status": 0, "description": "x"})
            uid = user.id
            assert (await crud.get(username=username)).id == uid
            await crud.update(uid, UserUpdateSchema(description=None))
            assert (await crud.get(id=uid)).description is None
            page = await crud.page(1, 10, {"username": username}, None)
            assert page.total == 1
            await crud.delete(ids=[uid])
            assert await crud.get(id=uid) is None
    finally:
        async with _db() as db:
            await db.execute(text("DELETE FROM sys_user WHERE username=:u"), {"u": username})
            await db.commit()


async def test_redis_real_expiry() -> None:
    from redis.asyncio import Redis

    client = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    key = f"it:ttl:{uuid.uuid4().hex}"
    try:
        assert await client.set(key, "1", ex=30)
        assert 0 < await client.ttl(key) <= 30
        assert await client.delete(key) == 1
    finally:
        await client.aclose()
