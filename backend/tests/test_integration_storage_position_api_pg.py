"""存储源/传输/岗位 controller 剩余接口。"""

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


async def test_storage_node_extra(test_client, auth_headers, tmp_path) -> None:
    name = _n("it_node")
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/storage/node/create")).rsplit("/create", 1)[0]
    payload = {"name": name, "protocol": "local", "host": str(tmp_path), "port": 0}
    try:
        r = test_client.post(f"{base}/create", json=payload, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        nid = r.json()["data"]["id"]
        assert test_client.get(f"{base}/protocols", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/advanced-fields", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/page", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/list", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/export", headers=auth_headers).status_code == 200
        assert test_client.post(f"{base}/import", json={"nodes": []}, headers=auth_headers).status_code in (200, 400)
        assert test_client.post(f"{base}/test/{nid}", headers=auth_headers).status_code in (200, 400)
    finally:
        await _clean("DELETE FROM task_storage_node WHERE name=:v", v=name)


async def test_position_controller(test_client, auth_headers) -> None:
    name = _n("it_pos"); code = _n("pos")
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/position/list")).rsplit("/list", 1)[0]
    try:
        r = test_client.post(f"{base}/create", json={"name": name, "code": code, "status": 0, "order": 1}, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        pid = r.json()["data"]["id"]
        assert test_client.get(f"{base}/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/detail/{pid}", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/options", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/update/{pid}", json={"name": name, "code": code, "status": 0, "order": 1}, headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/status/batch", json={"ids": [pid], "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/delete", json=[pid], headers=auth_headers).status_code == 200
    finally:
        await _clean("DELETE FROM sys_position WHERE code=:v", v=code)


async def test_transfer_controller_errors(test_client, auth_headers) -> None:
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/storage/transfer/task")).rsplit("/task", 1)[0]
    assert test_client.get(f"{base}/task/page", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/task/99999999", headers=auth_headers).status_code in (400, 404)
    assert test_client.post(f"{base}/task/99999999/cancel", headers=auth_headers).status_code in (400, 404)
    assert test_client.request("DELETE", f"{base}/task", json=[], headers=auth_headers).status_code in (200, 400)
    assert test_client.post(f"{base}/task", json={}, headers=auth_headers).status_code in (400, 422)
    assert test_client.post(f"{base}/task/upload", data={"name": "x", "task_type": "parallel", "targets": "bad"}, files={"file": ("a.txt", b"x", "text/plain")}, headers=auth_headers).status_code in (400, 422)
