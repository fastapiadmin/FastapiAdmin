"""微信小程序辅助逻辑/错误映射。"""

from __future__ import annotations

import pytest

from app.core.exceptions import CustomException
from app.modules.system.auth import wx_mini_service as wx


def test_credentials_and_username(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_ID", "id")
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_SECRET", "sec")
    assert wx._require_mini_credentials() == ("id", "sec")
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_SECRET", "")
    with pytest.raises(CustomException, match="未配置"):
        wx._require_mini_credentials()
    name = wx._username_for_wx_mini("OPENID_12345678901234567890")
    assert name.startswith("wxmini_")
    assert wx.extract_openid_from_username(name) == name[7:]
    assert wx.extract_openid_from_username("other") is None
    assert wx.extract_openid_from_username("") is None


def test_check_wx_error() -> None:
    wx._check_wx_error({"errcode": 0}, "x")
    wx._check_wx_error({}, "x")
    with pytest.raises(CustomException, match="失败"):
        wx._check_wx_error({"errcode": 40013, "errmsg": "bad"}, "登录")


async def test_code2session(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_ID", "id")
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_SECRET", "sec")
    async def http(method, url, **kw): return {"openid": "o", "session_key": "s", "unionid": "u"}
    monkeypatch.setattr(wx, "_http_json", http)
    assert await wx.code2session("c") == {"openid": "o", "session_key": "s", "unionid": "u"}
    async def incomplete(method, url, **kw): return {"openid": "o"}
    monkeypatch.setattr(wx, "_http_json", incomplete)
    with pytest.raises(CustomException, match="不完整"):
        await wx.code2session("c")


async def test_access_token_cache_and_fetch(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.redis_crud import RedisCURD
    async def cached(_key): return b"cached"
    monkeypatch.setattr(RedisCURD, "get", staticmethod(cached))
    assert await wx._get_access_token(object()) == "cached"
    async def none(_key): return None
    monkeypatch.setattr(RedisCURD, "get", staticmethod(none))
    async def set_(key, value, expire=None): return True
    monkeypatch.setattr(RedisCURD, "set", staticmethod(set_))
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_ID", "id")
    monkeypatch.setattr(wx.settings, "WX_MINI_APP_SECRET", "sec")
    async def http(method, url, **kw): return {"access_token": "tok"}
    monkeypatch.setattr(wx, "_http_json", http)
    assert await wx._get_access_token(object()) == "tok"
    async def bad(method, url, **kw): return {"errcode": 40013, "errmsg": "bad"}
    monkeypatch.setattr(wx, "_http_json", bad)
    with pytest.raises(CustomException, match="access_token"):
        await wx._get_access_token(object())
