"""真实 PostgreSQL 存储源服务 + 本地适配器集成。"""

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
from app.modules.task.storage.node.service import StorageNodeService

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
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


def _name() -> str:
    return f"it_node_{uuid.uuid4().hex[:10]}"


async def _cleanup(name: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM task_storage_node WHERE name=:n"), {"n": name})
        await db.commit()


def _data(tmp_path, name: str, is_default: bool = False):
    from app.modules.task.storage.node.schema import StorageNodeCreateSchema
    root = tmp_path / name; root.mkdir(exist_ok=True)
    return StorageNodeCreateSchema(name=name, protocol="local", host=str(root), port=0, is_default=is_default)


async def test_storage_node_roundtrip(test_client, tmp_path) -> None:
    name = _name(); auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = StorageNodeService(auth, db)
            node = await service.create(_data(tmp_path, name, True))
            assert node.name == name
            assert (await service.detail(node.id)).name == name
            assert (await service.test_connection(node.id)) is True
            assert any(item.name == name for item in await service.get_list())
            await service.delete([node.id])
            with pytest.raises(CustomException):
                await service.detail(node.id)
    finally:
        await _cleanup(name)


async def test_storage_node_duplicate(test_client, tmp_path) -> None:
    name = _name(); auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = StorageNodeService(auth, db)
            await service.create(_data(tmp_path, name))
            with pytest.raises(CustomException, match="已存在"):
                await service.create(_data(tmp_path, name))
    finally:
        await _cleanup(name); await _cleanup(name + "_b")


async def test_storage_node_default_switch(test_client, tmp_path) -> None:
    a = _name(); b = _name(); auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = StorageNodeService(auth, db)
            first = await service.create(_data(tmp_path, a, True))
            second = await service.create(_data(tmp_path, b, True))
            assert (await service.detail(first.id)).is_default is False
            assert (await service.detail(second.id)).is_default is True
    finally:
        await _cleanup(a); await _cleanup(b)
