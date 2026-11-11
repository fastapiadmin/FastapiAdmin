"""角色/工单 controller 接口。"""

from __future__ import annotations

import os
import uuid

import pytest
from sqlalchemy import text

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


def _s(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


async def _clean(sql: str, **params) -> None:
    from app.config.setting import settings
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.pool import NullPool
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    try:
        async with e.begin() as c:
            await c.execute(text(sql), params)
    finally:
        await e.dispose()


async def test_role_controller(test_client, auth_headers) -> None:
    code = _s("it_role")
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/role/list")).rsplit("/list", 1)[0]
    try:
        r = test_client.post(f"{base}/create", json={"name": "IT Role", "code": code, "status": 0, "data_scope": 1}, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        rid = r.json()["data"]["id"]
        assert test_client.get(f"{base}/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/detail/{rid}", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/options", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/update/{rid}", json={"name": "IT Role 2", "code": code, "status": 0, "data_scope": 1}, headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/status/batch", json={"ids": [rid], "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/permission", json={"role_id": rid, "menu_ids": []}, headers=auth_headers).status_code in (200, 400)
        assert test_client.request("DELETE", f"{base}/delete", json=[rid], headers=auth_headers).status_code == 200
    finally:
        await _clean("DELETE FROM sys_role WHERE code=:v", v=code)


async def test_ticket_controller(test_client, auth_headers) -> None:
    title = _s("it_ticket")
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/ticket/list")).rsplit("/list", 1)[0]
    try:
        assert test_client.get(f"{base}/stats", headers=auth_headers).status_code == 200
        r = test_client.post(f"{base}/create", json={"title": title}, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        tid = r.json()["data"]["id"]
        assert test_client.get(f"{base}/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/detail/{tid}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/update/{tid}", json={"title": title}, headers=auth_headers).status_code == 200
        c = test_client.post(f"{base}/{tid}/comments", json={"content": "ok"}, headers=auth_headers)
        assert c.status_code in (200, 201), c.text
        assert test_client.get(f"{base}/{tid}/comments", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/batch", json={"ids": [tid], "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/delete", json=[tid], headers=auth_headers).status_code == 200
    finally:
        await _clean("DELETE FROM sys_ticket WHERE title=:v", v=title)


async def test_cache_controller(test_client, auth_headers) -> None:
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/cache/info")).rsplit("/info", 1)[0]
    assert test_client.get(f"{base}/info", headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/get/names", headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/get/keys/system_config", headers=auth_headers).status_code in (200, 400)
    assert test_client.get(f"{base}/get/value/system_config/x", headers=auth_headers).status_code in (200, 400, 404)
    assert test_client.get(f"{base}/redis/keys", params={"pattern": "*", "limit": 5}, headers=auth_headers).status_code in (200, 400)
    assert test_client.get(f"{base}/redis/databases", headers=auth_headers).status_code in (200, 400)
    assert test_client.get(f"{base}/redis/value", params={"key": "missing"}, headers=auth_headers).status_code in (200, 400)
    assert test_client.request("DELETE", f"{base}/delete/key/missing", headers=auth_headers).status_code in (200, 400)
    assert test_client.request("DELETE", f"{base}/delete/name/missing", headers=auth_headers).status_code in (200, 400)
