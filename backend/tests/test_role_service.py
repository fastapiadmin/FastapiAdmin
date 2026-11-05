"""角色服务 CRUD/导出分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.role.schema import RoleCreateSchema, RoleUpdateSchema
from app.modules.system.role.service import RoleService


def _svc(monkeypatch, crud):
    import app.modules.system.role.service as mod
    monkeypatch.setattr(mod, "RoleCRUD", crud)
    s = RoleService.__new__(RoleService); s.auth = object(); s.db = object()
    return s


class C:
    def __init__(self, name=None, code=None, id=1): self.name = name; self.code = code; self.id = id
    def __call__(self, *a): return self
    async def get(self, **kw):
        if "name" in kw: return self.name
        if "code" in kw: return self.code
        return None
    async def get_or_404(self, **kw): return self
    async def create(self, data): return self
    async def update(self, **kw): return self
    async def delete(self, ids): self.deleted = ids
    async def get_list(self, **kw): return [self]
    async def set(self, **kw): return None


async def test_role_create_update_delete(monkeypatch: pytest.MonkeyPatch) -> None:
    c = C(); s = _svc(monkeypatch, c)
    async def detail(id): return "ok"
    s.detail = detail
    assert await s.create(RoleCreateSchema(name="r", code="r1")) == "ok"
    c.name = C(); c.code = C()
    with pytest.raises(CustomException, match="已存在"):
        await s.create(RoleCreateSchema(name="r", code="r1"))
    c.name = None; c.code = None
    assert await s.update(1, RoleUpdateSchema(name="r", code="r1")) == "ok"
    with pytest.raises(CustomException, match="不能为空"):
        await s.delete([])
    with pytest.raises(CustomException, match="部分ID"):
        await s.delete([1, 2])
    await s.delete([1])


async def test_role_set_available_and_export(monkeypatch: pytest.MonkeyPatch) -> None:
    c = C(); s = _svc(monkeypatch, c)
    async def get_list(**kw): return [SimpleNamespace(id=1)]
    c.get_list = get_list
    await s.set_available(__import__("app.core.base_schema", fromlist=["BatchSetAvailable"]).BatchSetAvailable(ids=[1], status=0))
    with pytest.raises(CustomException, match="不存在"):
        await s.set_available(__import__("app.core.base_schema", fromlist=["BatchSetAvailable"]).BatchSetAvailable(ids=[1, 2], status=0))
    data = await RoleService.export_list([{"id": 1, "name": "r", "status": 0, "data_scope": 3}])
    assert len(data) > 100


async def test_role_load_set_permission(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.role.service as mod
    roles = [SimpleNamespace(id=1, menus=[], depts=[])]
    class R:
        def __init__(self, *a): pass
        async def get_list(self, **kw): return roles
        async def set(self, **kw): self.set_data = kw
        async def set_role_menus_crud(self, **kw): self.menus = kw
        async def set_role_depts_crud(self, **kw): self.depts = kw
    class M:
        def __init__(self, *a): pass
        async def get_list(self, **kw): return [SimpleNamespace(id=1)]
    class D:
        def __init__(self, *a): pass
        async def get_list(self, **kw): return [SimpleNamespace(id=1)]
    monkeypatch.setattr(mod, "RoleCRUD", R)
    monkeypatch.setattr(mod, "MenuCRUD", M)
    monkeypatch.setattr(mod, "DeptCRUD", D)
    s = RoleService.__new__(RoleService); s.auth = object(); s.db = object()
    await s.set_permission(type("P", (), {"role_ids": [1], "menu_ids": [1], "data_scope": 2})())
    with pytest.raises(CustomException, match="不能为空"):
        await s._load_roles([], [])
    class R2(R):
        async def get_list(self, **kw): return []
    monkeypatch.setattr(mod, "RoleCRUD", R2)
    with pytest.raises(CustomException, match="不存在"):
        await s._load_roles([1], [])
