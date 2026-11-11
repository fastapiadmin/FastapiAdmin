"""调度器锁丢失/停止/触发类型边缘。"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

import app.core.ap_scheduler as S


async def test_maintain_lock_lost(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []
    class C:
        def __init__(self, redis): pass
        async def renew_lock(self, **k): return False
        async def get(self, **k): return "other"
    monkeypatch.setattr("app.core.redis_crud.RedisCURD", C)
    monkeypatch.setattr(S.SchedulerUtil, "_redis", object())
    monkeypatch.setattr(S.SchedulerUtil, "_leader_token", "t")
    monkeypatch.setattr(S.SchedulerUtil, "_stop_scheduler_local", classmethod(lambda cls: calls.append("stop")))
    async def sleep(_):
        if calls: raise asyncio.CancelledError
        calls.append("sleep")
    monkeypatch.setattr(asyncio, "sleep", sleep)
    with pytest.raises(asyncio.CancelledError):
        await S.SchedulerUtil._maintain_loop()
    assert "stop" in calls


async def test_maintain_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, redis): pass
        async def renew_lock(self, **k): raise RuntimeError("x")
    monkeypatch.setattr("app.core.redis_crud.RedisCURD", C)
    monkeypatch.setattr(S.SchedulerUtil, "_redis", object())
    monkeypatch.setattr(S.SchedulerUtil, "_leader_token", "t")
    async def sleep(_): return None
    monkeypatch.setattr(asyncio, "sleep", sleep)
    await S.SchedulerUtil._maintain_loop()


def test_start_local_running(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(S, "scheduler", SimpleNamespace(running=True))
    S.SchedulerUtil._start_scheduler_local()


def test_spawn_maintain_existing(monkeypatch: pytest.MonkeyPatch) -> None:
    task = SimpleNamespace(done=lambda: False)
    monkeypatch.setattr(S.SchedulerUtil, "_maintain_task", task)
    S.SchedulerUtil._spawn_maintain()
    assert S.SchedulerUtil._maintain_task is task


def test_trigger_type_manual(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(S.SchedulerUtil, "get_job", classmethod(lambda cls, job_id=None: SimpleNamespace(trigger=object())))
    assert S.SchedulerUtil._get_trigger_type("1") == "manual"
