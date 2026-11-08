"""存储基类配置/端点/高级字段覆盖。"""

from __future__ import annotations

from app.modules.task.storage.core.base import (
    ADVANCED_FIELD_DEFS,
    StorageObject,
    StoragePage,
    StorageProtocol,
    decrypt_password,
    encrypt_password,
    normalize_endpoint,
    parse_advanced_config,
)


def test_endpoint_and_password() -> None:
    assert normalize_endpoint(None) is None
    assert normalize_endpoint("") == ""
    assert normalize_endpoint("s3.example.com") == "https://s3.example.com"
    assert normalize_endpoint("s3.example.com", "http") == "http://s3.example.com"
    assert normalize_endpoint("http://x") == "http://x"
    token = encrypt_password("secret")
    assert decrypt_password(token) == "secret"
    assert encrypt_password(None) == ""
    assert decrypt_password(None) == ""


def test_advanced_config_and_field_defs() -> None:
    assert parse_advanced_config(StorageProtocol.LOCAL, {}) is None
    s3 = parse_advanced_config(StorageProtocol.S3, {"addressing_style": "path"})
    assert s3 is not None and s3.addressing_style == "path"
    assert "s3" in ADVANCED_FIELD_DEFS
    keys = {d.key: d for d in ADVANCED_FIELD_DEFS["s3"]}
    assert keys["addressing_style"].type == "select"
    assert keys["signature_version"].options


def test_storage_object_page() -> None:
    o = StorageObject(name="a", key="a", size=1)
    p = StoragePage(items=[o], has_next=True, next_cursor="c")
    assert p.items[0].name == "a" and p.has_next is True


def test_adapter_bucket_and_multipart() -> None:
    from app.core.exceptions import CustomException
    from app.modules.task.storage.core.base import BaseStorageAdapter, StorageAdapterConfig
    cfg=StorageAdapterConfig(protocol=StorageProtocol.S3,port=443,bucket="b",username="u",password="p")
    a=BaseStorageAdapter.__new__(StorageAdapter); a.config=cfg; a.bucket_name=cfg.bucket
    assert a._require_bucket()=="b"
    a.set_bucket("b2"); assert a.bucket_name=="b2"
    a.bucket_name=""
    try:
        a._require_bucket()
    except CustomException:
        pass
    else:
        raise AssertionError("expected")
    cfg.multipart_part_size=50; cfg.multipart_concurrency=6; cfg.multipart_memory_budget=512
    assert a._multipart_settings()==(50*1024*1024,6,True)
    cfg.transfer_mode="stream"
    assert a._multipart_settings()[2] is False


def test_entries_from_keys() -> None:
    from app.modules.task.storage.core.base import BaseStorageAdapter
    items=BaseStorageAdapter._entries_from_keys(["a/b/","a/b/c","a/d","a/b",""])
    assert [x.key for x in items if x.is_dir]==["a","a/b"]
    assert [x.key for x in items if not x.is_dir]==["a/b/c","a/d"]
