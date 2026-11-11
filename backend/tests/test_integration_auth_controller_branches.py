"""认证 controller 成功/失败返回分支。"""

from __future__ import annotations

import os
from unittest.mock import AsyncMock

import pytest
from app.core.base_schema import JWTOutSchema

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


def _login_out():
    from app.modules.system.auth.schema import LoginOutSchema
    return LoginOutSchema(access_token="a", refresh_token="r", token_type="Bearer", expires_in=1)


async def test_auth_controller_success_paths(test_client, auth_headers, monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.auth.controller as c
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/auth/login")).rsplit("/login", 1)[0]
    # docs referer -> 直接返回 login_result
    r = test_client.post(f"{base}/login", data={"username": "admin", "password": "admin123"}, headers={"referer": "http://x/docs"})
    assert r.status_code == 200 and "access_token" in r.json()
    # slider 成功分支
    monkeypatch.setattr(c.CaptchaService, "slider_complete", AsyncMock(return_value={"captcha_key": "k", "verified": True}))
    assert test_client.post(f"{base}/captcha/slider/complete", json={"captcha_key": "k"}, headers=auth_headers).status_code == 200
    # 微信登录/手机号/二维码成功分支
    monkeypatch.setattr(c, "wx_mini_login", AsyncMock(return_value=_login_out()))
    monkeypatch.setattr(c, "wx_mini_phone_login", AsyncMock(return_value=_login_out()))
    monkeypatch.setattr(c, "get_qrcode", AsyncMock(return_value=b"png"))
    assert test_client.post(f"{base}/wx-login", json={"code": "c"}, headers=auth_headers).status_code == 200
    assert test_client.post(f"{base}/wx-phone-login", json={"code": "c"}, headers=auth_headers).status_code == 200
    q = test_client.post(f"{base}/wx-qrcode/generate", json={"scene": "s"}, headers=auth_headers)
    assert q.status_code == 200 and q.json()["data"]["url"].startswith("data:image/png")
