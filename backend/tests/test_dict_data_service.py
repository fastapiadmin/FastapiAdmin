"""字典数据服务 CRUD/缓存刷新分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.dict.schema import DictDataCreateSchema, DictDataUpdateSchema
from app.modules.system.dict.service import DictDataService


def _obj(**over):
    d = dict(id=1, dict_sort=1, dict_label="A", dict_value="a", dict_type="t", dict_type_id=1)
    d.update(over)
    return SimpleNamespace(**d)


def _svc(monkeypatch, crud, type_crud=None):
    import app.modules.system.dict.service as mod
    monkeypatch.setattr(mod, "DictDataCRUD", crud)
    if type_crud is not None: monkeypatch.setattr(mod, "DictTypeCRUD", type_crud)
    s = DictDataService.__new__(DictDataService); s.auth = object(); s.db = object()
    async def refresh(redis, dt): refresh.calls.append(dt)
    refresh.calls = []
    s._refresh_dict_cache = refresh
    return s


async def test_dict_data_create(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a): pass
        async def get(self, **kw): return None
        async def create(self, data): return _obj()
    s = _svc(monkeypatch, C)
    data = DictDataCreateSchema(dict_sort=1, dict_label="A", dict_value="a", dict_type="t", dict_type_id=1)
    assert (await s.create(object(), data)).dict_label == "A"
    class C2(C):
        async def get(self, **kw): return _obj()
    with pytest.raises(CustomException, match="标签"):
        await _svc(monkeypatch, C2).create(object(), data)


async def test_dict_data_update(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a):
            self.obj = _obj()
        async def get_or_404(self, **kw): return self.obj
        async def get(self, **kw): return None
        async def update(self, **kw): return self.obj
    class T:
        def __init__(self, *a): pass
        async def get(self, **kw): return _obj(dict_type="old")
    s = _svc(monkeypatch, C, T)
    data = DictDataUpdateSchema(dict_sort=1, dict_label="B", dict_value="b", dict_type="new", dict_type_id=1)
    assert (await s.update(object(), 1, data)).dict_type == "t"
    class C2(C):
        async def get(self, **kw): return _obj()
    with pytest.raises(CustomException, match="标签"):
        await _svc(monkeypatch, C2, T).update(object(), 1, data)


async def test_dict_data_delete(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a): self.objs = [_obj()]
        async def get_list(self, **kw): return self.objs
        async def delete(self, **kw): self.deleted = kw
    s = _svc(monkeypatch, C)
    with pytest.raises(CustomException, match="不能为空"):
        await s.delete(object(), [])
    with pytest.raises(CustomException, match="不存在"):
        await s.delete(object(), [2])
    await s.delete(object(), [1])


async def test_dict_data_set_available(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a): pass
        async def set(self, **kw): self.called = kw
    s = _svc(monkeypatch, C)
    from app.core.base_schema import BatchSetAvailable
    await s.set_available(BatchSetAvailable(ids=[1], status=1))
