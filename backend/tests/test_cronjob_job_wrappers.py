"""调度任务运维包装（fake SchedulerUtil）。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.modules.task.cronjob.job.service as M
from app.core.ap_scheduler import SchedulerUtil
from app.core.exceptions import CustomException


def _patch(monkeypatch, **kw):
    for k, v in kw.items(): monkeypatch.setattr(SchedulerUtil, k, staticmethod(v))


def test_status_and_jobs(monkeypatch: pytest.MonkeyPatch) -> None:
    job = SimpleNamespace(id="1", name="n", trigger="cron", next_run_time=None)
    _patch(monkeypatch, get_scheduler_state=lambda: 1, is_running=lambda: True,
           get_jobs=lambda: [job], log_unschedulable_jobs=lambda **k: [],
           job_code_block=lambda j: "builtin:x", describe_schedulability=lambda c: (True, None),
           get_job_status=lambda job_id: 0)
    st = M.JobService.get_scheduler_status()
    assert st.job_count == 1 and st.is_running is True
    jobs = M.JobService.get_scheduler_jobs()
    assert jobs[0].id == "1" and jobs[0].schedulable is True


def test_ensure_job_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch(monkeypatch, get_job=lambda **k: None)
    with pytest.raises(CustomException):
        M.JobService._ensure_job_exists("1")


async def test_scheduler_controls(monkeypatch: pytest.MonkeyPatch) -> None:
    calls=[]
    async def start(): calls.append("start")
    async def shutdown(): calls.append("shutdown")
    _patch(monkeypatch, start=lambda: start(), shutdown=lambda: shutdown(), pause=lambda: calls.append("pause"),
           resume=lambda: calls.append("resume"), clear_jobs=lambda: calls.append("clear"), print_jobs=lambda: "x")
    await M.JobService.start_scheduler(); await M.JobService.shutdown_scheduler()
    M.JobService.pause_scheduler(); M.JobService.resume_scheduler(); M.JobService.clear_scheduler_jobs()
    assert calls == ["start", "shutdown", "pause", "resume", "clear"]
    assert M.JobService.get_scheduler_console() == "x"


def test_job_controls(monkeypatch: pytest.MonkeyPatch) -> None:
    calls=[]
    _patch(monkeypatch, get_job=lambda **k: True, pause_job=lambda **k: calls.append("pause"),
           resume_job=lambda **k: calls.append("resume"), run_job_now=lambda **k: calls.append("run"),
           modify_job=lambda **k: calls.append("modify"), remove_job=lambda **k: calls.append("remove"))
    M.JobService.pause_job("1"); M.JobService.resume_job("1"); M.JobService.run_job_now("1")
    data = SimpleNamespace(to_changes=lambda: {"name": "x"})
    M.JobService.modify_job("1", data)
    M.JobService.remove_job("1")
    assert calls == ["pause", "resume", "run", "modify", "remove"]
    with pytest.raises(CustomException):
        M.JobService.modify_job("1", SimpleNamespace(to_changes=lambda: {}))
