"""真实 PostgreSQL + 本地存储的传输引擎端到端集成。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.modules.task.storage.node.schema import StorageNodeCreateSchema
from app.modules.task.storage.node.service import StorageNodeService
from app.modules.task.storage.transfer import engine as transfer_engine
from app.modules.task.storage.transfer.model import StorageTransferStepModel, StorageTransferTaskModel

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
    return f"it_tr_{uuid.uuid4().hex[:10]}"


async def _cleanup(task_id: int, node_name: str, root: Path) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM task_storage_transfer WHERE id=:i"), {"i": task_id})
        await db.execute(text("DELETE FROM task_storage_node WHERE name=:n"), {"n": node_name})
        await db.commit()
    import shutil
    shutil.rmtree(root, ignore_errors=True)


async def _run(tmp_path, monkeypatch: pytest.MonkeyPatch, source_exists: bool) -> tuple[str, Path, int, str]:
    name = _name(); root = tmp_path / name; root.mkdir()
    src = tmp_path / f"{name}.txt"
    if source_exists:
        src.write_text("hello")
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    async with _db() as db:
        node = await StorageNodeService(auth, db).create(
            StorageNodeCreateSchema(name=name, protocol="local", host=str(root), port=0)
        )
        task = StorageTransferTaskModel(name=name, task_type="parallel", source_type="local", source_path=str(src), source_name=src.name, status="pending")
        db.add(task); await db.commit(); await db.refresh(task)
        db.add(StorageTransferStepModel(task_id=task.id, step_order=0, source_path=str(src), target_id=node.id, target_path="out/a.txt"))
        await db.commit()
        task_id = task.id

    @asynccontextmanager
    async def test_session():
        async with _db() as session:
            yield session
    monkeypatch.setattr(transfer_engine, "async_db_session", test_session)
    await transfer_engine._execute_transfer_task(task_id)
    async with _db() as db:
        status = (await db.execute(text("SELECT status FROM task_storage_transfer WHERE id=:i"), {"i": task_id})).scalar_one()
    return status, root, task_id, name


async def test_transfer_local_success(test_client, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    status, root, task_id, name = await _run(tmp_path, monkeypatch, True)
    try:
        assert status == "success"
        assert (root / "out" / "a.txt").read_text() == "hello"
    finally:
        await _cleanup(task_id, name, root)


async def test_transfer_local_missing_source(test_client, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    status, root, task_id, name = await _run(tmp_path, monkeypatch, False)
    try:
        assert status == "failed"
    finally:
        await _cleanup(task_id, name, root)
