"""字典类型/数据 HTTP 接口（真实 PG）。"""

from __future__ import annotations

import os
import uuid

import pytest
from sqlalchemy import text

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


def _name() -> str:
    return f"it_dict_{uuid.uuid4().hex[:8]}"


async def _cleanup(code: str) -> None:
    from app.config.setting import settings
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.pool import NullPool
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    try:
        async with e.begin() as c:
            await c.execute(text("DELETE FROM sys_dict_data WHERE dict_type=:t"), {"t": code})
            await c.execute(text("DELETE FROM sys_dict_type WHERE dict_type=:t"), {"t": code})
    finally:
        await e.dispose()


async def test_dict_api(test_client, auth_headers) -> None:
    code = _name()
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/dict/type/list")).rsplit("/type/list", 1)[0]
    try:
        t = test_client.post(f"{base}/type/create", json={"dict_name": code, "dict_type": code}, headers=auth_headers)
        assert t.status_code in (200, 201), t.text
        tid = t.json()["data"]["id"]
        assert test_client.get(f"{base}/type/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/type/optionselect", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/type/detail/{tid}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/type/update/{tid}", json={"dict_name": code, "dict_type": code, "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/type/status/batch", json={"ids": [tid], "status": 0}, headers=auth_headers).status_code == 200
        d = test_client.post(f"{base}/data/create", json={"dict_type": code, "dict_type_id": tid, "dict_label": "L", "dict_value": "1", "dict_sort": 1, "status": 0}, headers=auth_headers)
        assert d.status_code in (200, 201), d.text
        did = d.json()["data"]["id"]
        assert test_client.get(f"{base}/data/list", params={"dict_type": code, "page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/data/info/{code}", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/data/detail/{did}", headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/data/status/batch", json={"ids": [did], "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/data/delete", json=[did], headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/type/delete", json=[tid], headers=auth_headers).status_code == 200
    finally:
        await _cleanup(code)
