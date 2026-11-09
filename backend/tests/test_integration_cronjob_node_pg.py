"""真实 PostgreSQL 调度节点定义 CRUD 集成。"""

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
from app.modules.task.cronjob.node.service import NodeService

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


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


async def _cleanup(name: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM task_cornjob_node WHERE name=:n"), {"n": name})
        await db.commit()


async def test_node_crud(test_client) -> None:
    from app.modules.task.cronjob.node.schema import NodeCreateSchema, NodeUpdateSchema
    name = _name()
    try:
        async with _db() as db:
            svc = NodeService(_auth(), db)
            node = await svc.create(NodeCreateSchema(name=name, func="builtin:server_status", trigger=None))
            assert node.name == name and node.code
            assert (await svc.detail(node.id)).name == name
            assert any(n.name == name for n in await svc.options())
            assert (await svc.page(1, 10, None)).total >= 1
            await svc.batch_set_status([node.id], 1)
            await svc.update(node.id, NodeUpdateSchema(name=name, func="builtin:server_status", trigger=None))
            await svc.delete([node.id])
    finally:
        await _cleanup(name)


async def test_node_clear(test_client) -> None:
    from app.modules.task.cronjob.node.schema import NodeCreateSchema
    name = _name()
    try:
        async with _db() as db:
            svc = NodeService(_auth(), db)
            await svc.create(NodeCreateSchema(name=name, func="builtin:server_status", trigger=None))
            await svc.clear()
            assert isinstance(await svc.get_list(), list)
    finally:
        await _cleanup(name)


async def test_node_execute_errors(test_client) -> None:
    from app.modules.task.cronjob.node.schema import NodeCreateSchema
    from app.core.exceptions import CustomException
    name = _name()
    try:
        async with _db() as db:
            svc = NodeService(_auth(), db)
            with pytest.raises(CustomException):
                await svc.execute(99999999)
            node = await svc.create(NodeCreateSchema(name=name, func="builtin:missing_handler", trigger=None))
            with pytest.raises(CustomException):
                await svc.execute(node.id)
            with pytest.raises(CustomException):
                await svc.update(99999999, NodeCreateSchema(name=name, func="builtin:missing_handler", trigger=None))
    finally:
        await _cleanup(name)
