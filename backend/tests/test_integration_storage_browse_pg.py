"""真实 PostgreSQL + 本地存储适配器的文件浏览服务集成。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from io import BytesIO
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from fastapi import UploadFile
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.modules.task.storage.browse.service import StorageFileService
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
    return f"it_browse_{uuid.uuid4().hex[:10]}"


def _upload(name: str, content: bytes = b"hello") -> UploadFile:
    return UploadFile(filename=name, file=BytesIO(content))


async def _make_node(db: AsyncSession, tmp_path, name: str, auth):
    from app.modules.task.storage.node.schema import StorageNodeCreateSchema
    root = tmp_path / name; root.mkdir(exist_ok=True)
    node = await StorageNodeService(auth, db).create(
        StorageNodeCreateSchema(name=name, protocol="local", host=str(root), port=0)
    )
    return node


async def _cleanup(name: str, root) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM task_storage_node WHERE name=:n"), {"n": name})
        await db.commit()
    import shutil
    shutil.rmtree(root, ignore_errors=True)


async def test_upload_list_download_delete(test_client, tmp_path) -> None:
    name = _name(); auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            node = await _make_node(db, tmp_path, name, auth)
            service = StorageFileService(auth, db)
            result = await service.upload(node.id, _upload("a.txt"), "dir/a.txt")
            assert result.file_path == "dir/a.txt"
            items = await service.list_files(node.id, "dir", page_size=10, cursor=None)
            assert any(item.name == "a.txt" for item in items.items)
            local, filename = await service.download(node.id, "dir/a.txt")
            assert filename == "a.txt"
            from pathlib import Path
            assert Path(local).read_text() == "hello"
            Path(local).unlink()
            await service.delete(node.id, "dir/a.txt")
            items = await service.list_files(node.id, "dir", page_size=10, cursor=None)
            assert not any(item.name == "a.txt" for item in items.items)
    finally:
        await _cleanup(name, tmp_path / name)


async def test_mkdir_rename_delete_dir(test_client, tmp_path) -> None:
    name = _name(); auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            node = await _make_node(db, tmp_path, name, auth)
            service = StorageFileService(auth, db)
            await service.mkdir(node.id, "d1")
            await service.upload(node.id, _upload("a.txt"), "d1/a.txt")
            await service.rename(node.id, "d1", "d2")
            items = await service.list_files(node.id, "d2", page_size=10, cursor=None)
            assert any(item.name == "a.txt" for item in items.items)
            await service.delete(node.id, "d2")
    finally:
        await _cleanup(name, tmp_path / name)


async def test_upload_traversal_rejected(test_client, tmp_path) -> None:
    name = _name(); auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            node = await _make_node(db, tmp_path, name, auth)
            service = StorageFileService(auth, db)
            with pytest.raises(CustomException, match="非法"):
                await service.upload(node.id, _upload("../evil.txt"), "a.txt")
    finally:
        await _cleanup(name, tmp_path / name)
