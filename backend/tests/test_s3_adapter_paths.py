"""S3 适配器非网络分支测试（fakes client）。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.task.storage.core.s3_adapter import S3StorageAdapter


class FakeClient:
    def __init__(self):
        self.calls = []
        self.objects = {
            "Contents": [
                {"Key": "dir/a.txt", "Size": 1},
                {"Key": "dir/", "Size": 0},
            ],
            "CommonPrefixes": [{"Prefix": "dir/sub/"}],
            "IsTruncated": False,
        }

    def head_bucket(self, **kw):
        self.calls.append(("head_bucket", kw))

    def head_object(self, **kw):
        self.calls.append(("head_object", kw))

    def upload_file(self, *args, **kw):
        self.calls.append(("upload_file", args))

    def download_file(self, *args, **kw):
        self.calls.append(("download_file", args))

    def put_object(self, **kw):
        self.calls.append(("put_object", kw))

    def delete_object(self, **kw):
        self.calls.append(("delete_object", kw))

    def list_objects_v2(self, **kw):
        self.calls.append(("list_objects_v2", kw))
        return self.objects

    def list_buckets(self):
        return {"Buckets": [{"Name": "a"}, {"Name": ""}]}

    def create_bucket(self, **kw):
        self.calls.append(("create_bucket", kw))

    def generate_presigned_url(self, *args, **kwargs):
        return "https://url"

    def copy_object(self, **kw):
        self.calls.append(("copy_object", kw))

    def close(self):
        self.calls.append(("close", {}))


def _a(config=None):
    a = S3StorageAdapter.__new__(S3StorageAdapter)
    a.config = SimpleNamespace(bucket="b", region="eu-west-1", **(config or {}))
    a.bucket_name = "b"
    a.client = FakeClient()
    return a


def test_s3_connection_and_bucket_operations() -> None:
    a = _a()
    assert a._sync_test_connection() is True
    assert a._sync_exists("x") is True
    assert a._sync_list_buckets() == ["a"]
    a._sync_create_bucket("new")
    assert a.client.calls[-1][1]["CreateBucketConfiguration"] == {"LocationConstraint": "eu-west-1"}
    a._sync_mkdir("d")
    a._sync_rmdir("d")
    a._sync_delete("x")
    assert a._sync_get_url("x", 10) == "https://url"
    a._sync_close()


def test_s3_listing_and_page() -> None:
    a = _a()
    items = a._sync_list("dir/")
    assert {x.name for x in items} == {"a.txt", "sub"}
    page = a._sync_list_page("dir/", 10, "cur")
    assert page.items and page.has_next is False
    assert "ContinuationToken" not in page.__dict__


def test_s3_copy_file_and_rename_file() -> None:
    a = _a()
    a._is_dir = lambda key: False  # type: ignore[method-assign]
    a._sync_copy("a", "b")
    a._sync_rename("a", "b")
    assert any(c[0] == "copy_object" for c in a.client.calls)


def test_s3_directory_copy_uses_base() -> None:
    a = _a()
    a._is_dir = lambda key: True  # type: ignore[method-assign]
    called = []
    a._sync_copy_dir = lambda src, dst: called.append((src, dst))  # type: ignore[method-assign]
    a._sync_copy("a/", "b/")
    assert called == [("a/", "b/")]


def test_s3_validation_errors() -> None:
    from app.modules.task.storage.core.base import StorageAdapterConfig, StorageProtocol
    with pytest.raises(CustomException):
        S3StorageAdapter(StorageAdapterConfig(protocol=StorageProtocol.S3, port=0, bucket="b", username="", password="x"))
    with pytest.raises(CustomException):
        S3StorageAdapter(StorageAdapterConfig(protocol=StorageProtocol.S3, port=0, bucket="", username="a", password="x"))


def test_s3_upload_download_delete(monkeypatch: pytest.MonkeyPatch) -> None:
    a=_a()
    a._multipart_settings=lambda: (5*1024*1024, 2, True)
    import app.modules.task.storage.core.s3_adapter as mod
    from types import SimpleNamespace
    monkeypatch.setattr(mod, "boto_transfer", SimpleNamespace(TransferConfig=lambda **kw: kw))
    assert a._sync_upload("/tmp/a", "a") == "a"
    assert a._sync_download("a", "/tmp/a") == "/tmp/a"
    a._sync_delete("a")
    assert any(c[0]=="upload_file" for c in a.client.calls)


def test_s3_create_bucket_error(monkeypatch: pytest.MonkeyPatch) -> None:
    a=_a()
    def fail(**kw): raise RuntimeError("x")
    a.client.create_bucket=fail
    with pytest.raises(CustomException):
        a._sync_create_bucket("b")
