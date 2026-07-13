"""飞书 OAuth 服务单元测试。mock _http_json,不发真实请求。"""

import pytest

from app.api.v1.module_system.auth import oauth_service
from app.core.exceptions import CustomException


@pytest.fixture(autouse=True)
def _feishu_creds(monkeypatch):
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_APP_ID", "cli_test", raising=False)
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_APP_SECRET", "secret_test", raising=False)
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_API_BASE", "https://open.feishu.cn", raising=False)
    monkeypatch.setattr(oauth_service.settings, "OAUTH_FEISHU_AUTH_BASE", "https://accounts.feishu.cn", raising=False)


def _mock_http_json(monkeypatch, responses):
    """responses: 按调用顺序返回的 dict 列表。"""
    calls = {"i": 0}

    async def fake(method, url, **kwargs):
        idx = calls["i"]
        calls["i"] += 1
        return responses[idx]

    monkeypatch.setattr(oauth_service, "_http_json", fake)
    return calls


async def test_exchange_feishu_token_success(monkeypatch):
    # v2 单步:authen/v2/oauth/token 直接用 client_id+client_secret+code 换,响应扁平
    _mock_http_json(monkeypatch, [
        {"code": 0, "access_token": "u-at-456", "token_type": "Bearer", "expires_in": 7200},
    ])
    token = await oauth_service.exchange_feishu_token(
        "cli_test", "secret_test", "the-code", "https://x.com/cb"
    )
    assert token == "u-at-456"


async def test_exchange_feishu_token_error(monkeypatch):
    # v2 失败:非 0 code + OAuth 风格 error/error_description
    _mock_http_json(monkeypatch, [
        {"code": 20037, "error": "invalid_grant", "error_description": "code expired"},
    ])
    with pytest.raises(CustomException):
        await oauth_service.exchange_feishu_token(
            "cli_test", "secret_test", "the-code", "https://x.com/cb"
        )


async def test_fetch_feishu_profile_prefers_union_id(monkeypatch):
    _mock_http_json(monkeypatch, [
        {"code": 0, "data": {
            "union_id": "on_union_1", "open_id": "ou_open_1", "name": "张三",
            "avatar_url": "https://avatar.feishu.cn/u/on_union_1",
        }},
    ])
    uid, name, avatar = await oauth_service.fetch_feishu_profile("u-at-456")
    assert uid == "on_union_1"
    assert name == "张三"
    assert avatar == "https://avatar.feishu.cn/u/on_union_1"


async def test_fetch_feishu_profile_fallback_open_id(monkeypatch):
    _mock_http_json(monkeypatch, [
        {"code": 0, "data": {"open_id": "ou_open_1", "name": "李四"}},
    ])
    uid, name, avatar = await oauth_service.fetch_feishu_profile("u-at-456")
    assert uid == "ou_open_1"
    assert name == "李四"
    assert avatar == ""


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
    assert url.startswith("https://accounts.feishu.cn/open-apis/authen/v1/authorize?")
    assert "client_id=cli_test" in url
    assert "response_type=code" in url
    assert "state=st-1" in url
    assert "redirect_uri=" in url
