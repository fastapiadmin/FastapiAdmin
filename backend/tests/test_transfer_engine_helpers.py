"""传输引擎纯函数与步骤展开测试。"""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.modules.task.storage.core.base import StorageObject
from app.modules.task.storage.transfer import engine
from app.modules.task.storage.transfer.schema import TransferTaskCreateSchema
from app.modules.task.storage.transfer.service import StorageTransferService


def test_local_path_size_and_files(tmp_path: Path) -> None:
    root = tmp_path / "root"
    (root / "a").mkdir(parents=True)
    (root / "a" / "x.txt").write_text("xx")
    (root / "y.txt").write_text("y")
    assert engine._local_path_size(str(root / "y.txt")) == 1
    assert engine._local_path_size(str(root)) == 3
    assert engine._local_path_size(str(root / "missing")) == 0
    files = engine._list_local_files(str(root))
    assert len(files) == 2 and {rel for _, rel, _ in files} == {"a/x.txt", "y.txt"}


def test_prepare_local_dirs(tmp_path: Path) -> None:
    p1 = tmp_path / "a" / "x.txt"
    p2 = tmp_path / "b" / "y.txt"
    engine._prepare_local_dirs([str(p1), str(p2), ""])
    assert p1.parent.is_dir() and p2.parent.is_dir()


async def test_remove_temp_and_size_helpers(tmp_path: Path) -> None:
    f = tmp_path / "f.txt"
    f.write_text("x")
    task = SimpleNamespace(source_type="local", source_path=str(f))
    engine._remove_local_temp(task)
    assert not f.exists()
    d = tmp_path / "d"
    d.mkdir()
    await engine._remove_local_temp_dir(str(d))
    assert not d.exists()
    await engine._remove_local_temp_dir("")


async def test_is_dir_and_resolve_size(tmp_path: Path) -> None:
    class A:
        async def list_files(self, path):
            return [StorageObject(name="d", key="d", is_dir=True), StorageObject(name="f", key="f", size=7)]

        async def list_recursive(self, path):
            return [StorageObject(name="x", key="d/x", is_dir=False, size=3), StorageObject(name="y", key="d/y", is_dir=False, size=4)]

    a = A()
    assert await engine._is_dir_path(a, "d") is True
    assert await engine._resolve_source_size(a, "f") == 7
    assert await engine._resolve_source_size(a, "d") == 7


def test_transfer_steps_parallel_and_chain() -> None:
    targets = [{"target_id": 2, "target_path": "b"}, {"target_id": 3, "target_path": "c"}]
    data = TransferTaskCreateSchema(name="t", task_type="parallel", source_id=1, source_path="a", targets=targets)
    steps = StorageTransferService._build_steps(data)
    assert [s.target_id for s in steps] == [2, 3]
    data2 = TransferTaskCreateSchema(name="t", task_type="chain", source_id=1, source_path="a", targets=targets)
    steps2 = StorageTransferService._build_steps(data2)
    assert steps2[0].source_id == 1 and steps2[0].source_path == "a"
    assert steps2[1].source_id == 2 and steps2[1].source_path == "b"
