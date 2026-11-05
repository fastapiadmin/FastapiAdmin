"""OAuth 跳转 URL/回调域名/前端重定向工具。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.auth import oauth_service as oauth


def _req(host="example.com", base="https://example.com"):
    return SimpleNamespace(base_url=base + "/", url=SimpleNamespace(hostname=host))


def test_callback_url_host_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(oauth.settings, "OAUTH_ALLOWED_HOSTS", ["example.com"])
    assert oauth._callback_url(_req(), "github") == "https://example.com/system/auth/oauth/github/callback"
    assert oauth._callback_url(_req("sub.example.com"), "github").endswith("/callback")
    with pytest.raises(CustomException, match="非法"):
        oauth._callback_url(_req("evil.com"), "github")
    monkeypatch.setattr(oauth.settings, "OAUTH_ALLOWED_HOSTS", [])
    assert oauth._callback_url(_req("evil.com"), "github")


def test_frontend_redirects() -> None:
    e = oauth._frontend_error_redirect("https://f/cb", "bad msg")
    assert "oauth_error=bad%20msg" in e
    s = oauth._frontend_success_redirect("https://f/cb", "a", "r", "bearer")
    assert "access_token=a" in s and "refresh_token=r" in s
    s2 = oauth._frontend_success_redirect("https://f/cb?x=1", "a", "r", "bearer")
    assert "&access_token=a" in s2


def test_require_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(oauth.settings, "OAUTH_GITHUB_CLIENT_ID", "id")
    monkeypatch.setattr(oauth.settings, "OAUTH_GITHUB_CLIENT_SECRET", "sec")
    assert oauth._require_credentials("github") == ("id", "sec")
    monkeypatch.setattr(oauth.settings, "OAUTH_GITHUB_CLIENT_SECRET", "")
    with pytest.raises(RuntimeError):
        oauth._require_credentials("github")
    with pytest.raises(CustomException):
        oauth._require_credentials("unknown")


def test_build_authorize_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(oauth.settings, "OAUTH_GITHUB_CLIENT_ID", "gid")
    monkeypatch.setattr(oauth.settings, "OAUTH_GITHUB_CLIENT_SECRET", "gsec")
    monkeypatch.setattr(oauth.settings, "OAUTH_GITEE_CLIENT_ID", "eid")
    monkeypatch.setattr(oauth.settings, "OAUTH_GITEE_CLIENT_SECRET", "esec")
    monkeypatch.setattr(oauth.settings, "OAUTH_WECHAT_OPEN_APP_ID", "wid")
    monkeypatch.setattr(oauth.settings, "OAUTH_WECHAT_OPEN_APP_SECRET", "wsec")
    monkeypatch.setattr(oauth.settings, "OAUTH_QQ_APP_ID", "qid")
    monkeypatch.setattr(oauth.settings, "OAUTH_QQ_APP_SECRET", "qsec")
    cb = "https://x/cb"
    assert oauth.build_authorize_url(provider="github", callback_url=cb, state="s").startswith("https://github.com/")
    assert oauth.build_authorize_url(provider="gitee", callback_url=cb, state="s").startswith("https://gitee.com/")
    assert "open.weixin.qq.com" in oauth.build_authorize_url(provider="wechat", callback_url=cb, state="s")
    assert "graph.qq.com" in oauth.build_authorize_url(provider="qq", callback_url=cb, state="s")
    with pytest.raises(CustomException):
        oauth.build_authorize_url(provider="unknown", callback_url=cb, state="s")


async def test_http_json(monkeypatch: pytest.MonkeyPatch) -> None:
    class R:
        def __init__(self, bad=False): self.bad=bad; self.text="x"
        def raise_for_status(self): pass
        def json(self):
            if self.bad: raise ValueError()
            return {"ok": 1}
    class C:
        def __init__(self, r): self.r=r
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def request(self, *a, **k): return self.r
    class H:
        AsyncClient = lambda *a, **k: C(R())
    monkeypatch.setattr(oauth, "httpx", H)
    assert await oauth._http_json("GET", "http://x") == {"ok": 1}
