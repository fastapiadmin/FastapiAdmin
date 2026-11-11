"""验证器/数据权限剩余分支。"""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

import pytest

import app.core.validator as V
from app.core.exceptions import CustomException
from app.core.permission import Permission


def test_validator_extra(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(CustomException):
        V.datetime_validator("bad")
    with pytest.raises(CustomException):
        V.date_validator("bad")
    with pytest.raises(CustomException):
        V.time_validator("bad")
    with pytest.raises(ValueError):
        V.password_validator("a" * 128)
    monkeypatch.setattr(V.settings, "TIMEZONE", "Bad/Zone")
    assert V.to_local_datetime(datetime(2026, 1, 1)) is not None
    with pytest.raises(CustomException):
        V.menu_request_validator(SimpleNamespace(type=99))


async def test_permission_more(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        created_id = 1
        dept_id = 2
        __name__ = "UserModel"
    auth = SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=False, dept_id=2))
    p = Permission(U, auth, None)
    async def scopes(): return {2}
    async def depts(s): return {2}
    monkeypatch.setattr(p, "_load_user_data_scopes", scopes)
    monkeypatch.setattr(p, "_get_accessible_dept_ids", depts)
    assert await p._filter_by_data_scope() is not None
    async def scopes2(): return {1}
    monkeypatch.setattr(p, "_load_user_data_scopes", scopes2)
    assert await p._filter_by_data_scope() is not None
    async def scopes3(): return set()
    monkeypatch.setattr(p, "_load_user_data_scopes", scopes3)
    assert await p._filter_by_data_scope() is not None
