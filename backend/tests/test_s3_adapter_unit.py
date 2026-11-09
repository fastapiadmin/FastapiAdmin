"""S3 适配器对象操作（fake boto3 客户端，无需真实 MinIO）。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.modules.task.storage.core.s3_adapter import S3StorageAdapter


def _adapter(client):
    a = object.__new__(S3StorageAdapter)
    a.config = SimpleNamespace(bucket="b", region="us-east-1", endpoint="http://x", scheme="http")
    a.bucket_name = "b"
    a.client = client
    return a


class Client:
    def __init__(self, **kw):
        self.__dict__.update(kw); self.calls = []
    def head_bucket(self, **kw): return {}
    def head_object(self, **kw):
        if getattr(self, "missing", False): raise Exception("x")
        return {}
    def list_objects_v2(self, **kw):
        self.calls.append(kw)
        return {"CommonPrefixes": [{"Prefix": "a/"}, {"Prefix": "a/"}], "Contents": [{"Key": "a", "Size": 1}, {"Key": "a/", "Size": 0}, {"Key": "a/f", "Size": 2}, {"Key": "a/f", "Size": 2}], "IsTruncated": False}
    def list_buckets(self): return {"Buckets": [{"Name": "b"}, {}]}
    def create_bucket(self, **kw): self.created = kw
    def generate_presigned_url(self, *a, **k): return "url"
    def close(self): self.closed = True
    def put_object(self, **kw): self.put = kw
    def delete_object(self, **kw): self.deleted = kw
    def copy_object(self, **kw): self.copied = kw
    def get_paginator(self, name): return SimpleNamespace(paginate=lambda **k: [{"Contents": [{"Key": "a/x"}]}])
    def delete_objects(self, **kw): self.batch = kw


def test_test_connection_branches() -> None:
    assert _adapter(Client())._sync_test_connection() is True
    class Bad:
        def head_bucket(self, **kw):
            from botocore.exceptions import ClientError
            raise ClientError({"Error": {"Code": "403"}}, "op")
    assert _adapter(Bad())._sync_test_connection() is True
    class Bad2:
        def head_bucket(self, **kw): raise RuntimeError("x")
    assert _adapter(Bad2())._sync_test_connection() is False


def test_list_pagination_and_objects() -> None:
    a = _adapter(Client())
    objs = a._sync_list("a/")
    assert "f" in [o.name for o in objs]
    page = a._sync_list_page("a/", 10, None)
    assert page.items and page.has_next is False
    assert a._sync_list_buckets() == ["b"]


def test_bucket_create_and_url_and_close() -> None:
    c = Client(); a = _adapter(c)
    a._sync_create_bucket("b")
    assert c.created["Bucket"] == "b"
    assert a._sync_get_url("k", 60) == "url"
    a._sync_close()
    assert c.closed is True


def test_dir_operations() -> None:
    c = Client(); a = _adapter(c)
    assert a._is_dir("a/") is True
    a._sync_mkdir("a"); assert c.put["Key"] == "a/"
    a._sync_rmdir("a"); assert c.deleted["Key"] == "a/"
    a._sync_mkdir("b")
    assert c.put["Key"] == "b/"
    assert a._sync_list_recursive("a/")
    a._sync_delete_dir("a/")
    assert c.batch["Delete"]["Quiet"] is True
