"""本地存储适配器完整文件操作测试（真实临时目录）。"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.core.exceptions import CustomException
from app.modules.task.storage.core.base import StorageAdapterConfig, StorageProtocol
from app.modules.task.storage.core.local_adapter import LocalStorageAdapter


def _adapter(root: Path) -> LocalStorageAdapter:
    return LocalStorageAdapter(StorageAdapterConfig(protocol=StorageProtocol.LOCAL, port=0, host=str(root)))


async def test_local_storage_full_crud(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    a = _adapter(root)
    assert await a.test_connection() is True

    src = tmp_path / "src.txt"
    src.write_text("hello", encoding="utf-8")
    assert await a.upload(str(src), "dir/a.txt") == "dir/a.txt"
    assert await a.exists("dir/a.txt") is True

    files = await a.list_files("dir")
    assert files[0].name == "a.txt" and files[0].size == 5

    out = tmp_path / "out.txt"
    assert await a.download("dir/a.txt", str(out)) == str(out)
    assert out.read_text() == "hello"

    await a.mkdir("empty")
    await a.rmdir("empty")
    await a.rename("dir/a.txt", "dir/b.txt")
    await a.copy("dir/b.txt", "dir/c.txt")
    assert await a.exists("dir/c.txt") is True
    assert (await a.list_recursive("dir"))
    await a.delete("dir/c.txt")
    assert await a.exists("dir/c.txt") is False
    await a.delete("dir")


async def test_local_storage_dir_operations(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    a = _adapter(root)
    local_dir = tmp_path / "upload"
    local_dir.mkdir()
    (local_dir / "x.txt").write_text("x")
    assert await a.upload_dir(str(local_dir), "up", concurrency=2) == 1
    assert await a.exists("up/x.txt") is True
    target = tmp_path / "download"
    await a.download_dir("up", str(target), concurrency=2)
    assert (target / "x.txt").read_text() == "x"
    await a.delete_dir("up")


async def test_local_storage_rejects_traversal(tmp_path: Path) -> None:
    a = _adapter(tmp_path)
    with pytest.raises(CustomException, match="路径穿越"):
        await a.exists("../x")
    with pytest.raises(CustomException, match="路径穿越"):
        await a.upload("/etc/passwd", "../x")


async def test_local_storage_missing_root(tmp_path: Path) -> None:
    a = _adapter(tmp_path / "missing")
    assert await a.test_connection() is False


async def test_local_missing_operations(tmp_path: Path) -> None:
    root = tmp_path / "root"; root.mkdir(); a = _adapter(root)
    with pytest.raises(Exception):
        await a.list_files("missing")
    with pytest.raises(Exception):
        await a.rename("missing", "x")
    with pytest.raises(Exception):
        await a.copy("missing", "x")
    with pytest.raises(Exception):
        await a.download("missing", str(tmp_path / "x"))


async def test_local_edge_operations(tmp_path: Path) -> None:
    root=tmp_path/"root"; root.mkdir(); a=_adapter(root)
    assert await a.exists("missing") is False
    with pytest.raises(Exception):
        await a.list_files("missing")
    with pytest.raises(Exception):
        await a.rename("missing","x")
    with pytest.raises(Exception):
        await a.copy("missing","x")
    with pytest.raises(Exception):
        await a.download("missing",str(tmp_path/"x"))
