"""CRUDBase 条件解析/排序/预加载分支。"""

from __future__ import annotations

from datetime import datetime

import pytest

from app.core.base_crud import CRUDBase
from app.modules.system.user.model import UserModel


def _crud():
    c = CRUDBase.__new__(CRUDBase)
    c.model = UserModel
    return c


def test_resolve_condition_all_operators() -> None:
    attr = UserModel.id
    resolve = CRUDBase._resolve_condition
    assert len(resolve(attr, ("None", None))) == 1
    assert len(resolve(attr, ("not None", None))) == 1
    assert resolve(attr, ("like", None)) == []
    assert len(resolve(attr, ("date", "2026-01-01"))) == 2
    assert len(resolve(attr, ("month", "2026-12"))) == 2
    assert len(resolve(attr, ("month", "2026-01"))) == 2
    assert len(resolve(attr, ("like", "a"))) == 1
    assert len(resolve(attr, ("in", []))) == 1
    assert len(resolve(attr, ("in", [1, 2]))) == 1
    assert len(resolve(attr, ("between", [1, 2]))) == 1
    assert resolve(attr, ("between", [1])) == []
    assert len(resolve(attr, (">", 1))) == 1
    assert resolve(attr, ("unknown", 1)) == []


def test_parse_order() -> None:
    cols = _crud()._parse_order([{"id": "desc"}, {"name": "ASC"}])
    assert len(cols) == 2


def test_loader_options_and_invalid_preload() -> None:
    c = _crud()
    assert isinstance(c._loader_options(None), list)
    assert isinstance(c._loader_options(["not_a_field"]), list)
    assert isinstance(c._loader_options(["not_a_field.x"]), list)
    # 已存在的 option 对象原样追加
    marker = object()
    assert marker in c._loader_options([marker])


def test_soft_delete_helpers() -> None:
    from types import SimpleNamespace
    c=_crud(); c.auth=SimpleNamespace(user=SimpleNamespace(id=1))
    assert c._supports_soft_delete is True
    assert c._get_pk_col().name == "id"
    values=c._soft_delete_values()
    assert values["is_deleted"] is True and values["deleted_id"]==1
    c.auth=SimpleNamespace(user=SimpleNamespace(id=0))
    assert "deleted_id" not in c._soft_delete_values()


async def test_update_missing() -> None:
    from types import SimpleNamespace
    c=_crud(); c.auth=SimpleNamespace(user=SimpleNamespace(id=1)); c.db=object()
    async def get(**kw): return None
    c.get=get
    with pytest.raises(Exception, match="更新对象不存在"):
        await c.update(1,{})
