"""StorageFileService 校验/上传/下载/删除/目录操作（fake adapter）。"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest
from starlette.datastructures import UploadFile

from app.core.exceptions import CustomException
from app.modules.task.storage.browse.service import StorageFileService
from app.modules.task.storage.core.base import StorageObject, StoragePage


class FakeAdapter:
    def __init__(self, entries=None):
        self.entries = entries or []
        self.uploaded = []
        self.deleted = []
        self.closed = False
        self.url = "https://url"

    async def upload(self, local, remote):
        self.uploaded.append((Path(local).read_bytes(), remote))

    async def get_url(self, remote, expire=3600):
        return self.url

    async def download(self, remote, local):
        Path(local).write_bytes(b"data")
        return local

    async def delete(self, remote):
        self.deleted.append(remote)

    async def delete_dir(self, remote):
        self.deleted.append("dir:" + remote)

    async def exists(self, remote):
        return True

    async def list_files(self, prefix, page_size=None, cursor=None):
        return StoragePage(items=self.entries, has_next=False, next_cursor=None) if page_size is not None else self.entries

    async def rename(self, src, dst):
        self.deleted.append((src, dst))

    async def mkdir(self, path):
        self.deleted.append("mkdir:" + path)

    async def close(self):
        self.closed = True


def _service(adapter):
    svc = StorageFileService.__new__(StorageFileService)
    async def _get_adapter(source_id, bucket=None):
        return adapter
    svc._get_adapter = _get_adapter  # type: ignore[method-assign]
    return svc


def test_validate_remote_path() -> None:
    assert StorageFileService._validate_remote_path("/a//b/.") == "a/b"
    with pytest.raises(CustomException):
        StorageFileService._validate_remote_path("")
    with pytest.raises(CustomException):
        StorageFileService._validate_remote_path("../x")
    with pytest.raises(CustomException):
        StorageFileService._validate_remote_path("a\x00b")


async def test_upload_valid_and_invalid(tmp_path: Path) -> None:
    a = FakeAdapter()
    svc = _service(a)
    f = UploadFile(filename="a.txt", file=BytesIO(b"x"))
    r = await svc.upload(None, f, "dir/")
    assert r.file_path == "dir/a.txt" and a.uploaded[0][1] == "dir/a.txt"
    assert a.closed is True

    with pytest.raises(CustomException):
        await svc.upload(None, UploadFile(filename="a.exe", file=BytesIO(b"x")))
    with pytest.raises(CustomException):
        await svc.upload(None, UploadFile(filename="a", file=BytesIO(b"x")))
    with pytest.raises(CustomException):
        await svc.upload(None, UploadFile(filename="../a.txt", file=BytesIO(b"x")))


async def test_download_delete_list_rename_mkdir_share(tmp_path: Path) -> None:
    a = FakeAdapter(entries=[StorageObject(name="d", key="d", is_dir=True)])
    svc = _service(a)
    local, name = await svc.download(None, "a.txt")
    assert Path(local).read_bytes() == b"data" and name == "a.txt"
    await svc.delete(None, "d")
    assert a.deleted == ["dir:d"]
    assert await svc.exists(None, "x") is True
    assert (await svc.list_files(None, "d")) == a.entries
    assert isinstance(await svc.list_files(None, "d", page_size=10), StoragePage)
    await svc.rename(None, "a", "b")
    await svc.mkdir(None, "new")
    assert await svc.share(None, "a") == "https://url"
    assert a.closed is True


async def test_zip_directory(tmp_path: Path) -> None:
    root = tmp_path / "root"
    (root / "sub").mkdir(parents=True)
    (root / "a.txt").write_text("a")
    (root / "sub" / "b.txt").write_text("b")
    zip_path = tmp_path / "out.zip"
    StorageFileService._zip_directory(root, str(zip_path), root)
    assert zip_path.exists() and zip_path.stat().st_size > 0


async def test_delete_fallback_and_bucket_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    class A(FakeAdapter):
        async def list_files(self,prefix,page_size=None,cursor=None): raise RuntimeError()
        async def delete(self,remote): raise RuntimeError()
        async def delete_dir(self,remote): self.deleted.append("dir:"+remote)
    a=A(); s=_service(a)
    await s.delete(None,"x")
    assert "dir:x" in a.deleted
    async def source(_sid):
        from app.modules.task.storage.core.base import StorageAdapterConfig, StorageProtocol
        return StorageAdapterConfig(protocol=StorageProtocol.LOCAL,port=0,host="/tmp")
    s._get_source=source
    assert await s.list_buckets(None) == []
    for bad in ("","   ","x"*64,"a/b","a b"):
        with pytest.raises(CustomException):
            await s.create_bucket(None,bad)
