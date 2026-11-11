"""真实 PostgreSQL 岗位服务集成。"""

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
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.modules.system.position.service import PositionService

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
    return f"it_pos_{uuid.uuid4().hex[:8]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


async def _cleanup(name: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_position WHERE name=:n"), {"n": name})
        await db.commit()


async def test_position_crud(test_client) -> None:
    from app.modules.system.position.schema import PositionCreateSchema, PositionUpdateSchema
    name = _name(); code = name
    try:
        async with _db() as db:
            svc = PositionService(_auth(), db)
            obj = await svc.create(PositionCreateSchema(name=name, code=code, order=1))
            assert (await svc.detail(obj.id)).name == name
            assert await svc.get_options()
            assert (await svc.page(1, 10)).total >= 1
            assert (await svc.get_list())
            await svc.set_available(BatchSetAvailable(ids=[obj.id], status=1))
            await svc.update(obj.id, PositionUpdateSchema(name=name, code=code, order=2, status=0))
            data = await svc.export_list([x.model_dump() for x in await svc.get_list()])
            assert data
            await svc.delete([obj.id])
    finally:
        await _cleanup(name)


async def test_position_duplicate_and_missing(test_client) -> None:
    from app.modules.system.position.schema import PositionCreateSchema
    name = _name()
    try:
        async with _db() as db:
            svc = PositionService(_auth(), db)
            await svc.create(PositionCreateSchema(name=name, code=name))
            with pytest.raises(CustomException):
                await svc.create(PositionCreateSchema(name=name, code=name))
            with pytest.raises(CustomException):
                await svc.delete([99999999])
            with pytest.raises(CustomException):
                await svc.delete([])
    finally:
        await _cleanup(name)
