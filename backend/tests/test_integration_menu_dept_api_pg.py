"""菜单/部门 controller 接口。"""

from __future__ import annotations

import os
import uuid

import pytest
from sqlalchemy import text

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


def _n(p): return f"{p}_{uuid.uuid4().hex[:8]}"


async def _clean(sql, **params):
    from app.config.setting import settings
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.pool import NullPool
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    try:
        async with e.begin() as c:
            await c.execute(text(sql), params)
    finally:
        await e.dispose()


async def test_menu_controller(test_client, auth_headers) -> None:
    name = _n("IT菜单")
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/menu/tree")).rsplit("/tree", 1)[0]
    try:
        assert test_client.get(f"{base}/tree", headers=auth_headers).status_code == 200
        r = test_client.post(f"{base}/create", json={"name": name, "type": 1, "order": 999, "route_name": name.replace("IT菜单_","ItMenu"), "route_path": "/it-menu", "redirect": "/it-menu", "title": name}, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        mid = r.json()["data"]["id"]
        assert test_client.get(f"{base}/detail/{mid}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/update/{mid}", json={"name": name, "type": 1, "order": 999, "route_name": name.replace("IT菜单_","ItMenu"), "route_path": "/it-menu", "redirect": "/it-menu", "title": name}, headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/status/batch", json={"ids": [mid], "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/delete", json=[mid], headers=auth_headers).status_code == 200
    finally:
        await _clean("DELETE FROM sys_menu WHERE name=:v", v=name)


async def test_dept_controller(test_client, auth_headers) -> None:
    name = _n("IT部门"); code = _n("itdc")
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/dept/tree")).rsplit("/tree", 1)[0]
    try:
        r = test_client.post(f"{base}/create", json={"name": name, "code": code, "order": 1}, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        did = r.json()["data"]["id"]
        assert test_client.get(f"{base}/tree", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/detail/{did}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/update/{did}", json={"name": name, "code": code, "order": 1}, headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/status/batch", json={"ids": [did], "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/delete", json=[did], headers=auth_headers).status_code == 200
    finally:
        await _clean("DELETE FROM sys_dept WHERE name=:v", v=name)
