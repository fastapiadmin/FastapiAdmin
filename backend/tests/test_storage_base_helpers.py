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
