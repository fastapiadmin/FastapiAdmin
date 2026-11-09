"""代码生成 HTTP 接口（真实 PG）。"""

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
from app.modules.generator.gencode.crud import GenTableColumnCRUD, GenTableCRUD

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
    return f"it_gapi_{uuid.uuid4().hex[:8]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


async def test_gencode_api(test_client, auth_headers) -> None:
    from app.modules.generator.gencode.schema import GenTableColumnSchema, GenTableSchema
    table = _name()
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/gencode/list")).rsplit("/list", 1)[0]
    try:
        async with _db() as db:
            await db.execute(text(f'CREATE TABLE "{table}" (id SERIAL PRIMARY KEY, name VARCHAR(20))'))
            await db.execute(text(f'COMMENT ON TABLE "{table}" IS \'IT api\''))
            await db.commit()
            crud = GenTableCRUD(_auth(), db)
            obj = await crud.add_gen_table(GenTableSchema(table_name=table, table_comment="IT api", class_name="ItApi", package_name="module_it", module_name="itapi", business_name="demo", function_name="IT Api"))
            await GenTableColumnCRUD(_auth(), db).create_gen_table_column_crud(GenTableColumnSchema(table_id=obj.id, column_name="id", column_type="int", is_pk=True, html_type="input"))
            await db.commit()
            tid = obj.id
        assert test_client.get(f"{base}/list", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/db/list", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/detail/{tid}", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/preview/{tid}", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/sync_db/preview/{table}", headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/delete", json=[tid], headers=auth_headers).status_code == 200
    finally:
        async with _db() as db:
            await db.execute(text(f'DROP TABLE IF EXISTS "{table}"'))
            await db.execute(text("DELETE FROM gen_table WHERE table_name=:t"), {"t": table})
            await db.commit()
