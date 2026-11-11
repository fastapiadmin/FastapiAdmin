"""传输任务执行主体分支（取消/删除/无步骤/源配置缺失）。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import app.modules.task.storage.transfer.engine as E


def _task(**kw):
    base = dict(id=1, status="pending", source_type="local", source_id=None, source_path="", source_size=None, total_size=0, transferred_size=0, progress=0, speed=0.0, error_msg=None, finished_at=None, is_deleted=False, created_id=1)
    base.update(kw); return SimpleNamespace(**base)


def _step(**kw):
    base = dict(step_order=0, status="pending", total_size=0, transferred_size=0, speed=0.0, progress=0, error_msg=None, started_at=None, finished_at=None)
    base.update(kw); return SimpleNamespace(**base)


class Ctx:
    def __init__(self, db): self.db = db
    async def __aenter__(self): return self.db
    async def __aexit__(self, *a): return False


class DB:
    def __init__(self, task, steps): self.task = task; self.steps = steps; self.commits = 0
    async def get(self, *a): return self.task
    async def refresh(self, *a): pass
    async def commit(self): self.commits += 1


async def _run(monkeypatch, db, steps, kind="normal"):
    monkeypatch.setattr(E, "async_db_session", lambda: Ctx(db))
    monkeypatch.setattr(E, "_load_steps", AsyncMock(return_value=steps))
    monkeypatch.setattr(E, "_broadcast", AsyncMock())
    monkeypatch.setattr(E, "_run_step", AsyncMock(return_value=True))
    await E._execute_transfer_task(1)


async def test_task_missing_or_done(monkeypatch: pytest.MonkeyPatch) -> None:
    await _run(monkeypatch, DB(None, []), [])
    t = _task(status="success")
    await _run(monkeypatch, DB(t, []), [])


async def test_no_steps(monkeypatch: pytest.MonkeyPatch) -> None:
    t = _task(); db = DB(t, [])
    await _run(monkeypatch, db, [])
    assert t.status == "failed" and "步骤" in t.error_msg


async def test_remote_source_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    t = _task(source_type="remote", source_id=9, source_path="a")
    monkeypatch.setattr(E, "_build_config", AsyncMock(return_value=None))
    await _run(monkeypatch, DB(t, []), [_step()])
    assert t.status == "failed" and "源存储源" in t.error_msg


async def test_deleted_and_canceled(monkeypatch: pytest.MonkeyPatch) -> None:
    t = _task(is_deleted=True)
    steps = [_step()]
    await _run(monkeypatch, DB(t, []), steps)
    t2 = _task()
    steps2 = [_step()]
    E.transfer_task_registry.mark_cancel(1)
    await _run(monkeypatch, DB(t2, []), steps2)
    assert t2.status == "canceled"


async def test_execute_outer_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    class BadDB:
        async def get(self, *a): raise RuntimeError("x")
    monkeypatch.setattr(E, "async_db_session", lambda: Ctx(BadDB()))
    monkeypatch.setattr(E, "_execute_transfer_task", AsyncMock(side_effect=RuntimeError("boom")))
    await E.execute_transfer_task(1)
