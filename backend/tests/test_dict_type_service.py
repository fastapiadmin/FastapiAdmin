"""字典类型服务 CRUD/缓存联动。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.dict.schema import DictTypeCreateSchema, DictTypeUpdateSchema
from app.modules.system.dict.service import DictTypeService


def _svc(monkeypatch: pytest.MonkeyPatch, crud, data=None):
    import app.modules.system.dict.service as mod
    monkeypatch.setattr(mod, "DictTypeCRUD", crud)
    if data is not None: monkeypatch.setattr(mod, "DictDataCRUD", data)
    s = DictTypeService.__new__(DictTypeService); s.auth = object(); s.db = object()
    return s


async def test_create_dict_type(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a): pass
        async def get(self, **kw): return None
        async def create(self, data): return SimpleNamespace(dict_name="n", dict_type="t", status=0)
    s = _svc(monkeypatch, C)
    from app.core.redis_crud import RedisCURD
    async def set_(key, value, expire=None): return True
    monkeypatch.setattr(RedisCURD, "set", staticmethod(set_))
    out = await s.create(object(), DictTypeCreateSchema(dict_name="n", dict_type="t"))
    assert out.dict_type == "t"
    class C2(C):
        async def get(self, **kw): return object()
    s2 = _svc(monkeypatch, C2)
    with pytest.raises(CustomException, match="已存在"):
        await s2.create(object(), DictTypeCreateSchema(dict_name="n", dict_type="t"))


async def test_update_dict_type(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a):
            self.obj = SimpleNamespace(dict_name="n", dict_type="t", status=0, id=1, model_dump=lambda mode="json": {"id": 1})
        async def get_or_404(self, **kw): return self.obj
        async def update(self, **kw): return self.obj
    class D(C):
        async def get_list(self, **kw): return [SimpleNamespace(id=1, dict_sort=1, dict_label="A", dict_value="a", dict_type="t", dict_type_id=1)]
        async def set(self, **kw): self.set_called = kw
    s = _svc(monkeypatch, C, D)
    from app.core.redis_crud import RedisCURD
    async def set_(key, value, expire=None): return True
    monkeypatch.setattr(RedisCURD, "set", staticmethod(set_))
    out = await s.update(object(), 1, DictTypeUpdateSchema(dict_name="n", dict_type="t2"))
    assert out.dict_type == "t"
    with pytest.raises(CustomException, match="名称不可以修改"):
        await s.update(object(), 1, DictTypeUpdateSchema(dict_name="x", dict_type="t"))


async def test_delete_dict_type(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a): pass
        async def get_list(self, **kw):
            if "id" in kw: return [SimpleNamespace(id=1, dict_type="t")]
            return []
        async def delete(self, **kw): self.deleted = kw
    class D:
        def __init__(self, *a): pass
        async def get_list(self, **kw): return [SimpleNamespace(id=1,dict_sort=1,dict_label="A",dict_value="a",dict_type="t",dict_type_id=1)]
    class DEmpty(D):
        async def get_list(self, **kw): return []
    s = _svc(monkeypatch, C, D)
    from app.core.redis_crud import RedisCURD
    async def delete_(key): return True
    monkeypatch.setattr(RedisCURD, "delete", staticmethod(delete_))
    with pytest.raises(CustomException, match="不能为空"):
        await s.delete(object(), [])
    class C2(C):
        async def get_list(self, **kw):
            return [SimpleNamespace(id=1, dict_type="t")]
    s2 = _svc(monkeypatch, C2, D)
    with pytest.raises(CustomException, match="存在字典数据"):
        await s2.delete(object(), [1])
    with pytest.raises(CustomException, match="不存在"):
        await s2.delete(object(), [2])
    class C3(C):
        async def get_list(self, **kw):
            return [SimpleNamespace(id=1, dict_type="t")]
    s3 = _svc(monkeypatch, C3, DEmpty)
    await s3.delete(object(), [1])


async def test_dict_type_set_available(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a): pass
        async def set(self, **kw): self.called = kw
    s = _svc(monkeypatch, C)
    from app.core.base_schema import BatchSetAvailable
    await s.set_available(BatchSetAvailable(ids=[1], status=1))


async def test_update_type_no_cascade(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self,*a): self.obj=SimpleNamespace(dict_name="n",dict_type="t",status=0,id=1)
        async def get_or_404(self,**kw): return self.obj
        async def update(self,**kw): return self.obj
    class D:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return []
    s=_svc(monkeypatch,C,D)
    from app.core.redis_crud import RedisCURD
    async def set_(key,value,expire=None): return True
    monkeypatch.setattr(RedisCURD,"set",staticmethod(set_))
    assert (await s.update(object(),1,DictTypeUpdateSchema(dict_name="n",dict_type="t",status=0))).dict_type == "t"


async def test_update_type_status_cascade(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self,*a): self.obj=SimpleNamespace(dict_name="n",dict_type="t",status=0,id=1)
        async def get_or_404(self,**kw): return self.obj
        async def update(self,**kw): return self.obj
    class D:
        def __init__(self,*a): self.set_called=None
        async def get_list(self,**kw): return [SimpleNamespace(id=1)]
        async def set(self,**kw): self.set_called=kw
    s=_svc(monkeypatch,C,D)
    from app.core.redis_crud import RedisCURD
    async def set_(key,value,expire=None): return True
    monkeypatch.setattr(RedisCURD,"set",staticmethod(set_))
    out=await s.update(object(),1,DictTypeUpdateSchema(dict_name="n",dict_type="t",status=1))
    assert out.dict_type == "t"
