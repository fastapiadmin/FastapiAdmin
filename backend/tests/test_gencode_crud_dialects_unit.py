"""代码生成物理表分页的 MySQL/回退分支（fake 会话）。"""

from __future__ import annotations

from types import SimpleNamespace

from app.modules.generator.gencode.crud import GenTableColumnCRUD, GenTableCRUD
from app.modules.generator.gencode import crud as crud_mod


class _R:
    def scalar(self): return 1
    def fetchall(self): return [("t1", "c1")]


class _DB:
    async def execute(self, *a, **k): return _R()


def _crud():
    return GenTableCRUD(SimpleNamespace(user=None), _DB())


async def test_mysql_page(monkeypatch) -> None:
    monkeypatch.setattr(crud_mod.settings, "DATABASE_TYPE", "mysql")
    items, total = await _crud().get_db_table_page(table_name="t", table_comment="c", offset=0, limit=10)
    assert total == 1 and items[0]["table_name"] == "t1"


async def test_fallback_page(monkeypatch) -> None:
    monkeypatch.setattr(crud_mod.settings, "DATABASE_TYPE", "sqlite")
    async def listing(**k): return [{"table_name": "a"}, {"table_name": "b"}]
    c = _crud(); c.get_db_table_list = listing
    items, total = await c.get_db_table_page(offset=0, limit=1)
    assert total == 2 and len(items) == 1


def test_sync_helpers_errors(monkeypatch) -> None:
    import app.modules.generator.gencode.crud as c
    class Insp:
        def get_table_names(self): return ["a", "b"]
        def get_table_comment(self, name):
            if name == "a": raise RuntimeError("x")
            return {"text": "B"}
        def has_table(self, name): return name == "b"
        def get_columns(self, name): return []
        def get_pk_constraint(self, name): return None
        def get_unique_constraints(self, name): return []
    monkeypatch.setattr(c, "inspect", lambda e: Insp())
    rows = c.GenTableCRUD._sync_get_db_table_list(None, None)
    assert {r["table_name"] for r in rows} == {"a", "b"}
    by = c.GenTableCRUD._sync_get_db_table_list_by_names(["a", "missing", "b"])
    assert {r.table_name for r in by} == {"a", "b"}
    assert c.GenTableCRUD._sync_get_db_table_comment("missing") == ""
    assert c.GenTableCRUD._sync_get_db_table_comment("b") == "B"


async def test_execute_sql_error() -> None:
    class DB:
        async def execute(self, *a, **k): raise RuntimeError("x")
    c = GenTableCRUD(SimpleNamespace(user=None), DB())
    assert await c.execute_sql("SELECT 1") is False


async def test_get_columns_guard() -> None:
    import pytest as _p
    c = GenTableColumnCRUD(SimpleNamespace(user=None), object())
    with _p.raises(ValueError):
        await c.get_gen_db_table_columns_by_name(None)
