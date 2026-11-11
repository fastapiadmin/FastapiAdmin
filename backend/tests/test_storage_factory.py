"""存储适配器工厂协议映射。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.task.storage.core.factory import StorageAdapterFactory


def test_unsupported_protocol() -> None:
    with pytest.raises(CustomException, match="不支持"):
        StorageAdapterFactory.create(SimpleNamespace(protocol=SimpleNamespace(value="bad")))


def test_factory_creates_local(tmp_path) -> None:
    from app.modules.task.storage.core.base import StorageAdapterConfig, StorageProtocol
    from app.modules.task.storage.core.local_adapter import LocalStorageAdapter
    cfg = StorageAdapterConfig(protocol=StorageProtocol.LOCAL, port=0, host=str(tmp_path))
    assert isinstance(StorageAdapterFactory.create(cfg), LocalStorageAdapter)


def test_factory_s3_requires_credentials() -> None:
    from app.modules.task.storage.core.base import StorageAdapterConfig, StorageProtocol
    cfg=StorageAdapterConfig(protocol=StorageProtocol.S3,port=443,bucket="b",username="",password="x")
    with pytest.raises(CustomException, match="AccessKeyId"):
        StorageAdapterFactory.create(cfg)


def test_factory_s3_requires_bucket() -> None:
    from app.modules.task.storage.core.base import StorageAdapterConfig, StorageProtocol
    cfg=StorageAdapterConfig(protocol=StorageProtocol.S3,port=443,bucket="",username="a",password="x")
    with pytest.raises(CustomException, match="bucket"):
        StorageAdapterFactory.create(cfg)


def test_factory_s3_requires_secret() -> None:
    from app.modules.task.storage.core.base import StorageAdapterConfig, StorageProtocol
    cfg=StorageAdapterConfig(protocol=StorageProtocol.S3,port=443,bucket="b",username="a",password="")
    with pytest.raises(CustomException, match="AccessKeyId"):
        StorageAdapterFactory.create(cfg)
