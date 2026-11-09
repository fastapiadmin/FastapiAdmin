"""示例插件 HTTP 接口集成（若插件路由已注册）。"""

from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


def _base(test_client) -> str:
    paths = test_client.get("/openapi.json").json()["paths"]
    candidates = sorted(p for p in paths if "demo" in p and "template" not in p and "export" not in p and "import" not in p)
    if not candidates:
        pytest.skip("示例插件未注册路由")
    for p in candidates:
        if p.endswith("/list"):
            return p[: -len("/list")]
    return candidates[0].rsplit("/", 1)[0]


def test_demo_crud_api(test_client, auth_headers) -> None:
    base = _base(test_client)
    payload = {"name": "it_demo", "status": 0, "description": "it"}
    created = test_client.post(f"{base}/create", json=payload, headers=auth_headers)
    assert created.status_code in (200, 201), created.text
    oid = created.json()["data"]["id"]
    try:
        assert test_client.get(f"{base}/detail/{oid}", headers=auth_headers).status_code == 200
        listing = test_client.get(f"{base}/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers)
        assert listing.status_code == 200 and listing.json()["data"]["total"] >= 1
        updated = test_client.put(f"{base}/update/{oid}", json={**payload, "name": "it_demo2"}, headers=auth_headers)
        assert updated.status_code == 200
        batch = test_client.patch(f"{base}/status/batch", json={"ids": [oid], "status": 1}, headers=auth_headers)
        assert batch.status_code == 200
    finally:
        assert test_client.request("DELETE", f"{base}/delete", json=[oid], headers=auth_headers).status_code == 200


def test_demo_template_and_missing(test_client, auth_headers) -> None:
    base = _base(test_client)
    template = test_client.post(f"{base}/download/template", headers=auth_headers)
    assert template.status_code == 200 and template.content
    assert test_client.get(f"{base}/detail/99999999", headers=auth_headers).status_code in (400, 404)


def test_demo_import_export(test_client, auth_headers) -> None:
    base = _base(test_client)
    export = test_client.post(f"{base}/export", json={"page_no": 1, "page_size": 10}, headers=auth_headers)
    assert export.status_code == 200 and export.content
