"""真实 MinIO 与本地存储之间的传输引擎端到端。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import AsyncIterator

import boto3
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
    os.getenv("RUN_INTEGRATION") != "1" or not os.getenv("S3_ACCESS_KEY") or not os.getenv("S3_SECRET_KEY"),
    reason="需要真实 PostgreSQL/MinIO：设置 RUN_INTEGRATION=1、S3_ACCESS_KEY、S3_SECRET_KEY",
)

_ENDPOINT = os.getenv("S3_ENDPOINT", "http://127.0.0.1:9000")


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            yield session
    finally:
        await engine.dispose()


def _client():
    return boto3.client("s3", endpoint_url=_ENDPOINT, aws_access_key_id=os.environ["S3_ACCESS_KEY"], aws_secret_access_key=os.environ["S3_SECRET_KEY"], region_name="us-east-1")


def _name() -> str:
    return f"it-s3tr-{uuid.uuid4().hex[:8]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


async def _cleanup(task_id: int | None, names: list[str], bucket: str) -> None:
    async with _db() as db:
        if task_id:
            await db.execute(text("DELETE FROM task_storage_transfer WHERE id=:i"), {"i": task_id})
        for n in names:
            await db.execute(text("DELETE FROM task_storage_node WHERE name=:n"), {"n": n})
        await db.commit()
    c = _client()
    try:
        objs = c.list_objects_v2(Bucket=bucket).get("Contents", [])
        if objs:
            c.delete_objects(Bucket=bucket, Delete={"Objects": [{"Key": o["Key"]} for o in objs]})
        c.delete_bucket(Bucket=bucket)
    except Exception:
        pass


async def _run(tmp_path, monkeypatch, direction: str):
    name = _name(); bucket = name; src_root = tmp_path / (name + "_local"); src_root.mkdir()
    _client().create_bucket(Bucket=bucket)
    async with _db() as db:
        s3 = await StorageNodeService(_auth(), db).create(StorageNodeCreateSchema(
            name=name + "_s3", protocol="s3", endpoint=_ENDPOINT, scheme="http",
            username=os.environ["S3_ACCESS_KEY"], password=os.environ["S3_SECRET_KEY"],
            bucket=bucket, region="us-east-1", advanced_config={"addressing_style": "path"},
        ))
        if direction == "upload":
            src = tmp_path / "up.txt"; src.write_text("to-s3")
            task = StorageTransferTaskModel(name=name, task_type="parallel", source_type="local", source_path=str(src), source_name=src.name, status="pending")
            db.add(task); await db.commit(); await db.refresh(task)
            db.add(StorageTransferStepModel(task_id=task.id, step_order=0, source_path=str(src), target_id=s3.id, target_path="it/out.txt"))
        else:
            _client().put_object(Bucket=bucket, Key="it/in.txt", Body=b"from-s3")
            task = StorageTransferTaskModel(name=name, task_type="parallel", source_type="remote", source_id=s3.id, source_path="it/in.txt", source_name="in.txt", status="pending")
            db.add(task); await db.commit(); await db.refresh(task)
            local = await StorageNodeService(_auth(), db).create(StorageNodeCreateSchema(name=name + "_local", protocol="local", host=str(src_root), port=0))
            db.add(StorageTransferStepModel(task_id=task.id, step_order=0, source_id=s3.id, source_path="it/in.txt", target_id=local.id, target_path="dl/out.txt"))
        await db.commit(); task_id = task.id

    @asynccontextmanager
    async def test_session():
        async with _db() as session:
            yield session
    monkeypatch.setattr(transfer_engine, "async_db_session", test_session)
    await transfer_engine._execute_transfer_task(task_id)
    async with _db() as db:
        status = (await db.execute(text("SELECT status FROM task_storage_transfer WHERE id=:i"), {"i": task_id})).scalar_one()
    return task_id, [name + "_s3", name + "_local"], bucket, src_root, status


async def test_local_to_minio(test_client, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    task_id = None
    try:
        task_id, names, bucket, _, status = await _run(tmp_path, monkeypatch, "upload")
        assert status == "success"
        body = _client().get_object(Bucket=bucket, Key="it/out.txt")["Body"].read()
        assert body == b"to-s3"
    finally:
        await _cleanup(task_id, names, bucket)


async def test_minio_to_local(test_client, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    task_id = None
    try:
        task_id, names, bucket, root, status = await _run(tmp_path, monkeypatch, "download")
        assert status == "success"
        assert (root / "dl" / "out.txt").read_text() == "from-s3"
    finally:
        await _cleanup(task_id, names, bucket)
