"""真实 PostgreSQL 代码生成 CRUD/物理表探测集成。"""

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
    return f"it_gcrud_{uuid.uuid4().hex[:10]}"


async def _cleanup(table: str) -> None:
    async with _db() as db:
        await db.execute(text(f'DROP TABLE IF EXISTS "{table}"'))
        await db.execute(text("DELETE FROM gen_table WHERE table_name=:t"), {"t": table})
        await db.commit()


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


async def test_physical_table_detection(test_client) -> None:
    table = _name(); extra = _name()
    try:
        async with _db() as db:
            await db.execute(text(f'CREATE TABLE "{table}" (id SERIAL PRIMARY KEY, name VARCHAR(20))'))
            await db.execute(text(f'COMMENT ON TABLE "{table}" IS \'IT comment\''))
            await db.commit()
            crud = GenTableCRUD(_auth(), db)
            assert await crud.check_table_exists(table) is True
            assert await crud.check_table_exists("no_such_table_x") is False
            assert await crud.get_db_table_comment(table) == "IT comment"
            rows = await crud.get_db_table_list_by_names([table])
            assert rows and rows[0].table_name == table
            assert await crud.execute_sql(f'CREATE TABLE "{extra}" (id INT)') is True
    finally:
        await _cleanup(table); await _cleanup(extra)


async def test_gen_table_and_column_crud(test_client) -> None:
    table = _name()
    try:
        async with _db() as db:
            crud = GenTableCRUD(_auth(), db)
            from app.modules.generator.gencode.schema import GenTableColumnSchema, GenTableSchema
            obj = await crud.add_gen_table(GenTableSchema(table_name=table, class_name="ItCrud", package_name="module_it", module_name="it", business_name="demo", function_name="Demo"))
            assert obj.id and (await crud.get_gen_table_by_id(obj.id)).table_name == table
            assert (await crud.get_gen_table_by_name(table)).id == obj.id
            edited = await crud.edit_gen_table(obj.id, GenTableSchema(table_name=table, class_name="ItCrud2", package_name="module_it", module_name="it", business_name="demo", function_name="Demo"))
            assert edited.class_name == "ItCrud2"

            col = GenTableColumnCRUD(_auth(), db)
            created = await col.create_gen_table_column_crud(GenTableColumnSchema(table_id=obj.id, column_name="id", column_type="int"))
            assert created is not None
            assert (await col.get_gen_table_column_by_id(created.id)).column_name == "id"
            cols = await col.list_gen_table_column_crud_by_table_id(obj.id)
            assert len(cols) == 1
            updated = await col.update_gen_table_column_crud(created.id, GenTableColumnSchema(table_id=obj.id, column_name="id", column_type="bigint"))
            assert updated.column_type == "bigint"
            await col.delete_gen_table_column_by_column_id_crud([created.id])
            await crud.delete_gen_table([obj.id])
    finally:
        await _cleanup(table)
