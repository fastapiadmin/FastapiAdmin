"""微信小程序服务外部边界（无真实微信服务时 mock HTTP）。"""

from __future__ import annotations

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
