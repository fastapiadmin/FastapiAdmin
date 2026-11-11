"""日志/传输流程 controller。"""

from __future__ import annotations

import os

import pytest
from sqlalchemy import text

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


async def test_log_controller(test_client, auth_headers) -> None:
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/log/login/list")).rsplit("/login/list", 1)[0]
    assert test_client.get(f"{base}/login/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/operation/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/login/detail/99999999", headers=auth_headers).status_code in (400, 404)
    assert test_client.get(f"{base}/operation/detail/99999999", headers=auth_headers).status_code in (400, 404)
    assert test_client.request("DELETE", f"{base}/login/delete", json=[], headers=auth_headers).status_code in (200, 400)
    assert test_client.request("DELETE", f"{base}/operation/delete", json=[], headers=auth_headers).status_code in (200, 400)
    assert test_client.post(f"{base}/operation/export", json={}, headers=auth_headers).status_code in (200, 400)


async def test_workflow_controller(test_client, auth_headers) -> None:
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/storage/workflow/page")).rsplit("/page", 1)[0]
    assert test_client.get(f"{base}/page", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/list", headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/detail/99999999", headers=auth_headers).status_code in (400, 404)
    r = test_client.post(f"{base}/create", json={"name": "it_wf", "task_type": "parallel", "graph": {}}, headers=auth_headers)
    assert r.status_code in (200, 201, 400, 422)
    assert test_client.request("DELETE", f"{base}/delete", json=[], headers=auth_headers).status_code in (200, 400)
