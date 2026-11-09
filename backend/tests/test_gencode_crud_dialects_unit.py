"""代码生成物理表分页的 MySQL/回退分支（fake 会话）。"""

from __future__ import annotations

from types import SimpleNamespace

from app.modules.generator.gencode.crud import GenTableCRUD
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
