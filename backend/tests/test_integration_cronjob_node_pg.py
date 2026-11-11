"""真实 PostgreSQL 调度节点定义 CRUD 集成。"""

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
from app.modules.task.cronjob.node.service import NodeService

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
    return f"it_node_{uuid.uuid4().hex[:10]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


async def _cleanup(name: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM task_cornjob_node WHERE name=:n"), {"n": name})
        await db.commit()


async def test_node_crud(test_client) -> None:
    from app.modules.task.cronjob.node.schema import NodeCreateSchema, NodeUpdateSchema
    name = _name()
    try:
        async with _db() as db:
            svc = NodeService(_auth(), db)
            node = await svc.create(NodeCreateSchema(name=name, func="builtin:server_status", trigger=None))
            assert node.name == name and node.code
            assert (await svc.detail(node.id)).name == name
            assert any(n.name == name for n in await svc.options())
            assert (await svc.page(1, 10, None)).total >= 1
            await svc.batch_set_status([node.id], 1)
            await svc.update(node.id, NodeUpdateSchema(name=name, func="builtin:server_status", trigger=None))
            await svc.delete([node.id])
    finally:
        await _cleanup(name)


async def test_node_clear(test_client) -> None:
    from app.modules.task.cronjob.node.schema import NodeCreateSchema
    name = _name()
    try:
        async with _db() as db:
            svc = NodeService(_auth(), db)
            await svc.create(NodeCreateSchema(name=name, func="builtin:server_status", trigger=None))
            await svc.clear()
            assert isinstance(await svc.get_list(), list)
    finally:
        await _cleanup(name)


async def test_node_execute_errors(test_client) -> None:
    from app.modules.task.cronjob.node.schema import NodeCreateSchema
    from app.core.exceptions import CustomException
    name = _name()
    try:
        async with _db() as db:
            svc = NodeService(_auth(), db)
            with pytest.raises(CustomException):
                await svc.execute(99999999)
            node = await svc.create(NodeCreateSchema(name=name, func="builtin:missing_handler", trigger=None))
            with pytest.raises(CustomException):
                await svc.execute(node.id)
            with pytest.raises(CustomException):
                await svc.update(99999999, NodeCreateSchema(name=name, func="builtin:missing_handler", trigger=None))
    finally:
        await _cleanup(name)


async def test_node_duplicate_and_missing(test_client) -> None:
    from app.modules.task.cronjob.node.schema import NodeCreateSchema
    from app.core.exceptions import CustomException
    name = _name()
    try:
        async with _db() as db:
            svc = NodeService(_auth(), db)
            await svc.create(NodeCreateSchema(name=name, func="builtin:x", trigger=None))
            with pytest.raises(CustomException):
                await svc.create(NodeCreateSchema(name=name, func="builtin:x", trigger=None))
            with pytest.raises(CustomException):
                await svc.delete([99999999])
            with pytest.raises(CustomException):
                await svc.delete([])
    finally:
        await _cleanup(name)


async def test_cron_job_api(test_client, auth_headers) -> None:
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/cronjob/job/scheduler/status")).rsplit("/scheduler/status", 1)[0]
    assert test_client.get(f"{base}/scheduler/status", headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/scheduler/jobs", headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/scheduler/console", headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/log/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/log/detail/99999999", headers=auth_headers).status_code in (400, 404)
    assert test_client.request("DELETE", f"{base}/log/delete", json=[], headers=auth_headers).status_code == 400


async def test_cron_node_api(test_client, auth_headers) -> None:
    from app.modules.task.cronjob.node.schema import NodeCreateSchema
    name = _name()
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/cronjob/node/list")).rsplit("/list", 1)[0]
    try:
        async with _db() as db:
            await NodeService(_auth(), db).create(NodeCreateSchema(name=name, func="builtin:server_status", trigger=None))
            await db.commit()
            nid = (await db.execute(text("SELECT id FROM task_cornjob_node WHERE name=:n"), {"n": name})).scalar_one()
        created = test_client.post(f"{base}/create", json={"name": name + "_api", "func": "builtin:server_status", "trigger": None}, headers=auth_headers)
        assert created.status_code in (200, 201), created.text
        created_id = created.json()["data"]["id"]
        assert test_client.get(f"{base}/options", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/detail/{nid}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/update/{nid}", json={"name": name, "func": "builtin:server_status", "trigger": None}, headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/status/batch", json={"ids": [nid], "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.post(f"{base}/execute/{nid}", headers=auth_headers).status_code in (200, 400)
        assert test_client.post(f"{base}/execute/99999999", headers=auth_headers).status_code in (400, 404)
        assert test_client.request("DELETE", f"{base}/delete", json=[nid, created_id], headers=auth_headers).status_code == 200
    finally:
        await _cleanup(name)


async def test_cron_job_control_routes(test_client, auth_headers, monkeypatch: pytest.MonkeyPatch) -> None:
    from unittest.mock import AsyncMock, MagicMock
    import app.modules.task.cronjob.job.controller as c
    for name in ("start_scheduler", "shutdown_scheduler"):
        monkeypatch.setattr(c.JobService, name, staticmethod(AsyncMock()))
    for name in ("pause_scheduler", "resume_scheduler", "clear_scheduler_jobs", "pause_job", "resume_job", "run_job_now", "modify_job", "remove_job"):
        monkeypatch.setattr(c.JobService, name, staticmethod(MagicMock()))
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/cronjob/job/scheduler/status")).rsplit("/scheduler/status", 1)[0]
    assert test_client.post(f"{base}/scheduler/start", headers=auth_headers).status_code == 200
    assert test_client.post(f"{base}/scheduler/pause", headers=auth_headers).status_code == 200
    assert test_client.post(f"{base}/scheduler/resume", headers=auth_headers).status_code == 200
    assert test_client.post(f"{base}/scheduler/shutdown", headers=auth_headers).status_code == 200
    assert test_client.delete(f"{base}/scheduler/jobs/clear", headers=auth_headers).status_code == 200
    assert test_client.post(f"{base}/task/pause/1", headers=auth_headers).status_code == 200
    assert test_client.post(f"{base}/task/resume/1", headers=auth_headers).status_code == 200
    assert test_client.post(f"{base}/task/run/1", headers=auth_headers).status_code == 200
    assert test_client.put(f"{base}/task/modify/1", json={"name": "n"}, headers=auth_headers).status_code == 200
    assert test_client.delete(f"{base}/task/remove/1", headers=auth_headers).status_code == 200
