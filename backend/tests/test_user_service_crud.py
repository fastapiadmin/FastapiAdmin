"""用户服务创建/更新/删除校验分支（fake CRUD）。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.user.schema import UserCreateSchema, UserUpdateSchema
from app.modules.system.user.service import UserService


def _svc(monkeypatch: pytest.MonkeyPatch, user_crud, dept_crud=None):
    import app.modules.system.user.service as mod
    monkeypatch.setattr(mod, "UserCRUD", user_crud)
    if dept_crud is not None:
        monkeypatch.setattr(mod, "DeptCRUD", dept_crud)
    s = UserService.__new__(UserService)
    s.auth = SimpleNamespace(user=SimpleNamespace(id=99))
    s.db = object()
    return s


def _data(**over):
    base = dict(username="abc", name="A", password="Abc123!x")
    base.update(over)
    return UserCreateSchema(**base)


async def test_create_validation_and_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self, *a): pass
        async def get(self, **kw): return None
        async def create(self, data): return SimpleNamespace(id=1)
    s = _svc(monkeypatch, U)
    async def detail(id): return "ok"
    s.detail = detail
    async def noop(*a, **k): return None
    s._set_user_roles = noop; s._set_user_positions = noop
    assert await s.create(_data()) == "ok"
    with pytest.raises(CustomException, match="超级管理员"):
        await s.create(_data(is_superuser=True))
    class U2(U):
        async def get(self, **kw): return SimpleNamespace(id=2)
    s2 = _svc(monkeypatch, U2); s2.detail = detail; s2._set_user_roles = noop; s2._set_user_positions = noop
    with pytest.raises(CustomException, match="相同用户"):
        await s2.create(_data())
    class U3(U):
        async def get(self, **kw): return None
    class D:
        def __init__(self, *a): pass
        async def get(self, **kw): return None
    s3 = _svc(monkeypatch, U3, D); s3.detail = detail; s3._set_user_roles = noop; s3._set_user_positions = noop
    with pytest.raises(CustomException, match="不存在"):
        await s3.create(_data(dept_id=5))


async def test_update_duplicate_and_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self, *a): pass
        async def get(self, **kw): return SimpleNamespace(id=2)
        async def update(self, **kw): return None
    s = _svc(monkeypatch, U)
    async def detail(id): return "ok"
    s.detail = detail
    async def noop(*a, **k): return None
    s._set_user_roles = noop; s._set_user_positions = noop
    with pytest.raises(CustomException, match="账号已存在"):
        await s.update(1, UserUpdateSchema(username="abc"))
    with pytest.raises(CustomException, match="已存在"):
        await s.update(1, UserUpdateSchema(mobile="13800000000"))
    with pytest.raises(CustomException, match="已存在"):
        await s.update(1, UserUpdateSchema(email="a@b.com"))
    class U2(U):
        async def get(self, **kw): return None
    s2 = _svc(monkeypatch, U2); s2.detail = detail; s2._set_user_roles = noop; s2._set_user_positions = noop
    assert await s2.update(1, UserUpdateSchema(name="B")) == "ok"


async def test_delete_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self, *a): pass
        async def get_list(self, **kw): return [SimpleNamespace(id=1, is_superuser=False)]
        async def delete(self, ids): self.deleted = ids
        async def set_user_roles(self, **kw): return None
        async def set_user_positions(self, **kw): return None
    s = _svc(monkeypatch, U)
    with pytest.raises(CustomException, match="不能为空"):
        await s.delete([])
    with pytest.raises(CustomException, match="不存在"):
        await s.delete([2])
    class U2(U):
        async def get_list(self, **kw): return [SimpleNamespace(id=1, is_superuser=True)]
    s2 = _svc(monkeypatch, U2)
    with pytest.raises(CustomException, match="超级管理员"):
        await s2.delete([1])
    class U3(U):
        async def get_list(self, **kw): return [SimpleNamespace(id=99, is_superuser=False)]
    s3 = _svc(monkeypatch, U3)
    s3.auth.user.id = 99
    with pytest.raises(CustomException, match="当前登陆"):
        await s3.delete([99])


async def test_load_users_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self, *a): pass
        async def get_list(self, **kw): return [SimpleNamespace(id=1)]
    s = _svc(monkeypatch, U)
    with pytest.raises(CustomException, match="不能为空"):
        await s._load_users([], [])
    with pytest.raises(CustomException, match="不存在"):
        await s._load_users([1, 2], [])


async def test_current_info_light_and_update(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.user.schema import CurrentUserUpdateSchema
    class U:
        def __init__(self, *a): pass
        async def get(self, **kw): return None
        async def update(self, **kw): return None
    s = _svc(monkeypatch, U)
    async def menus(): return []
    s._load_menus = menus
    out = await s.current_info(check_data_scope=False)
    assert out.menus == []

    class U2(U):
        async def get(self, **kw): return SimpleNamespace(id=2)
    s2 = _svc(monkeypatch, U2)
    with pytest.raises(CustomException, match="已存在"):
        await s2.update_current_info(CurrentUserUpdateSchema(mobile="13800000000"))


async def test_set_available_protection(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.base_schema import BatchSetAvailable
    class U:
        def __init__(self, *a): pass
        async def get_list(self, **kw): return [SimpleNamespace(id=1, is_superuser=True)]
        async def set(self, **kw): self.set_data = kw
    s = _svc(monkeypatch, U)
    with pytest.raises(CustomException, match="超级管理员"):
        await s.set_available(BatchSetAvailable(ids=[1], status=0))
    class U2(U):
        async def get_list(self, **kw): return [SimpleNamespace(id=1, is_superuser=False)]
    s2 = _svc(monkeypatch, U2)
    await s2.set_available(BatchSetAvailable(ids=[1], status=1))


async def test_load_menus_super_and_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    class M:
        def __init__(self, *a): pass
        async def get_list(self, **kw): return []
    monkeypatch.setattr(mod, "MenuCRUD", M)
    s = _svc(monkeypatch, object)
    s.auth = SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True), menu_ids=[])
    assert await s._load_menus() == []
    s.auth = SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=False), menu_ids=[])
    assert await s._load_menus() == []


async def test_current_info_missing_user(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self, *a): pass
        async def get(self, **kw): return None
    s = _svc(monkeypatch, U)
    async def menus(): return []
    s._load_menus = menus
    with pytest.raises(CustomException, match="不存在"):
        await s.current_info()


async def test_set_user_roles_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    class U:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=1)]
    class R:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=2,status=1)]
    monkeypatch.setattr(mod,"UserCRUD",U); monkeypatch.setattr(mod,"RoleCRUD",R)
    s=UserService.__new__(UserService); s.auth=object(); s.db=object()
    await s._set_user_roles([1],[])
    with pytest.raises(CustomException, match="角色不存在"):
        await s._set_user_roles([1],[3])
    with pytest.raises(CustomException, match="已被禁用"):
        await s._set_user_roles([1],[2])


async def test_set_user_positions_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    class U:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=1)]
    class P:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=2,status=1)]
    monkeypatch.setattr(mod,"UserCRUD",U); monkeypatch.setattr(mod,"PositionCRUD",P)
    s=UserService.__new__(UserService); s.auth=object(); s.db=object()
    await s._set_user_positions([1],[])
    with pytest.raises(CustomException, match="岗位不存在"):
        await s._set_user_positions([1],[3])
    with pytest.raises(CustomException, match="已被禁用"):
        await s._set_user_positions([1],[2])


async def test_set_user_positions_success(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    class U:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=1)]
        async def set_user_positions(self,**kw): self.called=True
    class P:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=2,status=0)]
    monkeypatch.setattr(mod,"UserCRUD",U); monkeypatch.setattr(mod,"PositionCRUD",P)
    s=UserService.__new__(UserService); s.auth=object(); s.db=object()
    await s._set_user_positions([1],[2])


async def test_set_user_roles_success(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    class U:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=1)]
        async def set_user_roles(self,**kw): self.called=True
    class R:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=2,status=0)]
    monkeypatch.setattr(mod,"UserCRUD",U); monkeypatch.setattr(mod,"RoleCRUD",R)
    s=UserService.__new__(UserService); s.auth=object(); s.db=object()
    await s._set_user_roles([1],[2])


async def test_load_users_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=1),SimpleNamespace(id=2)]
    s=_svc(monkeypatch,U)
    assert len(await s._load_users([1,2],[])) == 2


async def test_load_users_duplicate_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return [SimpleNamespace(id=1)]
    s=_svc(monkeypatch,U)
    assert len(await s._load_users([1,1],[])) == 1
