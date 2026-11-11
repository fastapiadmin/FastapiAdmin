"""传输任务 HTTP 接口（本地源 → 本地目标）。"""

from __future__ import annotations

import json
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

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


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
    return f"it_trapi-{uuid.uuid4().hex[:8]}"


async def test_transfer_api(test_client, auth_headers, tmp_path) -> None:
    name = _name(); root = tmp_path / name; root.mkdir()
    node_name = name + "-local"
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    async with _db() as db:
        node = await StorageNodeService(auth, db).create(StorageNodeCreateSchema(name=node_name, protocol="local", host=str(root), port=0))
        await db.commit()
    base = "/api/v1/task/storage/transfer"
    try:
        targets = json.dumps([{"target_id": node.id, "target_path": "out/a.txt"}])
        created = test_client.post(f"{base}/task/upload", data={"name": name, "task_type": "parallel", "targets": targets}, files={"file": ("a.txt", b"hello-api", "text/plain")}, headers=auth_headers)
        if created.status_code == 404:
            base = "/api/v1/storage/transfer"
            created = test_client.post(f"{base}/task/upload", data={"name": name, "task_type": "parallel", "targets": targets}, files={"file": ("a.txt", b"hello-api", "text/plain")}, headers=auth_headers)
        assert created.status_code == 200, created.text
        tid = created.json()["data"]["id"]
        assert test_client.get(f"{base}/task/page", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/task/{tid}", headers=auth_headers).status_code == 200
        assert test_client.post(f"{base}/task/{tid}/cancel", headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/task", json=[tid], headers=auth_headers).status_code == 200
    finally:
        async with _db() as db:
            await db.execute(text("DELETE FROM task_storage_transfer WHERE name=:n"), {"n": name})
            await db.execute(text("DELETE FROM task_storage_node WHERE name=:n"), {"n": node_name})
            await db.commit()
        import shutil; shutil.rmtree(root, ignore_errors=True)
