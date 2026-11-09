"""真实 PostgreSQL 数据库控制台集成（以本机测试库为被管理库）。"""

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
from app.modules.ops.dbconsole.service import DbConsoleService

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
    return f"it_db_{uuid.uuid4().hex[:10]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0, is_superuser=True))


def _data(name: str):
    from app.modules.ops.dbconsole.schema import DbConnectionCreateSchema
    return DbConnectionCreateSchema(
        name=name, db_type="postgres", host="127.0.0.1", port=5432,
        username=settings.DATABASE_USER, password=settings.DATABASE_PASSWORD,
        database=settings.DATABASE_NAME,
    )


async def _cleanup(name: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM dbconsole_connection WHERE name=:n"), {"n": name})
        await db.commit()


async def test_connection_roundtrip(test_client) -> None:
    name = _name()
    try:
        async with _db() as db:
            service = DbConsoleService(_auth(), db)
            row = await service.create(_data(name))
            assert row.name == name and row.has_password is True
            assert any(x.name == name for x in await service.get_list())
            assert (await service.detail(row.id)).name == name
            assert await service.test_by_id(row.id) is True
            await service.delete([row.id])
    finally:
        await _cleanup(name)


async def test_test_connection_inline(test_client) -> None:
    from app.modules.ops.dbconsole.schema import DbConnectionTestSchema
    async with _db() as db:
        service = DbConsoleService(_auth(), db)
        data = DbConnectionTestSchema(db_type="postgres", host="127.0.0.1", port=5432, username=settings.DATABASE_USER, password=settings.DATABASE_PASSWORD, database=settings.DATABASE_NAME)
        assert await service.test_connection(data) is True


async def test_list_databases_and_tables(test_client) -> None:
    name = _name()
    try:
        async with _db() as db:
            service = DbConsoleService(_auth(), db)
            row = await service.create(_data(name))
            dbs = await service.list_databases(row.id)
            assert any(x.name == settings.DATABASE_NAME for x in dbs)
            tables = await service.list_tables(row.id)
            assert any(x.name == "sys_user" for x in tables)
    finally:
        await _cleanup(name)


async def test_run_select_and_reject_unconfirmed_write(test_client) -> None:
    name = _name()
    try:
        async with _db() as db:
            service = DbConsoleService(_auth(), db)
            row = await service.create(_data(name))
            result = await service.run_query(row.id, "SELECT 1 AS n")
            assert result.columns == ["n"] and result.rows == [[1]]
            with pytest.raises(CustomException, match="确认"):
                await service.run_query(row.id, "DELETE FROM sys_user WHERE id=-1")
    finally:
        await _cleanup(name)
