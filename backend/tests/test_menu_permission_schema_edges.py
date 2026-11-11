"""菜单 schema 归一化 / 数据权限分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.core.permission import Permission
from sqlalchemy import column


async def test_permission_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    class M:
        created_id = 1
        __name__ = "M"
    auth = SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=False, dept_id=2))
    p = Permission(M, auth, None)
    async def cond(): return "cond"
    monkeypatch.setattr(p, "_permission_condition", cond)
    assert await p.filter_query(SimpleNamespace(where=lambda c: "ok")) == "ok"
    p2 = Permission(M, SimpleNamespace(user=None), None)
    assert await p2._permission_condition() is None
    p3 = Permission(M, SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True)), None)
    assert await p3._permission_condition() is None
    p4 = Permission(object, auth, None)
    assert await p4._filter_by_data_scope() is None
    p5 = Permission(M, SimpleNamespace(user=None), None)
    assert await p5._filter_by_data_scope() is None
    async def scopes(): return {2}
    async def depts(s): return {2}
    monkeypatch.setattr(p, "_load_user_data_scopes", scopes)
    monkeypatch.setattr(p, "_get_accessible_dept_ids", depts)
    class Rel:
        property = SimpleNamespace(mapper=SimpleNamespace(class_=SimpleNamespace(dept_id=column("dept_id"))))
        def has(self, c): return "cond"
    M.created_by = Rel()
    assert await p._filter_by_data_scope() is not None
    assert p._relationship_column(None, "x") is None
    class Bad:
        property = SimpleNamespace(mapper=SimpleNamespace(class_=SimpleNamespace()))
    assert p._relationship_column(Bad(), "x") is None
