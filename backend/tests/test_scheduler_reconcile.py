"""节点任务自愈：补注册/移除/跳过。"""

from __future__ import annotations

from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest

import app.core.ap_scheduler as S
import app.modules.task.cronjob.node.service as node_service


class _Session:
    def __init__(self, nodes): self.nodes = nodes
    async def execute(self, *a, **k): return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: self.nodes))
    async def __aenter__(self): return self
    async def __aexit__(self, *a): return False


async def test_reconcile(monkeypatch: pytest.MonkeyPatch) -> None:
    future = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    past = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    nodes = [
        SimpleNamespace(id=1, status=0, trigger="cron", trigger_args="0 * * * * ? *", func="builtin:ok", name="a"),
        SimpleNamespace(id=2, status=0, trigger="date", trigger_args=past, func="builtin:ok", name="b"),
        SimpleNamespace(id=3, status=1, trigger="cron", trigger_args="0 * * * * ? *", func="builtin:ok", name="c"),
        SimpleNamespace(id=4, status=0, trigger="date", trigger_args=future, func="builtin:ok", name="d"),
    ]
    registered = []; removed = []
    import app.core.database as db_mod
    monkeypatch.setattr(db_mod, "async_db_session", lambda: _Session(nodes))
    monkeypatch.setattr(S.SchedulerUtil, "get_jobs", classmethod(lambda cls: [SimpleNamespace(id="99")]))
    monkeypatch.setattr(S.SchedulerUtil, "remove_job", classmethod(lambda cls, jid: removed.append(jid)))
    monkeypatch.setattr(S.SchedulerUtil, "describe_schedulability", classmethod(lambda cls, code: (True, None)))
    monkeypatch.setattr(S.SchedulerUtil, "log_unschedulable_jobs", classmethod(lambda cls, **k: []))
    monkeypatch.setattr(node_service, "register_node_job", lambda node: registered.append(node.id))
    await S.SchedulerUtil.reconcile_node_jobs()
    assert 1 in registered and 4 in registered and 2 not in registered and 3 not in registered
    assert "99" in removed
