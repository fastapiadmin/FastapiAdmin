"""在线用户/字典 CRUD/日志清理处理器。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.modules.system.dict.crud import DictDataCRUD
from app.modules.task.cronjob.node.handlers.system_log import cleanup_expired_logs


async def test_dict_batch_delete_and_type_list() -> None:
    auth = SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True))
    c = DictDataCRUD(auth, None)
    c.get_list = AsyncMock(return_value=[SimpleNamespace(id=1)])
    c.delete = AsyncMock()
    assert await c.batch_delete([1, 2]) == 1
    assert await c.batch_delete([2], exclude_system=False) == 1


def test_cleanup_expired_logs_guard() -> None:
    with pytest.raises(ValueError):
        cleanup_expired_logs(0)


def test_cleanup_expired_logs_real() -> None:
    out = cleanup_expired_logs(1)
    assert set(out) == {"days", "operation_deleted", "login_deleted"}


async def test_online_controller(test_client, auth_headers) -> None:
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/online/list")).rsplit("/list", 1)[0]
    assert test_client.get(f"{base}/list", headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/current", headers=auth_headers).status_code == 200
    assert test_client.get(f"{base}/stats", headers=auth_headers).status_code == 200
    assert test_client.request("DELETE", f"{base}/delete", json="badtoken", headers=auth_headers).status_code in (200, 400, 422)
