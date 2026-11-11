"""配置 URI / 调度器锁/序列化边缘。"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from app.config.setting import settings
import app.core.ap_scheduler as S


def test_setting_uri_edges(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.config.setting.logger", None, raising=False)
    monkeypatch.setattr(settings.__class__, "_warn", classmethod(lambda cls, m: None), raising=False)
    old = settings.DATABASE_TYPE
    try:
        object.__setattr__(settings, "DATABASE_TYPE", "sqlite")
        object.__setattr__(settings, "DATABASE_NAME", "x")
        assert settings.DB_URI.startswith("sqlite:///") and settings.ASYNC_DB_URI.startswith("sqlite+aiosqlite:///")
        object.__setattr__(settings, "DATABASE_NAME", "x.db")
        assert settings.DB_URI.endswith("x.db")
        object.__setattr__(settings, "DATABASE_TYPE", "oracle")
        with pytest.raises(ValueError):
            _ = settings.DB_URI
        with pytest.raises(ValueError):
            _ = settings.ASYNC_DB_URI
    finally:
        object.__setattr__(settings, "DATABASE_TYPE", old)


async def test_scheduler_lock_continue(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []
    class C:
        def __init__(self, r): pass
        async def renew_lock(self, **k): return False
        async def get(self, **k): return "t"
    monkeypatch.setattr("app.core.redis_crud.RedisCURD", C)
    monkeypatch.setattr(S.SchedulerUtil, "_redis", object())
    monkeypatch.setattr(S.SchedulerUtil, "_leader_token", "t")
    async def sleep(_):
        calls.append(1)
        if len(calls) > 1: raise asyncio.CancelledError
    monkeypatch.setattr(asyncio, "sleep", sleep)
    with pytest.raises(asyncio.CancelledError):
        await S.SchedulerUtil._maintain_loop()


async def test_scheduler_reconcile_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    class Ctx:
        async def __aenter__(self): raise RuntimeError("x")
        async def __aexit__(self, *a): return False
    import app.core.database as db
    monkeypatch.setattr(db, "async_db_session", lambda: Ctx())
    await S.SchedulerUtil.reconcile_node_jobs()


def test_serialize_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    class Bad:
        def __str__(self): raise RuntimeError("x")
    class Job:
        def __getstate__(self): return {"x": Bad()}
    assert S.SchedulerUtil._get_job_state(Job()) is not None
