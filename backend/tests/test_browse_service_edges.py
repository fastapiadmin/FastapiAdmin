"""存储浏览服务错误/桶切换分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.modules.task.storage.browse.service import StorageFileService


class FakeAdapter:
    def __init__(self):
        self.bucket = None
        self.deleted = []
    def set_bucket(self, b): self.bucket = b
    async def upload(self, local, remote): return remote
    async def get_url(self, remote): return "http://x"
    async def download(self, remote, local):
        open(local, "w").write("x")
        return local
    async def delete(self, remote): self.deleted.append(remote)
    async def list_files(self, p): return []
    async def close(self): pass


def _svc():
    return StorageFileService(SimpleNamespace(user=SimpleNamespace(id=1)), None)


class F:
    filename = "a.txt"
    size = 1
    def __init__(self): self.done = False
    async def read(self, n=-1):
        if self.done: return b""
        self.done = True; return b"x"
    async def seek(self, p): self.done = False


async def test_upload_without_path(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = _svc(); a = FakeAdapter()
    async def get(*args, **kw): return a
    monkeypatch.setattr(svc, "_get_adapter", get)
    out = await svc.upload(source_id=None, file=F(), remote_path=None)
    assert out.file_name.endswith(".txt")


async def test_download_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class Bad(FakeAdapter):
        async def download(self, remote, local): raise RuntimeError("x")
    svc = _svc(); a = Bad()
    async def get(*args, **kw): return a
    monkeypatch.setattr(svc, "_get_adapter", get)
    with pytest.raises(RuntimeError):
        await svc.download(None, "a.txt")


async def test_copy_bucket_and_move(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = _svc(); a = FakeAdapter()
    async def get_source(sid): return SimpleNamespace(protocol="local")
    monkeypatch.setattr(svc, "_get_source", get_source)
    import app.modules.task.storage.browse.service as m
    monkeypatch.setattr(m, "StorageAdapterFactory", SimpleNamespace(create=lambda cfg: a))
    await svc.copy_or_move(source_id=1, source_path="a", target_id=1, target_path="b", move=True, bucket="bk")
    assert a.bucket == "bk" and a.deleted == ["a"]
