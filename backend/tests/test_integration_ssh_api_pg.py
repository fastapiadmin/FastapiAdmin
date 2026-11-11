"""SSH 运维 HTTP 接口（真实 PG，连接层 mock）。"""

from __future__ import annotations

import os
import uuid

import pytest

from app.modules.ops.ssh import service as ssh_mod

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


def _name() -> str:
    return f"it_sshapi_{uuid.uuid4().hex[:8]}"


def test_ssh_host_and_snippet_api(test_client, auth_headers, monkeypatch: pytest.MonkeyPatch) -> None:
    name = _name()
    class C:
        def close(self): pass
    monkeypatch.setattr(ssh_mod, "connect_client", lambda **kw: C())
    base = "/api/v1/ops/ssh"
    try:
        created = test_client.post(f"{base}/host/create", json={"name": name, "host": "127.0.0.1", "port": 22, "username": "root", "auth_type": "password", "password": "x"}, headers=auth_headers)
        if created.status_code == 404:
            base = "/api/v1/ssh"
            created = test_client.post(f"{base}/host/create", json={"name": name, "host": "127.0.0.1", "port": 22, "username": "root", "auth_type": "password", "password": "x"}, headers=auth_headers)
        assert created.status_code in (200, 201), created.text
        hid = created.json()["data"]["id"]
        assert test_client.get(f"{base}/host/list", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/host/detail/{hid}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/host/update/{hid}", json={"name": name, "host": "127.0.0.1", "port": 2222, "username": "root", "auth_type": "password"}, headers=auth_headers).status_code == 200
        assert test_client.post(f"{base}/host/test/{hid}", headers=auth_headers).status_code == 200
        sn = test_client.post(f"{base}/snippet/create", json={"name": name, "command": "ls"}, headers=auth_headers)
        assert sn.status_code in (200, 201)
        sid = sn.json()["data"]["id"]
        assert test_client.get(f"{base}/snippet/list", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/snippet/update/{sid}", json={"name": name, "command": "pwd"}, headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/snippet/delete", json=[sid], headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/host/delete", json=[hid], headers=auth_headers).status_code == 200
    finally:
        from sqlalchemy import text
        from app.config.setting import settings
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy.pool import NullPool
        import asyncio
        async def clean():
            e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
            try:
                async with e.begin() as c:
                    await c.execute(text("DELETE FROM ops_ssh_host WHERE name=:n"), {"n": name})
                    await c.execute(text("DELETE FROM ops_ssh_snippet WHERE name=:n"), {"n": name})
            finally:
                await e.dispose()
        asyncio.run(clean())
