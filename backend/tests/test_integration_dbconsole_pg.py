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


async def test_dbconsole_api(test_client, auth_headers) -> None:
    name = _name()
    payload = {"name": name, "db_type": "postgres", "host": "127.0.0.1", "port": 5432, "username": settings.DATABASE_USER, "password": settings.DATABASE_PASSWORD, "database": settings.DATABASE_NAME}
    try:
        created = test_client.post("/api/v1/ops/dbconsole/connection/create", json=payload, headers=auth_headers)
        assert created.status_code in (200, 201), created.text
        cid = created.json()["data"]["id"]
        assert test_client.get("/api/v1/ops/dbconsole/connection/list", headers=auth_headers).status_code == 200
        assert test_client.get(f"/api/v1/ops/dbconsole/connection/detail/{cid}", headers=auth_headers).status_code == 200
        assert test_client.post(f"/api/v1/ops/dbconsole/connection/test/{cid}", headers=auth_headers).status_code == 200
        assert test_client.get(f"/api/v1/ops/dbconsole/connection/{cid}/databases", headers=auth_headers).status_code == 200
        assert test_client.get(f"/api/v1/ops/dbconsole/connection/{cid}/tables", headers=auth_headers).status_code == 200
        q = test_client.post(f"/api/v1/ops/dbconsole/connection/{cid}/query", json={"sql": "SELECT 1 AS n"}, headers=auth_headers)
        assert q.status_code == 200
        assert test_client.request("DELETE", "/api/v1/ops/dbconsole/connection/delete", json=[cid], headers=auth_headers).status_code == 200
    finally:
        await _cleanup(name)


async def test_connection_update_and_missing(test_client) -> None:
    from app.modules.ops.dbconsole.schema import DbConnectionUpdateSchema
    from app.core.exceptions import CustomException
    name = _name()
    try:
        async with _db() as db:
            svc = DbConsoleService(_auth(), db)
            row = await svc.create(_data(name))
            updated = await svc.update(row.id, DbConnectionUpdateSchema(name=name + "x", db_type="postgres", host="127.0.0.1", port=5432, username=settings.DATABASE_USER, password=None, database=settings.DATABASE_NAME))
            assert updated.name.endswith("x")
            with pytest.raises(CustomException):
                await svc.test_by_id(99999999)
            await svc.delete([row.id])
            with pytest.raises(CustomException):
                await svc.detail(row.id)
    finally:
        await _cleanup(name); await _cleanup(name + "x")


async def test_dbconsole_edge_branches(test_client) -> None:
    from app.modules.ops.dbconsole.schema import DbConnectionUpdateSchema
    from app.core.exceptions import CustomException
    name = _name()
    try:
        async with _db() as db:
            svc = DbConsoleService(_auth(), db)
            row = await svc.create(_data(name))
            with pytest.raises(CustomException):
                await svc.create(_data(name))
            with pytest.raises(CustomException):
                await svc.run_query(row.id, "")
            with pytest.raises(CustomException):
                await svc.run_query(row.id, "SELECT 1; SELECT 2", confirmed=True)
            res = await svc.run_query(row.id, "CREATE TEMP TABLE it_tmp (id INT)", confirmed=True)
            assert res.read_only is False
    finally:
        await _cleanup(name)


async def test_dbconsole_mysql_branches(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.ops.dbconsole.schema import DbConnectionCreateSchema
    from app.core.exceptions import CustomException
    name = _name()
    try:
        async with _db() as db:
            svc = DbConsoleService(_auth(), db)
            row = await svc.create(DbConnectionCreateSchema(name=name, db_type="mysql", host="127.0.0.1", port=3306, username="u", password="p", database=None))
            async def fetch(*a, **k): return [["t1"]]
            svc._fetch = fetch
            assert await svc.list_databases(row.id)
            with pytest.raises(CustomException):
                await svc.list_tables(row.id)
    finally:
        await _cleanup(name)


async def test_connection_duplicate_update(test_client) -> None:
    from app.modules.ops.dbconsole.schema import DbConnectionUpdateSchema
    from app.core.exceptions import CustomException
    a = _name(); b = _name()
    try:
        async with _db() as db:
            svc = DbConsoleService(_auth(), db)
            await svc.create(_data(a)); row = await svc.create(_data(b))
            with pytest.raises(CustomException):
                await svc.update(row.id, DbConnectionUpdateSchema(name=a, db_type="postgres", host="127.0.0.1", port=5432, username=settings.DATABASE_USER, database=settings.DATABASE_NAME))
            await svc.update(row.id, DbConnectionUpdateSchema(name=b, db_type="postgres", host="127.0.0.1", port=5432, username=settings.DATABASE_USER, password=None, database=settings.DATABASE_NAME))
    finally:
        await _cleanup(a); await _cleanup(b)
