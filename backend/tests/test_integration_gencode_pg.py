"""真实 PostgreSQL 代码生成同步集成：物理表 -> gen_table_column。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.modules.generator.gencode.model import GenTableColumnModel, GenTableModel
from app.modules.generator.gencode.service import GenTableService

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
    return f"it_gen_{uuid.uuid4().hex[:10]}"


async def _cleanup(table: str) -> None:
    async with _db() as db:
        await db.execute(text(f'DROP TABLE IF EXISTS "{table}"'))
        await db.execute(text("DELETE FROM gen_table WHERE table_name=:t"), {"t": table})
        await db.commit()


async def test_sync_db_creates_columns(test_client) -> None:
    table = _name()
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            await db.execute(text(f'CREATE TABLE "{table}" (id SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL, age INT)'))
            await db.commit()
            gen = GenTableModel(table_name=table, class_name="ItGen", table_comment="it")
            db.add(gen); await db.commit(); await db.refresh(gen)
            service = GenTableService(auth, db)
            await service.sync_db(table)
            cols = (await db.execute(select(GenTableColumnModel).where(GenTableColumnModel.table_id == gen.id))).scalars().all()
            names = {c.column_name for c in cols}
            assert {"id", "name", "age"} <= names
            pk = next(c for c in cols if c.column_name == "id")
            assert pk.is_pk is True
    finally:
        await _cleanup(table)


async def test_sync_db_is_idempotent_and_removes_stale(test_client) -> None:
    table = _name()
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            await db.execute(text(f'CREATE TABLE "{table}" (id SERIAL PRIMARY KEY, name VARCHAR(50))'))
            await db.commit()
            gen = GenTableModel(table_name=table, class_name="ItGen")
            db.add(gen); await db.commit(); await db.refresh(gen)
            service = GenTableService(auth, db)
            await service.sync_db(table)
            await service.sync_db(table)
            count = len((await db.execute(select(GenTableColumnModel).where(GenTableColumnModel.table_id == gen.id))).scalars().all())
            assert count == 2
            await db.execute(text(f'ALTER TABLE "{table}" ADD COLUMN age INT'))
            await db.commit()
            await service.sync_db(table)
            names = {c.column_name for c in (await db.execute(select(GenTableColumnModel).where(GenTableColumnModel.table_id == gen.id))).scalars().all()}
            assert "age" in names
    finally:
        await _cleanup(table)


async def test_batch_gen_code_real_table(test_client) -> None:
    import io
    import zipfile
    table = _name()
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            await db.execute(text(f'CREATE TABLE "{table}" (id SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL)'))
            await db.commit()
            gen = GenTableModel(table_name=table, class_name="ItGen", table_comment="it")
            db.add(gen); await db.commit(); await db.refresh(gen)
            service = GenTableService(auth, db)
            await service.sync_db(table)
            gen.package_name = "module_it"; gen.module_name = "it"; gen.business_name = "demo"; gen.function_name = "Demo"
            await db.commit()
            data, failed = await service.batch_gen_code([table])
            assert failed == []
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                names = z.namelist()
                assert names and any(n.endswith(".py") for n in names)
    finally:
        await _cleanup(table)
