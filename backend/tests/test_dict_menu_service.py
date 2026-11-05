"""字典缓存与菜单父级规则覆盖。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.dict.service import DictDataService
from app.modules.system.menu.service import MenuService


class Redis:
    def __init__(self, value=None): self.value = value; self.set_calls = []
    async def get(self, key): return self.value
    async def set(self, key, value, expire=None): self.set_calls.append((key, value, expire))


async def test_get_init_cache_cached_and_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.redis_crud import RedisCURD
    async def get(_key): return '[{"a":1}]'
    monkeypatch.setattr(RedisCURD, "get", staticmethod(get))
    assert await DictDataService.get_init_cache(object(), "t") == [{"a": 1}]
    async def get_list(_key): return [{"a": 2}]
    monkeypatch.setattr(RedisCURD, "get", staticmethod(get_list))
    assert await DictDataService.get_init_cache(object(), "t") == [{"a": 2}]
    async def bad(_key): return "not-json"
    monkeypatch.setattr(RedisCURD, "get", staticmethod(bad))
    async def no_init(_): return None
    monkeypatch.setattr(DictDataService, "init_cache", staticmethod(no_init))
    with pytest.raises(CustomException, match="不存在"):
        await DictDataService.get_init_cache(object(), "t")


async def test_refresh_dict_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.dict.service as mod
    class D:
        def __init__(self, *a): pass
        async def get_list(self, **kw): return [SimpleNamespace(dict_sort=1, dict_label="A", dict_value="a", dict_type="t", dict_type_id=1)]
    monkeypatch.setattr(mod, "DictDataCRUD", D)
    import app.core.redis_crud as rc
    calls = []
    async def set_(key, value, expire=None): calls.append((key, value, expire))
    monkeypatch.setattr(rc.RedisCURD, "set", staticmethod(set_))
    s = DictDataService.__new__(DictDataService); s.auth = object(); s.db = object()
    await s._refresh_dict_cache(object(), "t")
    assert calls and calls[0][0].endswith(":1:t")


async def test_menu_parent_type(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.menu.service as mod
    class M:
        def __init__(self, *a): pass
        async def get(self, **kw): return None
    monkeypatch.setattr(mod, "MenuCRUD", M)
    s = MenuService.__new__(MenuService); s.auth = object(); s.db = object()
    await s._validate_parent_child_type(None, None)
    await s._validate_parent_child_type(None, 1)
    with pytest.raises(CustomException, match="顶级菜单"):
        await s._validate_parent_child_type(None, 3)
    with pytest.raises(CustomException, match="父级菜单不存在"):
        await s._validate_parent_child_type(1, 2)
    class M2(M):
        async def get(self, **kw): return SimpleNamespace(type=1)
    monkeypatch.setattr(mod, "MenuCRUD", M2)
    await s._validate_parent_child_type(1, 2)
    with pytest.raises(CustomException, match="目录下"):
        await s._validate_parent_child_type(1, 3)
    class M3(M):
        async def get(self, **kw): return SimpleNamespace(type=2)
    monkeypatch.setattr(mod, "MenuCRUD", M3)
    await s._validate_parent_child_type(1, 3)
    with pytest.raises(CustomException, match="按钮"):
        await s._validate_parent_child_type(1, 2)
    class M4(M):
        async def get(self, **kw): return SimpleNamespace(type=4)
    monkeypatch.setattr(mod, "MenuCRUD", M4)
    with pytest.raises(CustomException):
        await s._validate_parent_child_type(1, 2)


async def test_menu_parent_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.menu.service as mod
    class M:
        def __init__(self, *a): pass
        async def get(self, **kw): return SimpleNamespace(scope="web")
    monkeypatch.setattr(mod, "MenuCRUD", M)
    s = MenuService.__new__(MenuService); s.auth = object(); s.db = object()
    await s._validate_parent_child_scope(None, None)
    await s._validate_parent_child_scope(1, "web")
    with pytest.raises(CustomException, match="可见范围"):
        await s._validate_parent_child_scope(1, "app")


async def test_menu_crud_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.menu.schema import MenuCreateSchema, MenuOutSchema, MenuUpdateSchema
    import app.modules.system.menu.service as mod
    menu = MenuOutSchema(id=1, name="n", type=1, order=1, title="t", status=0, parent_id=None, route_name="n", route_path="/n", component_path="n/index", redirect="/n")
    class M:
        def __init__(self, *a): pass
        async def get(self, **kw): return None if kw.get("id") == 9 else menu
        async def get_or_404(self, **kw): return menu
        async def create(self, data): return menu
        async def update(self, **kw): return menu
        async def get_list(self, **kw): return [menu]
        async def delete(self, ids): self.deleted = ids
        async def set(self, **kw): self.set_data = kw
    monkeypatch.setattr(mod, "MenuCRUD", M)
    s = MenuService.__new__(MenuService); s.auth = object(); s.db = object()
    async def noop(*a, **k): return None
    s._validate_parent_child_type = noop; s._validate_parent_child_scope = noop
    assert (await s.detail(1)).name == "n"
    assert (await s.tree())[0]["name"] == "n"
    assert (await s.create(MenuCreateSchema(name="n", type=1, order=1, route_name="n", route_path="/n", component_path="n/index", redirect="/n"))).name == "n"
    assert (await s.update(1, MenuUpdateSchema(name="n", type=1, order=1, route_name="n", route_path="/n", component_path="n/index", redirect="/n"))).name == "n"
    with pytest.raises(CustomException, match="不能为空"):
        await s.delete([])
    await s.delete([1])
    from app.core.base_schema import BatchSetAvailable
    await s.set_available(BatchSetAvailable(ids=[1], status=0))
    await s.set_available(BatchSetAvailable(ids=[1], status=1))


async def test_menu_detail_missing_and_parent(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.menu.service as mod
    class M:
        def __init__(self, *a): pass
        async def get(self, **kw):
            if kw.get("id") == 2: return None
            return SimpleNamespace(id=1, name="n", type=1, order=1, title="n", status=0, parent_id=2)
    monkeypatch.setattr(mod, "MenuCRUD", M)
    s = MenuService.__new__(MenuService); s.auth = object(); s.db = object()
    with pytest.raises(CustomException, match="不存在"):
        await s.detail(2)
