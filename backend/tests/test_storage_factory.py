"""存储适配器工厂协议映射。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.task.storage.core.factory import StorageAdapterFactory


def test_unsupported_protocol() -> None:
    with pytest.raises(CustomException, match="不支持"):
        StorageAdapterFactory.create(SimpleNamespace(protocol=SimpleNamespace(value="bad")))
