"""用户改密/重置/忘记密码/注册分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.user.schema import ResetPasswordSchema, UserChangePasswordSchema, UserForgetPasswordSchema, UserRegisterSchema
from app.modules.system.user.service import UserService


def _svc(monkeypatch, crud):
    import app.modules.system.user.service as mod
    monkeypatch.setattr(mod, "UserCRUD", crud)
    s = UserService.__new__(UserService)
    s.auth = SimpleNamespace(user=SimpleNamespace(id=1))
    s.db = object()
    return s


async def test_change_password(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self, *a): pass
        async def get_or_404(self, **kw): return SimpleNamespace(id=1, password="old")
        async def change_password(self, **kw): self.changed = kw
    s = _svc(monkeypatch, U)
    async def detail(id): return "ok"
    s.detail = detail
    import app.modules.system.user.service as mod
    async def verify(plain_password, password_hash): return plain_password == "rightpass"
    monkeypatch.setattr(mod.PwdUtil, "averify_password", staticmethod(verify))
    async def hash_pwd(password): return "Hashed123!x"
    monkeypatch.setattr(mod.PwdUtil, "ahash_password", staticmethod(hash_pwd))
    with pytest.raises(CustomException, match="原密码"):
        await s.change_password(UserChangePasswordSchema(old_password="wrongpass", new_password="Abc123!x"))
    assert await s.change_password(UserChangePasswordSchema(old_password="rightpass", new_password="Abc123!x")) == "ok"


async def test_reset_and_forget_password(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self, *a): pass
        async def get_or_404(self, **kw): return SimpleNamespace(id=2, is_superuser=False)
        async def change_password(self, **kw): self.changed = kw
        async def get(self, **kw): return None
    s = _svc(monkeypatch, U)
    async def detail(id): return "ok"
    s.detail = detail
    import app.modules.system.user.service as mod
    async def hash_pwd(password): return "Hashed123!x"
    monkeypatch.setattr(mod.PwdUtil, "ahash_password", staticmethod(hash_pwd))
    assert await s.reset_password(ResetPasswordSchema(id=2, password="Abc123!x")) == "ok"
    assert await s.forget_password(UserForgetPasswordSchema(username="abc")) is None
    class U2(U):
        async def get_or_404(self, **kw): return SimpleNamespace(id=2, is_superuser=True)
    s2 = _svc(monkeypatch, U2)
    with pytest.raises(CustomException, match="超级管理员"):
        await s2.reset_password(ResetPasswordSchema(id=2, password="Abc123!x"))


async def test_register(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self, *a): pass
        async def get(self, **kw): return None
        async def create(self, data): return SimpleNamespace(id=1)
        async def set(self, *a, **kw): return None
    s = _svc(monkeypatch, U)
    async def detail(id): return "ok"
    s.detail = detail
    import app.modules.system.user.service as mod
    async def hash_pwd(password): return "Hashed123!x"
    monkeypatch.setattr(mod.PwdUtil, "ahash_password", staticmethod(hash_pwd))
    assert await s.register(UserRegisterSchema(username="abc", password="Abc123!x", name="A")) == "ok"
    class U2(U):
        async def get(self, **kw): return SimpleNamespace(id=2)
    s2 = _svc(monkeypatch, U2)
    with pytest.raises(CustomException, match="相同用户"):
        await s2.register(UserRegisterSchema(username="abc", password="Abc123!x", name="A"))


async def test_register_create_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    class U:
        def __init__(self,*a): pass
        async def get(self,**kw): return None
        async def create(self,data): return None
    monkeypatch.setattr(mod,"UserCRUD",U)
    class P:
        @staticmethod
        async def ahash_password(password): return "Hashed123!x"
    monkeypatch.setattr(mod,"PwdUtil",P)
    s=UserService.__new__(UserService); s.auth=object(); s.db=object()
    with pytest.raises(CustomException, match="注册失败"):
        await s.register(UserRegisterSchema(username="abc",password="Abc123!x",name="A"))
