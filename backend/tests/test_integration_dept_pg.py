"""真实 PostgreSQL 部门服务集成。"""

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
from app.modules.system.dept.service import DeptService

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
    return f"it_dept_{uuid.uuid4().hex[:10]}"


def _code() -> str:
    return f"it_dc_{uuid.uuid4().hex[:8]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


async def _cleanup(*names: str) -> None:
    async with _db() as db:
        for name in names:
            await db.execute(text("DELETE FROM sys_dept WHERE name=:n"), {"n": name})
        await db.commit()


async def test_dept_tree_and_detail(test_client) -> None:
    from app.modules.system.dept.schema import DeptCreateSchema
    parent = _name(); child = _name()
    try:
        async with _db() as db:
            service = DeptService(_auth(), db)
            p = await service.create(DeptCreateSchema(name=parent, code=_code(), order=1))
            c = await service.create(DeptCreateSchema(name=child, code=_code(), parent_id=p.id, order=1))
            detail = await service.detail(c.id)
            assert detail.parent_id == p.id
            tree = await service.tree()
            assert tree
    finally:
        await _cleanup(child, parent)


async def test_dept_update(test_client) -> None:
    from app.modules.system.dept.schema import DeptCreateSchema, DeptUpdateSchema
    name = _name(); new_name = _name()
    try:
        async with _db() as db:
            service = DeptService(_auth(), db)
            d = await service.create(DeptCreateSchema(name=name, code=_code(), order=1))
            out = await service.update(d.id, DeptUpdateSchema(name=new_name, code=_code(), order=2, status=1))
            assert out.name == new_name and out.status == 1
    finally:
        await _cleanup(name, new_name)


async def test_dept_delete_protection(test_client) -> None:
    from app.modules.system.dept.schema import DeptCreateSchema
    parent = _name(); child = _name()
    try:
        async with _db() as db:
            service = DeptService(_auth(), db)
            p = await service.create(DeptCreateSchema(name=parent, code=_code(), order=1))
            c = await service.create(DeptCreateSchema(name=child, code=_code(), parent_id=p.id, order=1))
            with pytest.raises(CustomException):
                await service.delete([p.id])
            await service.delete([c.id])
            await db.commit()
            await service.delete([p.id])
    finally:
        await _cleanup(child, parent)


async def test_dept_delete_missing(test_client) -> None:
    async with _db() as db:
        await DeptService(_auth(), db).delete([99999999])


async def test_dept_service_guards(test_client) -> None:
    from app.core.base_schema import BatchSetAvailable
    from app.modules.system.dept.schema import DeptCreateSchema, DeptUpdateSchema
    a = _name(); b = _name(); code = _code()
    try:
        async with _db() as db:
            svc = DeptService(_auth(), db)
            p = await svc.create(DeptCreateSchema(name=a, code=code, order=1))
            with pytest.raises(CustomException):
                await svc.create(DeptCreateSchema(name=a, code=_code(), order=1))
            with pytest.raises(CustomException):
                await svc.create(DeptCreateSchema(name=b, code=code, order=1))
            c = await svc.create(DeptCreateSchema(name=b, code=_code(), parent_id=p.id, order=1))
            with pytest.raises(CustomException):
                await svc.update(c.id, DeptUpdateSchema(name=a, code=c.code, order=1))
            with pytest.raises(CustomException):
                await svc.update(c.id, DeptUpdateSchema(name=c.name, code=code, order=1))
            with pytest.raises(CustomException):
                await svc.delete([])
            with pytest.raises(CustomException):
                await svc.delete([p.id])
            await svc.set_available(BatchSetAvailable(ids=[p.id], status=1))
            await svc.set_available(BatchSetAvailable(ids=[p.id], status=0))
    finally:
        await _cleanup(b, a)
