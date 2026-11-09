"""登录前用户可用性准备。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.auth.service import LoginService


async def test_prepare_disabled() -> None:
    with pytest.raises(CustomException, match="停用"):
        await LoginService.prepare_user_for_login(db=object(), user=SimpleNamespace(status=1, id=1))


async def test_prepare_missing_after_refresh(monkeypatch) -> None:
    import app.modules.system.auth.service as mod
    class C:
        def __init__(self,*a): pass
        async def update_last_login(self, **k): return None
    monkeypatch.setattr(mod, "UserCRUD", C)
    with pytest.raises(CustomException, match="不存在"):
        await LoginService.prepare_user_for_login(db=object(), user=SimpleNamespace(status=0, id=1))


def test_sanitize_login_name() -> None:
    from app.modules.system.auth.service import sanitize_login_name
    assert sanitize_login_name("a").startswith("a")
    assert sanitize_login_name("1abc").startswith("u")
    assert sanitize_login_name("用户")


async def test_auto_register(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.auth.service as mod
    class U:
        def __init__(self,*a): pass
        async def create(self,**k): return None
        async def get(self,**k): return SimpleNamespace(id=1)
    monkeypatch.setattr(mod, "UserService", U); monkeypatch.setattr(mod, "UserCRUD", U)
    user = await mod.auto_register_login_user(db=object(), username="user_1", display_name="N", fail_msg="注册失败")
    assert user.id == 1
    class U2(U):
        async def get(self,**k): return None
    monkeypatch.setattr(mod, "UserCRUD", U2)
    with pytest.raises(CustomException):
        await mod.auto_register_login_user(db=object(), username="user_1", display_name="N", fail_msg="注册失败")


async def test_write_login_log_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.auth.service as mod
    class C:
        def __init__(self,*a): pass
        async def create(self,**k): raise RuntimeError("x")
    monkeypatch.setattr(mod, "LoginLogCRUD", C)
    assert await mod._write_login_log(username="u", status=1, login_ip="1", login_location="x", request_os="o", request_browser="b", msg="m") is None
