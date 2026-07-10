"""飞书 OAuth 服务单元测试。mock _http_json,不发真实请求。"""

import pytest

from app.api.v1.module_system.auth import oauth_service
from app.core.exceptions import CustomException


@pytest.fixture(autouse=True)
def _feishu_creds(monkeypatch):
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_APP_ID", "cli_test", raising=False)
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_APP_SECRET", "secret_test", raising=False)
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_API_BASE", "https://open.feishu.cn", raising=False)


def _mock_http_json(monkeypatch, responses):
    """responses: 按调用顺序返回的 dict 列表。"""
    calls = {"i": 0}

    async def fake(method, url, **kwargs):
        idx = calls["i"]
        calls["i"] += 1
        return responses[idx]

    monkeypatch.setattr(oauth_service, "_http_json", fake)
    return calls


async def test_fetch_app_access_token_success(monkeypatch):
    _mock_http_json(monkeypatch, [{"code": 0, "app_access_token": "a-at-123"}])
    token = await oauth_service.fetch_feishu_app_access_token()
    assert token == "a-at-123"


async def test_fetch_app_access_token_error_code(monkeypatch):
    _mock_http_json(monkeypatch, [{"code": 10003, "msg": "invalid app_secret"}])
    with pytest.raises(CustomException):
        await oauth_service.fetch_feishu_app_access_token()


async def test_exchange_feishu_token_success(monkeypatch):
    # 第 1 次调用:app_access_token;第 2 次:oidc/access_token
    _mock_http_json(monkeypatch, [
        {"code": 0, "app_access_token": "a-at-123"},
        {"code": 0, "data": {"access_token": "u-at-456"}},
    ])
    token = await oauth_service.exchange_feishu_token("the-code")
    assert token == "u-at-456"


async def test_exchange_feishu_token_error(monkeypatch):
    _mock_http_json(monkeypatch, [
        {"code": 0, "app_access_token": "a-at-123"},
        {"code": 20037, "msg": "code expired"},
    ])
    with pytest.raises(CustomException):
        await oauth_service.exchange_feishu_token("the-code")


async def test_fetch_feishu_profile_prefers_union_id(monkeypatch):
    _mock_http_json(monkeypatch, [
        {"code": 0, "data": {"union_id": "on_union_1", "open_id": "ou_open_1", "name": "张三"}},
    ])
    uid, name = await oauth_service.fetch_feishu_profile("u-at-456")
    assert uid == "on_union_1"
    assert name == "张三"


async def test_fetch_feishu_profile_fallback_open_id(monkeypatch):
    _mock_http_json(monkeypatch, [
        {"code": 0, "data": {"open_id": "ou_open_1", "name": "李四"}},
    ])
    uid, name = await oauth_service.fetch_feishu_profile("u-at-456")
    assert uid == "ou_open_1"
    assert name == "李四"


async def test_fetch_feishu_profile_error(monkeypatch):
    _mock_http_json(monkeypatch, [{"code": 99991663, "msg": "token invalid"}])
    with pytest.raises(CustomException):
        await oauth_service.fetch_feishu_profile("bad")


def test_build_authorize_url_feishu():
    url = oauth_service.build_authorize_url(
        provider="feishu",
        callback_url="https://x.com/api/v1/system/auth/oauth/feishu/callback",
        state="st-1",
    )
    assert url.startswith("https://open.feishu.cn/open-apis/authen/v1/authorize?")
    assert "app_id=cli_test" in url
    assert "state=st-1" in url
    assert "redirect_uri=" in url
