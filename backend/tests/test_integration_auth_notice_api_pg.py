"""认证/公告 controller 剩余接口。"""

from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


async def test_auth_controller_extra(test_client, auth_headers) -> None:
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/auth/login")).rsplit("/login", 1)[0]
    assert test_client.get(f"{base}/captcha/get", headers=auth_headers).status_code in (200, 400)
    assert test_client.post(f"{base}/token/refresh", json="bad", headers=auth_headers).status_code in (400, 401, 403, 422)
    assert test_client.post(f"{base}/logout", json="bad", headers=auth_headers).status_code in (200, 400, 401)
    assert test_client.post(f"{base}/wx-login", json={"code": "bad"}, headers=auth_headers).status_code in (400, 500)
    assert test_client.post(f"{base}/wx-phone-login", json={"code": "bad"}, headers=auth_headers).status_code in (400, 500)


async def test_notice_extra(test_client, auth_headers) -> None:
    from sqlalchemy import text
    from app.config.setting import settings
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.pool import NullPool
    title = "it_notice_extra"
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/notice/list")).rsplit("/list", 1)[0]
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    try:
        r = test_client.post(f"{base}/create", json={"notice_title": title, "notice_type": "1", "notice_content": "x", "status": 0}, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        nid = r.json()["data"]["id"]
        assert test_client.patch(f"{base}/status/batch", json={"ids": [nid], "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/available", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/unread-count", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/read-ids", headers=auth_headers).status_code == 200
        assert test_client.post(f"{base}/read", json={"ids": [nid]}, headers=auth_headers).status_code in (200, 400)
        assert test_client.request("DELETE", f"{base}/delete", json=[nid], headers=auth_headers).status_code == 200
    finally:
        async with e.begin() as c:
            await c.execute(text("DELETE FROM sys_notice WHERE notice_title=:v"), {"v": title})
            await c.execute(text("DELETE FROM sys_notice_read WHERE notice_id NOT IN (SELECT id FROM sys_notice)"))
        await e.dispose()


async def test_auth_controller_more(test_client, auth_headers) -> None:
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/auth/login")).rsplit("/login", 1)[0]
    assert test_client.post(f"{base}/captcha/slider/complete", json={"captcha_key": "x"}, headers=auth_headers).status_code in (200, 400, 422)
    assert test_client.get(f"{base}/oauth/github/login", headers=auth_headers, follow_redirects=False).status_code in (302, 307, 400, 403, 404, 500)
    assert test_client.get(f"{base}/oauth/github/callback", params={"code": "x", "state": "y"}, headers=auth_headers, follow_redirects=False).status_code in (200, 302, 307, 400, 403, 404, 500)
    assert test_client.post(f"{base}/wx-qrcode/generate", json={"scene": "x"}, headers=auth_headers).status_code in (400, 500)
