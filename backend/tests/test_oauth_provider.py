"""OAuth 提供方令牌/用户信息映射。"""

from __future__ import annotations

import pytest

from app.core.exceptions import CustomException
from app.modules.system.auth import oauth_service as o


async def test_exchange_tokens(monkeypatch: pytest.MonkeyPatch) -> None:
    async def gh(method, url, **kw): return {"access_token": "g"}
    monkeypatch.setattr(o, "_http_json", gh)
    assert await o.exchange_github_token("i", "s", "c", "r") == "g"
    async def gitee(method, url, **kw): return {"access_token": "e"}
    monkeypatch.setattr(o, "_http_json", gitee)
    assert await o.exchange_gitee_token("i", "s", "c", "r") == "e"
    async def wechat(method, url, **kw): return {"access_token": "w", "openid": "oid"}
    monkeypatch.setattr(o, "_http_json", wechat)
    assert await o.exchange_wechat_token("i", "s", "c") == ("w", "oid")
    async def text(method, url, **kw): return "access_token=q&x=1"
    async def me(method, url, **kw): return {"openid": "qid"}
    monkeypatch.setattr(o, "_http_text", text); monkeypatch.setattr(o, "_http_json", me)
    assert await o.exchange_qq_token("i", "s", "c", "r") == ("q", "qid")


async def test_exchange_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    async def bad(method, url, **kw): return []
    monkeypatch.setattr(o, "_http_json", bad)
    with pytest.raises(CustomException): await o.exchange_gitee_token("i", "s", "c", "r")
    async def no_token(method, url, **kw): return {}
    monkeypatch.setattr(o, "_http_json", no_token)
    with pytest.raises(CustomException): await o.exchange_wechat_token("i", "s", "c")
    async def text(method, url, **kw): return "x=1"
    monkeypatch.setattr(o, "_http_text", text)
    with pytest.raises(CustomException): await o.exchange_qq_token("i", "s", "c", "r")


async def test_profiles(monkeypatch: pytest.MonkeyPatch) -> None:
    async def gh(method, url, **kw):
        if url.endswith("/emails"): return [{"primary": True, "email": "e@x"}]
        return {"login": "l", "name": "N"}
    monkeypatch.setattr(o, "_http_json", gh)
    assert await o.fetch_github_profile("t") == ("l", "N", "e@x")
    async def gitee(method, url, **kw): return {"login": "l", "email": "e"}
    monkeypatch.setattr(o, "_http_json", gitee)
    assert await o.fetch_gitee_profile("t") == ("l", "l", "e")
    async def wx(method, url, **kw): return {"nickname": "W", "unionid": "u"}
    monkeypatch.setattr(o, "_http_json", wx)
    assert await o.fetch_wechat_profile("t", "o") == ("u", "W")
    async def qq(method, url, **kw): return {"ret": 0, "nickname": "Q"}
    monkeypatch.setattr(o, "_http_json", qq)
    assert await o.fetch_qq_profile("t", "a", "o") == ("o", "Q")


async def test_profile_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    async def bad(method, url, **kw): return []
    monkeypatch.setattr(o, "_http_json", bad)
    for fn in (o.fetch_github_profile, o.fetch_gitee_profile):
        with pytest.raises(CustomException): await fn("t")
    with pytest.raises(CustomException): await o.fetch_wechat_profile("t", "o")
    async def qq(method, url, **kw): return {"ret": 1, "msg": "bad"}
    monkeypatch.setattr(o, "_http_json", qq)
    with pytest.raises(CustomException): await o.fetch_qq_profile("t", "a", "o")
