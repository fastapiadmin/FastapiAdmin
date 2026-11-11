"""存储浏览 HTTP 接口（本地存储源）。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.modules.task.storage.node.schema import StorageNodeCreateSchema
from app.modules.task.storage.node.service import StorageNodeService

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


async def test_browse_api(test_client, auth_headers, tmp_path) -> None:
    name = f"it-browse-{uuid.uuid4().hex[:8]}"; root = tmp_path / name; root.mkdir()
    async with _db() as db:
        node = await StorageNodeService(SimpleNamespace(user=SimpleNamespace(id=0)), db).create(StorageNodeCreateSchema(name=name, protocol="local", host=str(root), port=0))
        await db.commit()
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/storage/browse/list")).rsplit("/list", 1)[0]
    try:
        up = test_client.post(f"{base}/upload", data={"source_id": node.id, "remote_path": "dir/a.txt"}, files={"file": ("a.txt", b"hello-browse", "text/plain")}, headers=auth_headers)
        assert up.status_code == 200, up.text
        assert test_client.get(f"{base}/list", params={"source_id": node.id, "prefix": "dir/"}, headers=auth_headers).status_code == 200
        assert test_client.post(f"{base}/download", json={"source_id": node.id, "remote_path": "dir/a.txt"}, headers=auth_headers).status_code == 200
        assert test_client.post(f"{base}/mkdir", json={"source_id": node.id, "remote_dir": "newdir"}, headers=auth_headers).status_code in (200, 201)
        assert test_client.post(f"{base}/copy", json={"source_id": node.id, "target_id": node.id, "source_path": "dir/a.txt", "target_path": "dir/b.txt"}, headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/rename", json={"source_id": node.id, "source_path": "dir/b.txt", "target_path": "dir/c.txt"}, headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/delete", json={"source_id": node.id, "remote_path": "dir/c.txt"}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/buckets", params={"source_id": node.id}, headers=auth_headers).status_code in (200, 400)
        assert test_client.post(f"{base}/create-bucket", json={"source_id": node.id, "bucket": "it-b"}, headers=auth_headers).status_code in (200, 400)
        assert test_client.post(f"{base}/share", json={"source_id": node.id, "remote_path": "dir/a.txt"}, headers=auth_headers).status_code in (200, 400)
        assert test_client.request("DELETE", f"{base}/delete", json={"source_id": node.id, "remote_path": "missing"}, headers=auth_headers).status_code in (200, 400)
        assert test_client.post(f"{base}/mkdir", json={"source_id": node.id, "remote_dir": "dir"}, headers=auth_headers).status_code in (200, 400)
    finally:
        async with _db() as db:
            await db.execute(text("DELETE FROM task_storage_node WHERE name=:n"), {"n": name})
            await db.commit()
        import shutil; shutil.rmtree(root, ignore_errors=True)
