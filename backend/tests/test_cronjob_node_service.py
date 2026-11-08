"""定时任务节点服务基础分支。"""

from __future__ import annotations

import pytest
from types import SimpleNamespace

import app.modules.task.cronjob.node.service as mod
from app.core.exceptions import CustomException
from app.modules.task.cronjob.node.schema import NodeCreateSchema
from app.modules.task.cronjob.node.service import NodeService


def _svc(crud):
    monkeypatch = pytest.MonkeyPatch(); monkeypatch.setattr(mod, "NodeCRUD", lambda *a: crud)
    s = NodeService.__new__(NodeService); s.auth = object(); s.db = object()
    return s, monkeypatch


async def test_options_and_detail_missing() -> None:
    class C:
        async def get_obj_list_crud(self): return []
        async def get_obj_by_id_crud(self, **kw): return None
    s, m = _svc(C())
    try:
        assert await s.options() == []
        with pytest.raises(CustomException, match="不存在"):
            await s.detail(1)
    finally:
        m.undo()


async def test_create_duplicate_and_invalid_trigger() -> None:
    class C:
        async def get(self, **kw): return SimpleNamespace(id=1)
    s, m = _svc(C())
    try:
        with pytest.raises(CustomException, match="已存在"):
            await s.create(NodeCreateSchema(name="n", func="builtin:x"))
    finally:
        m.undo()
    class C2:
        async def get(self, **kw): return None
    s, m = _svc(C2())
    try:
        with pytest.raises(Exception):
            NodeCreateSchema(name="n", func="builtin:x", trigger="cron", trigger_args="bad")
    finally:
        m.undo()


async def test_batch_set_status_empty() -> None:
    class C: ...
    s, m = _svc(C())
    try:
        with pytest.raises(CustomException, match="请选择"):
            await s.batch_set_status([], 0)
    finally:
        m.undo()
