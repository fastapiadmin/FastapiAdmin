"""调度器维护协程：续期、候选轮询、接管。"""

from __future__ import annotations

import asyncio

import pytest

import app.core.ap_scheduler as S
import app.core.redis_crud as R


async def test_maintain_leader_renew(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"sleep": 0}
    class C:
        def __init__(self, redis): pass
        async def renew_lock(self, **kw): return True
        async def get(self, **kw): return "t"
        async def lock(self, **kw): return (False, "")
    monkeypatch.setattr(R, "RedisCURD", C)
    monkeypatch.setattr(S.SchedulerUtil, "_redis", object())
    monkeypatch.setattr(S.SchedulerUtil, "_leader_token", "t")
    async def sleep(_):
        calls["sleep"] += 1
        if calls["sleep"] > 1: raise asyncio.CancelledError
    monkeypatch.setattr(asyncio, "sleep", sleep)
    with pytest.raises(asyncio.CancelledError):
        await S.SchedulerUtil._maintain_loop()
    assert calls["sleep"] >= 2


async def test_maintain_candidate_takeover(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"n": 0}; started = []; spawned = []
    class C:
        def __init__(self, redis): pass
        async def lock(self, **kw):
            calls["n"] += 1
            return (True, "tok") if calls["n"] == 2 else (False, "")
    monkeypatch.setattr(R, "RedisCURD", C)
    monkeypatch.setattr(S.SchedulerUtil, "_redis", object())
    monkeypatch.setattr(S.SchedulerUtil, "_leader_token", None)
    monkeypatch.setattr(S.SchedulerUtil, "_start_scheduler_local", classmethod(lambda cls: started.append(1)))
    monkeypatch.setattr(S.SchedulerUtil, "_spawn_reconcile", classmethod(lambda cls: spawned.append(1)))
    async def sleep(_):
        if calls["n"] >= 2: raise asyncio.CancelledError
    monkeypatch.setattr(asyncio, "sleep", sleep)
    with pytest.raises(asyncio.CancelledError):
        await S.SchedulerUtil._maintain_loop()
    assert started and spawned and S.SchedulerUtil._leader_token == "tok"
