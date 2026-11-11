"""调度器剩余分支：init/maintain/reconcile/finish。"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import app.core.ap_scheduler as S


async def test_init_scheduler_logs(monkeypatch: pytest.MonkeyPatch) -> None:
    with patch.object(S.SchedulerUtil, "_ensure_scheduler_running", new=AsyncMock(return_value=True)):
        await S.SchedulerUtil.init_scheduler(object())
    with patch.object(S.SchedulerUtil, "_ensure_scheduler_running", new=AsyncMock(return_value=False)):
        await S.SchedulerUtil.init_scheduler(None)
    with patch.object(S.SchedulerUtil, "_ensure_scheduler_running", new=AsyncMock(side_effect=RuntimeError("x"))):
        with pytest.raises(RuntimeError):
            await S.SchedulerUtil.init_scheduler(None)


async def test_ensure_running_shortcuts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(S, "scheduler", SimpleNamespace(running=True))
    assert await S.SchedulerUtil._ensure_scheduler_running() is True
    monkeypatch.setattr(S.SchedulerUtil, "_redis", None)
    await S.SchedulerUtil._maintain_loop()


async def test_spawn_reconcile_existing(monkeypatch: pytest.MonkeyPatch) -> None:
    task = SimpleNamespace(done=lambda: False)
    monkeypatch.setattr(S.SchedulerUtil, "_reconcile_task", task)
    S.SchedulerUtil._spawn_reconcile()
    assert S.SchedulerUtil._reconcile_task is task


async def test_reconcile_error_branches(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    from datetime import datetime, timedelta
    future = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    nodes = [
        SimpleNamespace(id=1, status=0, trigger="date", trigger_args="bad", func="builtin:x", name="bad-date"),
        SimpleNamespace(id=2, status=0, trigger="date", trigger_args=future, func="builtin:x", name="reg-fail"),
        SimpleNamespace(id=3, status=0, trigger="cron", trigger_args="0 * * * * ? *", func="bad", name="unsched"),
    ]
    class Ses:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def execute(self, *a, **k):
            return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: nodes))
    import app.core.database as db
    monkeypatch.setattr(db, "async_db_session", lambda: Ses())
    monkeypatch.setattr(S.SchedulerUtil, "get_jobs", classmethod(lambda cls: [SimpleNamespace(id="99")]))
    def remove(_): raise RuntimeError("x")
    monkeypatch.setattr(S.SchedulerUtil, "remove_job", remove)
    def reg(node):
        if node.id == 2: raise RuntimeError("x")
    import app.modules.task.cronjob.node.service as ns
    monkeypatch.setattr(ns, "register_node_job", reg)
    monkeypatch.setattr(S.SchedulerUtil, "describe_schedulability", classmethod(lambda cls, code: (code != "bad", "bad")))
    monkeypatch.setattr(S.SchedulerUtil, "log_unschedulable_jobs", classmethod(lambda cls, **k: []))
    await S.SchedulerUtil.reconcile_node_jobs()


def test_finish_job_error_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(S.SchedulerUtil, "get_job", classmethod(lambda cls, job_id=None: (_ for _ in ()).throw(RuntimeError("x"))))
    monkeypatch.setattr(S.SchedulerUtil, "_is_temp_job_id", staticmethod(lambda jid: True))
    monkeypatch.setattr(S.SchedulerUtil, "_record_job_log", staticmethod(lambda r: (_ for _ in ()).throw(RuntimeError("log"))))
    monkeypatch.setattr(S.SchedulerUtil, "remove_job", classmethod(lambda cls, job_id: (_ for _ in ()).throw(RuntimeError("rm"))))
    S.SchedulerUtil._finish_job_record(job_id="1:manual:x", status=1, detail="e")
