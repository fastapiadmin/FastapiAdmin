"""代码生成物理表分页的 MySQL/回退分支（fake 会话）。"""

from __future__ import annotations

import pytest
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


def test_crud_more_branches(monkeypatch) -> None:
    import app.modules.generator.gencode.crud as c
    class Type:
        def __init__(self, s, item=None): self.s=s; self.item_type=item
        def __str__(self): return self.s
    class Insp:
        def get_table_names(self): return []
        def has_table(self, n): return True
        def get_table_comment(self, n): raise RuntimeError("x")
        def get_columns(self, n):
            return [
                {"name": "a", "type": Type("INTEGER[]", Type("INTEGER")), "nullable": True, "default": None, "comment": ""},
                {"name": "b", "type": Type("VARCHAR(10) COLLATE x"), "nullable": False, "default": "", "comment": ""},
            ]
        def get_pk_constraint(self, n): raise RuntimeError("x")
        def get_unique_constraints(self, n): return [{"column_names": ["a"]}]
    monkeypatch.setattr(c, "inspect", lambda e: Insp())
    assert c.GenTableCRUD._sync_get_db_table_comment("x") == ""
    assert c.GenTableCRUD._sync_get_db_table_list_by_names([]) == []
    pg = c.GenTableColumnCRUD._sync_get_table_columns("postgres", "x")
    my = c.GenTableColumnCRUD._sync_get_table_columns("mysql", "x")
    assert pg and my
    monkeypatch.setattr(c.asyncio, "to_thread", lambda *a: (_ for _ in ()).throw(RuntimeError("x")))
    import asyncio as _a
    with pytest.raises(RuntimeError):
        _a.run(c.GenTableColumnCRUD(object(), object()).get_gen_db_table_columns_by_name("x"))


async def test_delete_columns_by_table() -> None:
    class Res:
        def fetchall(self): return [(1,), (2,)]
    class DB:
        async def execute(self, *a): return Res()
    crud = GenTableColumnCRUD(SimpleNamespace(user=None), DB())
    called = {}
    async def delete(ids): called["ids"] = ids
    crud.delete = delete
    await crud.delete_gen_table_column_by_table_id_crud([1])
    assert called["ids"] == [1, 2]
