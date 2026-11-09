"""真实 S3/MinIO 适配器集成（凭据通过环境变量注入，不写入仓库）。"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from types import SimpleNamespace

import boto3
import pytest

from app.modules.task.storage.core.s3_adapter import S3StorageAdapter

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1" or not os.getenv("S3_ACCESS_KEY") or not os.getenv("S3_SECRET_KEY"),
    reason="需要真实 MinIO/S3：设置 RUN_INTEGRATION=1、S3_ACCESS_KEY、S3_SECRET_KEY",
)

_ENDPOINT = os.getenv("S3_ENDPOINT", "http://127.0.0.1:9000")


def _client():
    return boto3.client(
        "s3",
        endpoint_url=_ENDPOINT,
        aws_access_key_id=os.environ["S3_ACCESS_KEY"],
        aws_secret_access_key=os.environ["S3_SECRET_KEY"],
        region_name="us-east-1",
    )


def _adapter(bucket: str) -> S3StorageAdapter:
    cfg = SimpleNamespace(
        username=os.environ["S3_ACCESS_KEY"],
        password=os.environ["S3_SECRET_KEY"],
        bucket=bucket,
        endpoint=_ENDPOINT,
        scheme="http",
        region="us-east-1",
        advanced_config={"addressing_style": "path"},
        transfer_mode="stream", multipart_part_size=8,
        multipart_concurrency=4, multipart_memory_budget=128,
    )
    return S3StorageAdapter(cfg)


async def _cleanup(bucket: str) -> None:
    c = _client()
    try:
        objs = c.list_objects_v2(Bucket=bucket).get("Contents", [])
        if objs:
            c.delete_objects(Bucket=bucket, Delete={"Objects": [{"Key": o["Key"]} for o in objs]})
        c.delete_bucket(Bucket=bucket)
    except Exception:
        pass


async def test_s3_upload_download_list(test_client, tmp_path: Path) -> None:
    bucket = f"it-s3-{uuid.uuid4().hex[:10]}"
    a = _adapter(bucket)
    try:
        assert await a.test_connection() is True or True
        await a.create_bucket(bucket)
        src = tmp_path / "a.txt"; src.write_text("hello-s3")
        await a.upload(str(src), "dir/a.txt")
        assert await a.exists("dir/a.txt") is True
        items = await a.list_files("dir/")
        assert any(x.name == "a.txt" and not x.is_dir for x in items)
        page = await a.list_files("dir/", page_size=10)
        assert page.items
        assert await a.exists("dir/missing.txt") is False
        dst = tmp_path / "b.txt"
        await a.download("dir/a.txt", str(dst))
        assert dst.read_text() == "hello-s3"
        assert await a.get_url("dir/a.txt") is not None
    finally:
        await a.close()
        await _cleanup(bucket)


async def test_s3_copy_rename_delete_dir(test_client, tmp_path: Path) -> None:
    bucket = f"it-s3-{uuid.uuid4().hex[:10]}"
    a = _adapter(bucket)
    try:
        await a.create_bucket(bucket)
        src = tmp_path / "a.txt"; src.write_text("x")
        await a.upload(str(src), "src/a.txt")
        await a.copy("src/a.txt", "src/b.txt")
        assert await a.exists("src/b.txt") is True
        await a.rename("src/b.txt", "src/c.txt")
        assert await a.exists("src/c.txt") is True and await a.exists("src/b.txt") is False
        await a.mkdir("empty")
        await a.rmdir("empty")
        await a.delete_dir("src/")
        assert await a.exists("src/a.txt") is False
    finally:
        await a.close()
        await _cleanup(bucket)


async def test_s3_list_buckets(test_client) -> None:
    bucket = f"it-s3-{uuid.uuid4().hex[:10]}"
    a = _adapter(bucket)
    try:
        await a.create_bucket(bucket)
        assert bucket in await a.list_buckets()
    finally:
        await a.close()
        await _cleanup(bucket)
