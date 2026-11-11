"""用户/JWT/分页/存储源/菜单 schema 校验边缘。"""

from __future__ import annotations

import pytest

from app.core.base_schema import JWTPayloadSchema, PaginationQueryParam


def test_user_schema_validators() -> None:
    from app.modules.system.user.schema import UserCreateSchema, UserForgetPasswordSchema, UserRegisterSchema, UserUpdateSchema
    with pytest.raises(Exception):
        UserCreateSchema(username="abc", password="Abc123!x", name="n", avatar="ftp://x")
    with pytest.raises(Exception):
        UserCreateSchema(username="abc", password="Abc123!x", name="x" * 33)
    with pytest.raises(Exception):
        UserForgetPasswordSchema(username=" ")
    with pytest.raises(Exception):
        UserForgetPasswordSchema(username="1bad")
    with pytest.raises(Exception):
        UserRegisterSchema(username="1bad", password="Abc123!x")
    assert UserUpdateSchema(username=None, password=None, name=None) is not None
    with pytest.raises(Exception):
        UserUpdateSchema(username="1bad")


def test_base_schema_validators() -> None:
    with pytest.raises(Exception):
        JWTPayloadSchema(sub=" ", exp=1)
    assert PaginationQueryParam(order_by='[{"id":"asc"}]').order_by
    assert PaginationQueryParam(order_by=[{"id": "asc"}]).order_by
    with pytest.raises(Exception):
        PaginationQueryParam(order_by="bad")
    with pytest.raises(Exception):
        PaginationQueryParam(order_by="{}")
    with pytest.raises(Exception):
        PaginationQueryParam(order_by=1)


def test_node_schema_validators() -> None:
    from app.modules.task.storage.node.schema import StorageNodeCreateSchema
    with pytest.raises(Exception):
        StorageNodeCreateSchema(name="x", protocol="s3", advanced_config={"signature_version": "bad"})
    with pytest.raises(Exception):
        StorageNodeCreateSchema(name="x", protocol="s3", host="h", endpoint="https://x")
    with pytest.raises(Exception):
        StorageNodeCreateSchema(name="x", protocol="local")
    with pytest.raises(Exception):
        StorageNodeCreateSchema(name="x", protocol="s3", host="h", bucket="b")
    with pytest.raises(Exception):
        StorageNodeCreateSchema(name="x", protocol="cos", host="h", bucket="b", endpoint="https://x")
    with pytest.raises(Exception):
        StorageNodeCreateSchema(name="x", protocol="cos", host="h", bucket="b", endpoint="https://x", region="r", advanced_config={"appid": "abc"})
    node = StorageNodeCreateSchema(name="x", protocol="ftps", host="h", encrypt_type=3)
    assert node.is_secure is True
    with pytest.raises(Exception):
        StorageNodeCreateSchema(name=" ", protocol="local", host="h")
