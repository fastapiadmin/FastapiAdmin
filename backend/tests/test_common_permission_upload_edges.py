"""通用工具/权限/上传工具边缘。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.utils.common_util as U
from app.core.permission import Permission


def test_row_and_transform() -> None:
    from sqlalchemy import create_engine, select, literal
    e = create_engine("sqlite://")
    with e.connect() as c:
        row = c.execute(select(literal(1), literal(2))).first()
    assert U.SqlalchemyUtil.serialize_result(row) is not None
    assert U.SqlalchemyUtil.serialize_result([row]) is not None
    assert U.SqlalchemyUtil.serialize_result({"a_b": 1}, "snake_to_camel") == {"AB": 1}
    assert U.CamelCaseUtil.transform_result({"a_b": 1}) == {"AB": 1}
    assert U.SnakeCaseUtil.transform_result({"aB": 1}) == {"a_b": 1}
    assert U.SqlalchemyUtil.get_boolean_server_default("mysql", True) is not None


def test_traversal_children() -> None:
    nodes = [{"id": 1, "parent_id": None, "name": "a"}, {"id": 2, "parent_id": 99, "name": "b"}]
    tree = U.traversal_to_tree(nodes)
    assert tree


async def test_permission_self_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    class M:
        created_id = 1
        __name__ = "M"
    p = Permission(M, __import__("app.core.base_schema", fromlist=["AuthSchema"]).AuthSchema(user=SimpleNamespace(id=1, is_superuser=False, dept_id=None)), None)
    async def scopes(): return {1}
    async def depts(s): return set()
    monkeypatch.setattr(p, "_load_user_data_scopes", scopes)
    monkeypatch.setattr(p, "_get_accessible_dept_ids", depts)
    assert await p._filter_by_data_scope() is not None
    assert p._relationship_column(None, "x") is None
