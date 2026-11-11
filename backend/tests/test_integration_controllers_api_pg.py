"""公告/存储源/版本 controller 接口。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from app.config.setting import settings
from sqlalchemy import text

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            yield session
    finally:
        await engine.dispose()


def _name() -> str:
    return f"it_api_{uuid.uuid4().hex[:8]}"


async def _clean(sql: str, value: str) -> None:
    from app.config.setting import settings
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.pool import NullPool
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    try:
        async with e.begin() as c:
            await c.execute(text(sql), {"v": value})
    finally:
        await e.dispose()


async def test_notice_controller(test_client, auth_headers) -> None:
    title = _name()
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/notice/list")).rsplit("/list", 1)[0]
    try:
        r = test_client.post(f"{base}/create", json={"notice_title": title, "notice_type": "1", "notice_content": "x", "status": 0}, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        nid = r.json()["data"]["id"]
        assert test_client.get(f"{base}/detail/{nid}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/update/{nid}", json={"notice_title": title, "notice_type": "1", "notice_content": "x", "status": 0}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/available", headers=auth_headers).status_code in (200, 404)
        assert test_client.request("DELETE", f"{base}/delete", json=[nid], headers=auth_headers).status_code == 200
    finally:
        await _clean("DELETE FROM sys_notice WHERE notice_title=:v", title)


async def test_storage_node_controller(test_client, auth_headers, tmp_path) -> None:
    name = _name()
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/storage/node/list")).rsplit("/list", 1)[0]
    try:
        payload = {"name": name, "protocol": "local", "host": str(tmp_path), "port": 0}
        r = test_client.post(f"{base}/create", json=payload, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        nid = r.json()["data"]["id"]
        assert test_client.get(f"{base}/detail/{nid}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/update/{nid}", json=payload, headers=auth_headers).status_code == 200
        assert test_client.post(f"{base}/test", json={"name": name, "protocol": "local", "host": str(tmp_path), "port": 0}, headers=auth_headers).status_code in (200, 400)
        assert test_client.request("DELETE", f"{base}/delete", json=[nid], headers=auth_headers).status_code == 200
    finally:
        await _clean("DELETE FROM task_storage_node WHERE name=:v", name)


async def test_version_controller(test_client, auth_headers) -> None:
    title = _name()
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if "version" in p and p.endswith("/list")).rsplit("/list", 1)[0]
    try:
        payload = {"version": "9.9.9", "title": title, "date": "2026-01-01", "sort": 0, "status": 0}
        r = test_client.post(f"{base}/create", json=payload, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        vid = r.json()["data"]["id"]
        assert test_client.get(f"{base}/detail/{vid}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/update/{vid}", json=payload, headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/delete", json=[vid], headers=auth_headers).status_code == 200
    finally:
        await _clean("DELETE FROM sys_version WHERE title=:v", title)


async def test_gencode_controller(test_client, auth_headers) -> None:
    import uuid
    from sqlalchemy import text
    table = f"it_genapi_{uuid.uuid4().hex[:8]}"
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/gencode/create")).rsplit("/create", 1)[0]
    try:
        sql = f'CREATE TABLE "{table}" (id SERIAL PRIMARY KEY, name VARCHAR(20))'
        r = test_client.post(f"{base}/create", json={"sql": sql}, headers=auth_headers)
        assert r.status_code in (200, 201), r.text
        assert test_client.post(f"{base}/import", json=[table], headers=auth_headers).status_code == 200
        async with _db() as db:
            gid = (await db.execute(text("SELECT id FROM gen_table WHERE table_name=:t"), {"t": table})).scalar_one()
        data = {"table_name": table, "class_name": "ItGenApi", "package_name": "module_it", "module_name": "it", "business_name": "it", "function_name": "ItGenApi"}
        assert test_client.put(f"{base}/update/{gid}", json=data, headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/batch/output", json=[table], headers=auth_headers).status_code in (200, 400)
        assert test_client.post(f"{base}/batch/output", json=[], headers=auth_headers).status_code in (200, 400, 405)
    finally:
        async with _db() as db:
            await db.execute(text(f'DROP TABLE IF EXISTS "{table}"'))
            await db.execute(text("DELETE FROM gen_table WHERE table_name=:t"), {"t": table})
            await db.execute(text("DELETE FROM sys_menu WHERE name=:n"), {"n": "ItGenApi"})
            await db.commit()
