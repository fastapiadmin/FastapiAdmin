"""登录前用户可用性准备。"""

from __future__ import annotations

from types import SimpleNamespace

import json

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


async def test_auto_register_exception_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.auth.service as mod
    class S:
        def __init__(self,*a): pass
        async def create(self,**k): raise RuntimeError("x")
    class Existing:
        def __init__(self,*a): pass
        async def get(self,**k): return SimpleNamespace(id=1)
    monkeypatch.setattr(mod, "UserService", S); monkeypatch.setattr(mod, "UserCRUD", Existing)
    assert (await mod.auto_register_login_user(db=object(), username="user_1", display_name="N", fail_msg="f")).id == 1
    class NoneC(Existing):
        async def get(self,**k): return None
    monkeypatch.setattr(mod, "UserCRUD", NoneC)
    with pytest.raises(RuntimeError):
        await mod.auto_register_login_user(db=object(), username="user_1", display_name="N", fail_msg="f")


async def test_captcha_missing_and_bad(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.auth.service as mod
    monkeypatch.setattr(mod.settings, "CAPTCHA_ENABLE", True)
    form = SimpleNamespace(captcha_key=None, login_type=1, username="user_1")
    with pytest.raises(CustomException):
        await mod.LoginService.authenticate_user(SimpleNamespace(headers={}, client=None, method="POST", url=SimpleNamespace(path="/")), None, form, None)
    form2 = SimpleNamespace(captcha_key="k", login_type=1, username="user_1")
    class Cap:
        @staticmethod
        async def check_captcha(**k): raise CustomException(msg="bad")
    monkeypatch.setattr(mod, "CaptchaService", Cap)
    from unittest.mock import AsyncMock
    monkeypatch.setattr(mod.LoginService, "_check_login_rate_limit", AsyncMock())
    monkeypatch.setattr(mod.IpLocalUtil, "resolve_location", AsyncMock(return_value="x"))
    with pytest.raises(CustomException):
        await mod.LoginService.authenticate_user(SimpleNamespace(headers={}, client=None, method="POST", url=SimpleNamespace(path="/")), None, form2, None)


def test_login_service_init() -> None:
    from app.modules.system.auth.service import LoginService
    obj = LoginService(object(), object())
    assert obj.auth is not None and obj.db is not None


async def test_prepare_user_none(monkeypatch) -> None:
    import app.modules.system.auth.service as mod
    class C:
        def __init__(self,*a): pass
        async def update_last_login(self, **k): return None
    monkeypatch.setattr(mod, "UserCRUD", C)
    with pytest.raises(CustomException):
        await mod.LoginService.prepare_user_for_login(None, SimpleNamespace(status=0, id=1))


async def test_refresh_token_edges(monkeypatch) -> None:
    import app.modules.system.auth.service as mod
    payload = SimpleNamespace(is_refresh=True, sub="s")
    monkeypatch.setattr(mod, "decode_access_token", lambda *a, **k: payload)
    class R:
        def __init__(self,*a): pass
        async def get(self, key):
            return json.dumps({"session_id": "s", "user_id": 1}) if "session" in key and "refresh" not in key else b"refresh"
        async def delete(self, *a): pass
    class U:
        def __init__(self,*a): pass
        async def get(self, **k): return None
    monkeypatch.setattr(mod, "RedisCURD", R); monkeypatch.setattr(mod, "UserCRUD", U)
    with pytest.raises(CustomException):
        await mod.LoginService.refresh_token(None, None, "refresh")
    class R2(R):
        async def get(self, key):
            return json.dumps({"session_id": "s"}) if "session" in key and "refresh" not in key else b"refresh"
    monkeypatch.setattr(mod, "RedisCURD", R2)
    with pytest.raises(CustomException):
        await mod.LoginService.refresh_token(None, None, "refresh")


async def test_prepare_refresh_none(monkeypatch) -> None:
    import app.modules.system.auth.service as mod
    class C:
        def __init__(self,*a): pass
        async def update_last_login(self, **k): return None
    monkeypatch.setattr(mod, "UserCRUD", C)
    with pytest.raises(CustomException):
        await mod.LoginService.prepare_user_for_login(None, SimpleNamespace(status=0, id=1))


async def test_captcha_states(monkeypatch) -> None:
    import app.modules.system.auth.service as mod
    class Cap(mod.CaptchaService):
        PENDING = 0; VERIFIED = 1
        @staticmethod
        async def _read_state(**k): return {"status": 9, "target_x": 0, "issued_at": 0, "fingerprint": "f"}
    monkeypatch.setattr(mod, "CaptchaService", Cap)
    with pytest.raises(CustomException):
        await mod.CaptchaService.slider_complete(redis=None, request=None, captcha_key="k", position=0)
    class Cap2(Cap):
        @staticmethod
        async def _read_state(**k): return {"status": 0, "target_x": 0, "issued_at": 0, "fingerprint": "f"}
        @staticmethod
        def _matches(state, request): return False
    monkeypatch.setattr(mod, "CaptchaService", Cap2)
    with pytest.raises(CustomException):
        await Cap2.slider_complete(redis=None, request=None, captcha_key="k", position=0)
