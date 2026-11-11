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


async def _run_multi(tmp_path, monkeypatch: pytest.MonkeyPatch, targets: int, canceled: bool) -> tuple[str, list[Path], int, list[str]]:
    name = _name(); src = tmp_path / f"{name}.txt"; src.write_text("hello")
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    roots: list[Path] = []
    node_names: list[str] = []
    async with _db() as db:
        node_ids = []
        for i in range(targets):
            n = f"{name}_{i}"; node_names.append(n); root = tmp_path / n; root.mkdir(); roots.append(root)
            node = await StorageNodeService(auth, db).create(StorageNodeCreateSchema(name=n, protocol="local", host=str(root), port=0))
            node_ids.append(node.id)
        task = StorageTransferTaskModel(name=name, task_type="parallel", source_type="local", source_path=str(src), source_name=src.name, status="pending")
        db.add(task); await db.commit(); await db.refresh(task)
        for i, nid in enumerate(node_ids):
            db.add(StorageTransferStepModel(task_id=task.id, step_order=i, source_path=str(src), target_id=nid, target_path=f"out/{i}.txt"))
        await db.commit(); task_id = task.id

    @asynccontextmanager
    async def test_session():
        async with _db() as session:
            yield session
    monkeypatch.setattr(transfer_engine, "async_db_session", test_session)
    if canceled:
        transfer_engine.transfer_task_registry.mark_cancel(task_id)
    await transfer_engine._execute_transfer_task(task_id)
    async with _db() as db:
        status = (await db.execute(text("SELECT status FROM task_storage_transfer WHERE id=:i"), {"i": task_id})).scalar_one()
    return status, roots, task_id, node_names


async def test_transfer_multi_target(test_client, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    status, roots, task_id, names = await _run_multi(tmp_path, monkeypatch, 2, False)
    try:
        assert status == "success"
        assert all((root / "out" / f"{i}.txt").read_text() == "hello" for i, root in enumerate(roots))
    finally:
        async with _db() as db:
            await db.execute(text("DELETE FROM task_storage_transfer WHERE id=:i"), {"i": task_id})
            for name in names:
                await db.execute(text("DELETE FROM task_storage_node WHERE name=:n"), {"n": name})
            await db.commit()


async def test_transfer_canceled(test_client, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    status, roots, task_id, names = await _run_multi(tmp_path, monkeypatch, 1, True)
    try:
        assert status == "canceled"
        assert not (roots[0] / "out" / "0.txt").exists()
    finally:
        async with _db() as db:
            await db.execute(text("DELETE FROM task_storage_transfer WHERE id=:i"), {"i": task_id})
            for name in names:
                await db.execute(text("DELETE FROM task_storage_node WHERE name=:n"), {"n": name})
            await db.commit()



async def test_transfer_service_create_local(test_client, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    from io import BytesIO
    from fastapi import UploadFile
    from app.modules.task.storage.transfer.schema import TransferTargetSchema, TransferTaskCreateSchema
    from app.modules.task.storage.transfer.service import StorageTransferService
    name = _name(); root = tmp_path / name; root.mkdir()
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    async with _db() as db:
        node = await StorageNodeService(auth, db).create(StorageNodeCreateSchema(name=name, protocol="local", host=str(root), port=0))
        svc = StorageTransferService(auth, db)
        monkeypatch.setattr(svc, "_launch_after_commit", lambda task_id: None)
        data = TransferTaskCreateSchema(name=name, task_type="parallel", source_type="local", targets=[TransferTargetSchema(target_id=node.id, target_path="out/a.txt")])
        task_id = await svc.create_local(data, UploadFile(filename="a.txt", file=BytesIO(b"hello")))
        await db.commit()
        detail = await svc.detail(task_id)
        assert detail.name == name and detail.steps
        page = await svc.page(None, 1, 10)
        assert page.total >= 1
        await svc.cancel(task_id)
        await db.commit()
        await svc.delete([task_id])
        await db.commit()
    import shutil; shutil.rmtree(root, ignore_errors=True)
    await _cleanup(task_id, name, root)


async def test_transfer_service_validation(test_client) -> None:
    from app.modules.task.storage.transfer.schema import TransferTargetSchema, TransferTaskCreateSchema
    from app.modules.task.storage.transfer.service import StorageTransferService
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    async with _db() as db:
        svc = StorageTransferService(auth, db)
        data = TransferTaskCreateSchema(name=_name(), task_type="parallel", source_type="local", targets=[TransferTargetSchema(target_id=99999999, target_path="x")])
        with pytest.raises(Exception):
            await svc.create(data)
