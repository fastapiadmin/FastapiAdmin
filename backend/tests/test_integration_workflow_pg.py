"""真实 PostgreSQL 传输流程创建/执行集成。"""

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
from app.core.exceptions import CustomException
from app.modules.task.storage.node.schema import StorageNodeCreateSchema
from app.modules.task.storage.node.service import StorageNodeService
from app.modules.task.storage.workflow.schema import WorkflowCreateSchema
from app.modules.task.storage.workflow.service import WorkflowService

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
    return f"it_wf_{uuid.uuid4().hex[:8]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


def _graph(src: int, dst: int, src_path: str, dst_path: str, enabled: bool = True) -> dict:
    return {
        "nodes": [
            {"id": "s", "type": "storage", "position": {"x": 0, "y": 0}, "data": {"source_id": src, "source_path": src_path, "label": "S"}},
            {"id": "d", "type": "storage", "position": {"x": 1, "y": 0}, "data": {"source_id": dst, "source_path": dst_path, "label": "D"}},
        ],
        "edges": [{"id": "e", "source": "s", "target": "d", "data": {"enabled": enabled}}],
    }


async def _cleanup(flow_id: int, names: list[str]) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM task_storage_workflow_node WHERE flow_id=:i"), {"i": flow_id})
        await db.execute(text("DELETE FROM task_storage_workflow_edge WHERE flow_id=:i"), {"i": flow_id})
        await db.execute(text("DELETE FROM task_storage_workflow WHERE id=:i"), {"i": flow_id})
        for n in names:
            await db.execute(text("DELETE FROM task_storage_node WHERE name=:n"), {"n": n})
        await db.commit()


async def test_workflow_crud(test_client) -> None:
    tag = _name(); src_name = tag + "_s"; dst_name = tag + "_d"; flow_id = 0
    try:
        async with _db() as db:
            auth = _auth()
            src = await StorageNodeService(auth, db).create(StorageNodeCreateSchema(name=src_name, protocol="local", host="/tmp", port=0))
            dst = await StorageNodeService(auth, db).create(StorageNodeCreateSchema(name=dst_name, protocol="local", host="/tmp/dst", port=0))
            svc = WorkflowService(auth, db)
            flow = await svc.create(WorkflowCreateSchema(name=tag, graph=_graph(src.id, dst.id, "/tmp", "/tmp/out")))
            flow_id = flow.id
            assert (await svc.detail(flow_id)).name == tag
            assert (await svc.page(None, 1, 10)).total >= 1
            with pytest.raises(CustomException, match="已存在"):
                await svc.create(WorkflowCreateSchema(name=tag, graph=_graph(src.id, dst.id, "/tmp", "/tmp/out")))
            await svc.delete([flow_id])
    finally:
        await _cleanup(flow_id, [src_name, dst_name])


async def test_workflow_execute_no_enabled_edges(test_client) -> None:
    tag = _name(); names = [tag + "_s", tag + "_d"]; flow_id = 0
    try:
        async with _db() as db:
            auth = _auth()
            src = await StorageNodeService(auth, db).create(StorageNodeCreateSchema(name=names[0], protocol="local", host="/tmp", port=0))
            dst = await StorageNodeService(auth, db).create(StorageNodeCreateSchema(name=names[1], protocol="local", host="/tmp/dst", port=0))
            svc = WorkflowService(auth, db)
            flow = await svc.create(WorkflowCreateSchema(name=tag, graph=_graph(src.id, dst.id, "/tmp", "/tmp/out", enabled=False)))
            flow_id = flow.id
            with pytest.raises(CustomException, match="没有启用"):
                await svc.execute(flow_id)
    finally:
        await _cleanup(flow_id, names)


async def test_workflow_execute_plan(test_client) -> None:
    tag = _name(); names = [tag + "_s", tag + "_d"]
    async with _db() as db:
        auth = _auth()
        src = await StorageNodeService(auth, db).create(StorageNodeCreateSchema(name=names[0], protocol="local", host="/tmp", port=0))
        dst = await StorageNodeService(auth, db).create(StorageNodeCreateSchema(name=names[1], protocol="local", host="/tmp/dst", port=0))
        svc = WorkflowService(auth, db)
        flow = await svc.create(WorkflowCreateSchema(name=tag, graph=_graph(src.id, dst.id, "/tmp", "/tmp/out")))
        ids = await svc.execute(flow.id, {str(src.id): "/tmp"})
        assert ids
        await db.rollback()
