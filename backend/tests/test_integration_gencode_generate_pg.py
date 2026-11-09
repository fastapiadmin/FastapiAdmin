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


async def test_generate_guards(test_client) -> None:
    from app.modules.generator.gencode.service import GenTableService
    from app.core.exceptions import CustomException
    async with _db() as db:
        svc = GenTableService(_auth(), db)
        with pytest.raises(CustomException):
            await svc.generate_code("")
        with pytest.raises(CustomException):
            await svc.batch_gen_code([])
        with pytest.raises(CustomException):
            await svc.preview_code(99999999)


async def test_generate_code_with_sub(test_client, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.generator.gencode.schema import GenTableColumnSchema, GenTableSchema
    from app.modules.generator.gencode.service import GenTableService
    import app.modules.generator.gencode.service as svc_mod
    main = _name(); sub = _name(); func = f"IT Sub {main}"
    root = tmp_path / "repo"; (root / "backend" / "app" / "plugin").mkdir(parents=True)
    monkeypatch.setattr(svc_mod, "BASE_DIR", root / "backend")
    async def noop(_): return None
    monkeypatch.setattr(GenTableService, "_write_plugin_migration", staticmethod(noop))
    try:
        async with _db() as db:
            await db.execute(text(f'CREATE TABLE "{main}" (id SERIAL PRIMARY KEY)'))
            await db.execute(text(f'CREATE TABLE "{sub}" (id SERIAL PRIMARY KEY, main_id INT)'))
            await db.commit()
            crud = GenTableCRUD(_auth(), db)
            sub_obj = await crud.add_gen_table(GenTableSchema(table_name=sub, class_name="SubRow", package_name="module_it", module_name=f"its{uuid.uuid4().hex[:5]}", business_name="sub", function_name="SubRow"))
            await GenTableColumnCRUD(_auth(), db).create_gen_table_column_crud(GenTableColumnSchema(table_id=sub_obj.id, column_name="main_id", column_type="int", html_type="input"))
            main_obj = await crud.add_gen_table(GenTableSchema(table_name=main, class_name="MainRow", package_name="module_it", module_name=f"itm{uuid.uuid4().hex[:5]}", business_name="main", function_name=func, sub_table_name=sub, sub_table_fk_name="main_id"))
            await db.commit()
            assert await GenTableService(_auth(), db).generate_code(main) is True
            await crud.delete_gen_table([main_obj.id, sub_obj.id])
            await db.execute(text("DELETE FROM sys_menu WHERE name=:n"), {"n": func})
            await db.commit()
    finally:
        async with _db() as db:
            await db.execute(text(f'DROP TABLE IF EXISTS "{main}"'))
            await db.execute(text(f'DROP TABLE IF EXISTS "{sub}"'))
            await db.execute(text("DELETE FROM gen_table WHERE table_name IN (:m,:s)"), {"m": main, "s": sub})
            await db.execute(text("DELETE FROM sys_menu WHERE name=:n"), {"n": func})
            await db.commit()
