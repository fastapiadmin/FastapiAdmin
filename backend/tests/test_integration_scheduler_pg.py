"""真实 PostgreSQL 调度器节点自愈集成（不启动真实 APScheduler）。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.core.ap_scheduler import SchedulerUtil
from app.modules.task.cronjob.node.model import NodeModel

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            yield session
    finally:
        await engine.dispose()


def _code() -> str:
    return f"it_{uuid.uuid4().hex[:10]}"


async def _cleanup(codes: list[str]) -> None:
    async with _db() as db:
        for code in codes:
            await db.execute(text("DELETE FROM task_cornjob_node WHERE code=:c"), {"c": code})
        await db.commit()


async def test_reconcile_real_db_registers_and_removes(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    import app.core.database as dbmod
    import app.modules.task.cronjob.node.service as node_service

    codes = [_code(), _code(), _code()]
    past = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    async with _db() as db:
        enabled = NodeModel(name="it_enabled", code=codes[0], status=0, trigger="cron", trigger_args="* * * * *", func="builtin:x")
        disabled = NodeModel(name="it_disabled", code=codes[1], status=1, trigger="cron", trigger_args="* * * * *", func="builtin:x")
        past_date = NodeModel(name="it_past", code=codes[2], status=0, trigger="date", trigger_args=past, func="builtin:x")
        db.add_all([enabled, disabled, past_date]); await db.commit()
        ids = [enabled.id, disabled.id, past_date.id]
    try:
        @asynccontextmanager
        async def test_session():
            async with _db() as session:
                yield session
        monkeypatch.setattr(dbmod, "async_db_session", test_session)
        monkeypatch.setattr(SchedulerUtil, "get_jobs", classmethod(lambda cls: [type("J", (), {"id": "999999"})()]))
        removed: list[str] = []
        registered: list[int] = []
        monkeypatch.setattr(SchedulerUtil, "remove_job", classmethod(lambda cls, job_id: removed.append(str(job_id))))
        monkeypatch.setattr(node_service, "register_node_job", lambda node: registered.append(node.id))
        monkeypatch.setattr(SchedulerUtil, "describe_schedulability", classmethod(lambda cls, func: (True, None)))
        monkeypatch.setattr(SchedulerUtil, "log_unschedulable_jobs", classmethod(lambda cls, context=None: []))
        await SchedulerUtil.reconcile_node_jobs()
        assert ids[0] in registered
        assert ids[1] not in registered and ids[2] not in registered
        assert "999999" in removed
    finally:
        await _cleanup(codes)


async def test_reconcile_read_failure_is_safe(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.core.database as dbmod

    class Boom:
        async def __aenter__(self): raise RuntimeError("db down")
        async def __aexit__(self, *a): return False
    monkeypatch.setattr(dbmod, "async_db_session", lambda: Boom())
    await SchedulerUtil.reconcile_node_jobs()


async def test_reconcile_runs_without_error(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    import app.core.database as dbmod
    import app.modules.task.cronjob.node.service as node_service

    @asynccontextmanager
    async def test_session():
        async with _db() as session:
            yield session
    monkeypatch.setattr(dbmod, "async_db_session", test_session)
    monkeypatch.setattr(SchedulerUtil, "get_jobs", classmethod(lambda cls: []))
    registered: list[int] = []
    monkeypatch.setattr(node_service, "register_node_job", lambda node: registered.append(node.id))
    monkeypatch.setattr(SchedulerUtil, "describe_schedulability", classmethod(lambda cls, func: (True, None)))
    monkeypatch.setattr(SchedulerUtil, "log_unschedulable_jobs", classmethod(lambda cls, context=None: []))
    await SchedulerUtil.reconcile_node_jobs()
    assert all(isinstance(node_id, int) for node_id in registered)
