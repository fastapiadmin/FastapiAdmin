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
