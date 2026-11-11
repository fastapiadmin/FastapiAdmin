"""微信小程序服务外部边界（无真实微信服务时 mock HTTP）。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import CustomException
from app.modules.system.auth import wx_mini_service as wx


def test_check_wx_error() -> None:
    wx._check_wx_error({}, "登录")
    wx._check_wx_error({"errcode": 0}, "登录")
    with pytest.raises(CustomException, match="登录失败"):
        wx._check_wx_error({"errcode": 40013, "errmsg": "bad"}, "登录")


async def test_code2session(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wx, "_require_mini_credentials", lambda: ("id", "secret"))
    async def ok(method, url, **kw): return {"openid": "o", "session_key": "s", "unionid": "u"}
    monkeypatch.setattr(wx, "_http_json", ok)
    assert await wx.code2session("c") == {"openid": "o", "session_key": "s", "unionid": "u"}
    async def incomplete(method, url, **kw): return {"openid": "o"}
    monkeypatch.setattr(wx, "_http_json", incomplete)
    with pytest.raises(CustomException, match="不完整"):
        await wx.code2session("c")


async def test_get_phone(monkeypatch: pytest.MonkeyPatch) -> None:
    async def token(redis): return "t"
    async def ok(method, url, **kw): return {"phone_info": {"phoneNumber": "13800138000"}}
    monkeypatch.setattr(wx, "_get_access_token", token); monkeypatch.setattr(wx, "_http_json", ok)
    assert await wx.get_phone_number(object(), "c") == "13800138000"
    async def empty(method, url, **kw): return {"phone_info": {}}
    monkeypatch.setattr(wx, "_http_json", empty)
    with pytest.raises(CustomException, match="手机号为空"):
        await wx.get_phone_number(object(), "c")


def test_username_helpers() -> None:
    name = wx._username_for_wx_mini("openid1234567890abcdef")
    assert name.startswith("wxmini_")
    assert wx.extract_openid_from_username(name) == "openid1234567890abcdef"[:20]
    assert wx.extract_openid_from_username("normal_user") is None


async def test_ensure_wx_user_existing(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    class U:
        def __init__(self,*a): pass
        async def get(self,**kw): return SimpleNamespace(mobile=None,name="old",avatar=None)
    class DB:
        def __init__(self): self.flushed=False
        async def flush(self): self.flushed=True
    monkeypatch.setattr(wx,"UserCRUD",U)
    db=DB()
    user=await wx.ensure_wx_user(db=db,openid="openid123",nickname="new",mobile="13800000000",avatar="a")
    assert user.name=="new" and user.mobile=="13800000000" and db.flushed


async def test_ensure_wx_user_new(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self,*a): pass
        async def get(self,**kw): return None
    async def auto(**kw): return "new-user"
    monkeypatch.setattr(wx,"UserCRUD",U); monkeypatch.setattr(wx,"auto_register_login_user",auto)
    assert await wx.ensure_wx_user(db=object(),openid="openid123")=="new-user"


async def test_qrcode(monkeypatch: pytest.MonkeyPatch) -> None:
    async def token(redis): return "t"
    monkeypatch.setattr(wx,"_get_access_token",token)
    class R:
        def __init__(self,ct="image/png",data=b"png",bad=False): self.headers={"content-type":ct}; self.content=data; self._bad=bad
        def raise_for_status(self): return None
        def json(self):
            if self._bad: raise wx.json.JSONDecodeError("x","x",0)
            return {"errcode":40013,"errmsg":"bad"}
    class C:
        def __init__(self,r): self.r=r
        async def __aenter__(self): return self
        async def __aexit__(self,*a): return False
        async def post(self,*a,**k): return self.r
    def H(r): return type("H",(),{"AsyncClient":lambda *a,**k:C(r)})
    monkeypatch.setattr(wx,"httpx",H(R()))
    assert await wx.get_qrcode(object(),"s")==b"png"
    monkeypatch.setattr(wx,"httpx",H(R("application/json")))
    with pytest.raises(CustomException, match="生成小程序码失败"):
        await wx.get_qrcode(object(),"s")


async def test_subscribe_skip_and_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_ID", "")
    assert await wx.send_subscribe_message(object(), openid="o", template_id="t") is False
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_ID", "id")
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_SECRET", "s")
    assert await wx.send_subscribe_message(object(), openid="o", template_id="") is False
    assert await wx.send_subscribe_message(object(), openid="", template_id="t") is False
    async def token(redis): return "tok"
    async def not_sub(method, url, **kw): return {"errcode": 43101}
    monkeypatch.setattr(wx, "_get_access_token", token); monkeypatch.setattr(wx, "_http_json", not_sub)
    assert await wx.send_subscribe_message(object(), openid="o", template_id="t") is False
    async def bad(method, url, **kw): raise RuntimeError("x")
    monkeypatch.setattr(wx, "_http_json", bad)
    assert await wx.send_subscribe_message(object(), openid="o", template_id="t") is False
    async def ok(method, url, **kw): return {"errcode": 0}
    monkeypatch.setattr(wx, "_http_json", ok)
    assert await wx.send_subscribe_message(object(), openid="o", template_id="t", page="p") is True


async def test_wx_login_orchestration(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    async def code2(**kw): return {"openid": "o", "session_key": "s"}
    async def user(**kw): return SimpleNamespace(username="u", id=1, name="N", avatar=None, is_superuser=False)
    async def token(**kw): return SimpleNamespace(access_token="a", refresh_token="r", expires_in=1, token_type="Bearer")
    monkeypatch.setattr(wx, "code2session", code2)
    monkeypatch.setattr(wx, "get_wx_login_user", user)
    monkeypatch.setattr(wx.LoginService, "create_token", staticmethod(token))
    monkeypatch.setattr(wx.LoginService, "build_login_out", staticmethod(lambda **k: SimpleNamespace(access_token="a")))
    out = await wx.wx_mini_login(request=None, redis=None, db=None, code="c")
    assert out.access_token == "a"
    async def phone(redis, code): return "13800138000"
    async def puser(*, db, phone): return SimpleNamespace(username="u2", id=2, name="N2", avatar=None, is_superuser=False, mobile=phone)
    monkeypatch.setattr(wx, "get_phone_number", phone)
    monkeypatch.setattr(wx, "get_wx_phone_login_user", puser)
    out2 = await wx.wx_mini_phone_login(request=None, redis=None, db=None, code="c")
    assert out2.access_token == "a"


async def test_http_json_and_phone(monkeypatch: pytest.MonkeyPatch) -> None:
    class Resp:
        text = "bad"
        headers = {"content-type": "application/json"}
        content = b"x"
        def raise_for_status(self): pass
        def json(self): raise json.JSONDecodeError("x", "bad", 0)
    class Client:
        def __init__(self, **k): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def request(self, *a, **k): return Resp()
        async def post(self, *a, **k): return Resp()
    monkeypatch.setattr(wx.httpx, "AsyncClient", Client)
    with pytest.raises(Exception):
        await wx._http_json("GET", "http://x")
    monkeypatch.setattr(wx, "_get_access_token", AsyncMock(return_value="t"))
    with pytest.raises(Exception):
        await wx.generate_wxacodeunlimit(redis=None, scene="s", page="p")
    async def prepare(db, user): return user
    monkeypatch.setattr(wx.LoginService, "prepare_user_for_login", prepare)
    monkeypatch.setattr(wx, "auto_register_login_user", AsyncMock(return_value=SimpleNamespace(id=1)))
    class C:
        def __init__(self, *a): pass
        async def get(self, **k): return None
    monkeypatch.setattr(wx, "UserCRUD", C)
    assert await wx.get_wx_phone_login_user(db=None, phone="13800138000") is not None


async def test_wx_http_and_qr_edges(monkeypatch) -> None:
    import json as _json
    class Resp:
        text = "bad"; content = b"x"; headers = {"content-type": "application/json"}
        def raise_for_status(self): pass
        def json(self): raise _json.JSONDecodeError("x", "bad", 0)
    class Client:
        def __init__(self, **k): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def request(self, *a, **k): return Resp()
        async def post(self, *a, **k): return Resp()
    monkeypatch.setattr(wx.httpx, "AsyncClient", Client)
    with pytest.raises(Exception):
        await wx._http_json("GET", "http://x")
    monkeypatch.setattr(wx, "_get_access_token", AsyncMock(return_value="t"))
    with pytest.raises(CustomException):
        await wx.get_qrcode(redis=None, scene="s", page="p")


async def test_wx_login_user_and_subscribe(monkeypatch) -> None:
    async def ensure(**k): return SimpleNamespace(id=1)
    async def prep(**k): return SimpleNamespace(id=1)
    monkeypatch.setattr(wx, "ensure_wx_user", ensure)
    monkeypatch.setattr(wx.LoginService, "prepare_user_for_login", staticmethod(prep))
    assert await wx.get_wx_login_user(db=None, openid="o") is not None
    async def http(*a, **k): return {"errcode": 1, "errmsg": "bad"}
    monkeypatch.setattr(wx, "_http_json", http)
    assert await wx.send_subscribe_message(redis=None, openid="o", template_id="t", data={}) is False
