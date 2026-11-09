"""传输引擎目录/大小/远端解析分支。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import app.modules.task.storage.transfer.engine as E


def _obj(key, size=0, is_dir=False):
    return SimpleNamespace(key=key, name=key.rsplit("/", 1)[-1], size=size, is_dir=is_dir)


async def test_resolve_source_size() -> None:
    class DirAdapter:
        async def list_files(self, p): return [_obj("d/", is_dir=True)]
        async def list_recursive(self, p): return [_obj("d/a", 2), _obj("d/b", 3), _obj("d/sub/", is_dir=True)]
    assert await E._resolve_source_size(DirAdapter(), "d/") == 5
    class FileAdapter:
        async def list_files(self, p): return [_obj("a.txt", 7)]
    assert await E._resolve_source_size(FileAdapter(), "a.txt") == 7
    class Bad:
        async def list_files(self, p): raise RuntimeError("x")
    assert await E._resolve_source_size(Bad(), "x") == 0


def test_local_dir_helpers(tmp_path) -> None:
    d = tmp_path / "d"; d.mkdir(); (d / "a").write_text("123")
    assert E._local_path_size(str(d)) == 3
    assert E._local_path_size(str(d / "missing")) == 0
    p = d / "a"
    task = SimpleNamespace(source_type="local", source_path=str(p))
    E._remove_local_temp(task)
    assert not p.exists()
    E._prepare_local_dirs([str(tmp_path / "x" / "a"), str(tmp_path / "x" / "b")])
    assert (tmp_path / "x").is_dir()


async def test_remove_temp_dir(tmp_path) -> None:
    d = tmp_path / "d"; d.mkdir(); (d / "a").write_text("x")
    await E._remove_local_temp_dir(str(d))
    assert not d.exists()


async def test_download_dir(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    class A:
        async def list_recursive(self, p): return [_obj("d/a.txt", 1), _obj("d/sub/b.txt", 1), _obj("d/sub/", is_dir=True)]
        async def download(self, key, local): open(local, "w").write(key)
    await E._download_dir(A(), "d/", str(tmp_path))
    assert (tmp_path / "a.txt").exists() and (tmp_path / "sub" / "b.txt").exists()


async def test_build_config(monkeypatch: pytest.MonkeyPatch) -> None:
    class DB:
        async def get(self, model, sid):
            return None if sid == 1 else SimpleNamespace(status=1)
    assert await E._build_config(DB(), 1) is None
    assert await E._build_config(DB(), 2) is None


async def test_run_step_errors_and_success(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    class DB:
        async def commit(self): pass
    class Adapter:
        def __init__(self): self.uploaded=[]; self.closed=False
        async def upload(self, local, remote): self.uploaded.append((local, remote))
        async def close(self): self.closed=True
    adapter = Adapter()
    class Factory:
        @staticmethod
        def create(cfg): return adapter
    monkeypatch.setattr(E, "StorageAdapterFactory", Factory)
    monkeypatch.setattr(E, "_load_steps", AsyncMock(return_value=[]))
    monkeypatch.setattr(E, "_broadcast", AsyncMock())
    async def build(db, sid): return SimpleNamespace(transfer_mode=None, multipart_part_size=None, multipart_concurrency=None) if sid == 9 else None
    monkeypatch.setattr(E, "_build_config", build)
    def task(): return SimpleNamespace(id=1, status="running", total_size=10, transferred_size=0, speed=0.0, progress=0, error_msg=None, finished_at=None)
    def step(**kw):
        base = dict(source_id=None, source_path=str(tmp_path / "missing"), target_id=9, target_path="out/a.txt", status="pending", started_at=None, progress=0, total_size=0, transferred_size=0, speed=0, error_msg=None, finished_at=None, step_order=0, transfer_mode=None, multipart_part_size=None, multipart_concurrency=None)
        base.update(kw); return SimpleNamespace(**base)
    t = task(); s = step()
    assert await E._run_step(DB(), t, s) is False
    f = tmp_path / "a.txt"; f.write_text("hello")
    t2 = task(); s2 = step(source_path=str(f))
    assert await E._run_step(DB(), t2, s2) is True
    assert adapter.uploaded and s2.status == "success"
    t3 = task(); s3 = step(source_path=str(f), target_id=8)
    assert await E._run_step(DB(), t3, s3) is False
