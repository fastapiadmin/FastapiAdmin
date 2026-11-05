"""代码生成器同步差异预览覆盖。"""

from __future__ import annotations

import pytest

from app.core.exceptions import CustomException
from app.modules.generator.gencode.schema import GenTableColumnOutSchema, GenTableOutSchema
from app.modules.generator.gencode.service import GenTableService


def test_sync_diff_added_removed_changed_unchanged() -> None:
    svc = GenTableService.__new__(GenTableService)
    cur = [
        GenTableColumnOutSchema(column_name="a", column_type="int"),
        GenTableColumnOutSchema(column_name="b", column_type="int"),
        GenTableColumnOutSchema(column_name="gone", column_type="int"),
    ]
    db = [
        GenTableColumnOutSchema(column_name="a", column_type="int"),
        GenTableColumnOutSchema(column_name="b", column_type="varchar(10)"),
        GenTableColumnOutSchema(column_name="added_col", column_type="int"),
    ]
    added, removed, changed, unchanged = svc._sync_preview_diff(cur, db)
    assert added == ["added_col"] and removed == ["gone"] and unchanged == 1
    assert changed[0].column_name == "b" and "column_type" in changed[0].change_fields


async def test_sync_preview_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = GenTableService.__new__(GenTableService); svc.auth = object(); svc.db = object()
    with pytest.raises(CustomException, match="表名不能为空"):
        await svc.sync_db_preview("")
    from app.modules.generator.gencode import service as mod
    class CRUD:
        def __init__(self, *a): pass
        async def get_gen_table_by_name(self, name, preload=None): return None
    monkeypatch.setattr(mod, "GenTableCRUD", CRUD)
    with pytest.raises(CustomException, match="业务表不存在"):
        await svc.sync_db_preview("x")


async def test_sync_preview_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.generator.gencode import service as mod
    table = GenTableOutSchema(id=1, table_name="demo", columns=[GenTableColumnOutSchema(column_name="a", column_type="int")])
    class CRUD:
        def __init__(self, *a): pass
        async def get_gen_table_by_name(self, name, preload=None): return table
    monkeypatch.setattr(mod, "GenTableCRUD", CRUD)
    svc = GenTableService.__new__(GenTableService); svc.auth = object(); svc.db = object()
    async def cols(name): return [GenTableColumnOutSchema(column_name="a", column_type="varchar(10)")]
    svc._get_db_table_columns = cols
    result = await svc.sync_db_preview("demo")
    assert result.table_name == "demo" and result.changed[0].column_name == "a"
