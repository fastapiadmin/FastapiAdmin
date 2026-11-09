"""代码生成写盘（隔离到临时仓库目录，不污染真实仓库）。"""

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
    return f"it_gen_{uuid.uuid4().hex[:8]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0, username="it"))


async def test_generate_code_isolated(test_client, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.generator.gencode.schema import GenTableColumnSchema, GenTableSchema
    from app.modules.generator.gencode.service import GenTableService
    import app.modules.generator.gencode.service as svc_mod

    table = _name(); func = f"IT {table}"
    root = tmp_path / "repo"; (root / "backend" / "app" / "plugin").mkdir(parents=True)
    (root / "backend" / "alembic.ini").write_text("[alembic]\n")
    monkeypatch.setattr(svc_mod, "BASE_DIR", root / "backend")
    try:
        async with _db() as db:
            await db.execute(text(f'CREATE TABLE "{table}" (id SERIAL PRIMARY KEY, name VARCHAR(20))'))
            await db.execute(text(f'COMMENT ON TABLE "{table}" IS \'IT generate\''))
            await db.commit()
            crud = GenTableCRUD(_auth(), db)
            obj = await crud.add_gen_table(GenTableSchema(table_name=table, table_comment="IT generate", class_name="ItGenerate", package_name="module_it", module_name=f"it{uuid.uuid4().hex[:6]}", business_name="demo", function_name=func))
            col = GenTableColumnCRUD(_auth(), db)
            await col.create_gen_table_column_crud(GenTableColumnSchema(table_id=obj.id, column_name="id", column_type="int", is_pk=True, html_type="input"))
            await col.create_gen_table_column_crud(GenTableColumnSchema(table_id=obj.id, column_name="name", column_type="varchar(20)", html_type="input"))
            await db.commit()
            monkeypatch.setattr(GenTableService, "_write_plugin_migration", staticmethod(lambda s: _noop()))
            assert await GenTableService(_auth(), db).generate_code(table) is True
            await db.commit()
            written = list(root.rglob("*.py"))
            assert written
            await crud.delete_gen_table([obj.id])
            await db.execute(text("DELETE FROM sys_menu WHERE name=:n"), {"n": func})
            await db.commit()
    finally:
        async with _db() as db:
            await db.execute(text("DELETE FROM sys_menu WHERE name=:n"), {"n": func})
            await db.execute(text(f'DROP TABLE IF EXISTS "{table}"'))
            await db.execute(text("DELETE FROM gen_table WHERE table_name=:t"), {"t": table})
            await db.commit()


async def _noop():
    return None
