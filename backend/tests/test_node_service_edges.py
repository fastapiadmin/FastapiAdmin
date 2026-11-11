"""定时任务节点服务错误/运行时分支。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import CustomException
from app.modules.task.cronjob.node.service import NodeService


def _svc():
    return NodeService(SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True)), None)


async def test_create_none(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a): pass
        async def get(self, **k): return None
        async def create_obj_crud(self, **k): return None
    monkeypatch.setattr("app.modules.task.cronjob.node.service.NodeCRUD", C)
    with pytest.raises(CustomException):
        await _svc().create(SimpleNamespace(trigger=None, trigger_args=None, code=None, name="x"))


async def test_update_invalid_trigger_and_none(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a): pass
        async def get_obj_by_id_crud(self, **k): return SimpleNamespace(id=1)
        async def update_obj_crud(self, **k): return None
    monkeypatch.setattr("app.modules.task.cronjob.node.service.NodeCRUD", C)
    with pytest.raises(Exception):
        await _svc().update(1, SimpleNamespace(trigger="bad", trigger_args="bad"))
    with pytest.raises(CustomException):
        await _svc().update(1, SimpleNamespace(trigger=None, trigger_args=None))


def test_run_once_empty_func() -> None:
    from app.modules.task.cronjob.node.service import run_node_once
    with pytest.raises(ValueError):
        run_node_once(SimpleNamespace(func=""))
