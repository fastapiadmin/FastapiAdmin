"""数据权限过滤分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.base_schema import AuthSchema
from app.core.permission import Permission


class Model:
    created_id = 1
    dept_id = 2


class NoCreated:
    pass


def _auth(**kw):
    base = dict(id=1, is_superuser=False, dept_id=2)
    base.update(kw)
    return AuthSchema(user=SimpleNamespace(**base))


async def test_permission_conditions(monkeypatch: pytest.MonkeyPatch) -> None:
    p = Permission(Model, _auth(), None)
    monkeypatch.setattr(p, "_load_user_data_scopes", lambda: _ret({3}))
    monkeypatch.setattr(p, "_get_accessible_dept_ids", lambda s: _ret({2}))
    assert await p._filter_by_data_scope() is None
    monkeypatch.setattr(p, "_load_user_data_scopes", lambda: _ret({1}))
    assert await p._filter_by_data_scope() is not None
    assert Permission(NoCreated, _auth(), None)._relationship_column(None, "x") is None


async def _ret(value):
    return value
