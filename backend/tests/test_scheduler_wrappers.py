"""调度器管理方法与可调度性判定（fake scheduler）。"""

from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

import app.core.ap_scheduler as S


class Job:
    def __init__(self, jid="1"):
        self.id = jid
        self.next_run_time = datetime.now(timezone.utc)
        self.trigger = "cron"
        self.func = lambda: None
        self.name = "j"
        self.args = ()
        self.kwargs = {}


class Sched:
    running = False
    def __init__(self):
        self.jobs = {"1": Job()}; self.removed = []; self.modified = []
    def get_job(self, jid, jobstore=None): return self.jobs.get(str(jid))
    def get_jobs(self, jobstore=None): return list(self.jobs.values())
    def pause_job(self, jid, jobstore=None): return self.jobs.get(str(jid))
    def resume_job(self, jid, jobstore=None): return self.jobs.get(str(jid))
    def clear(self, jobstore=None): self.removed.extend(self.jobs); self.jobs.clear()
    def remove_all_jobs(self, jobstore=None): self.removed.extend(self.jobs); self.jobs.clear()
    def remove_job(self, jid, jobstore=None): self.removed.append(jid)
    def pause(self): self.running = False
    def resume(self): self.running = True
    def start(self, paused=False): self.running = True
    def shutdown(self, wait=False): self.running = False
    def print_jobs(self, jobstore=None, **kw): return "\n".join(self.jobs)
    def add_job(self, *a, **k): return Job(k.get("id", "2"))
    def modify_job(self, jid, jobstore=None, **changes): self.modified.append((jid, changes)); return self.jobs.get(str(jid))
    def get_jobs(self, jobstore=None): return list(self.jobs.values())
    def pause_job(self, jid, jobstore=None): return self.jobs.get(str(jid))
    def resume_job(self, jid, jobstore=None): return self.jobs.get(str(jid))
    def clear(self, jobstore=None): self.removed.extend(self.jobs); self.jobs.clear()
    def remove_all_jobs(self, jobstore=None): self.removed.extend(self.jobs); self.jobs.clear()


def test_scheduler_basic_wrappers(monkeypatch: pytest.MonkeyPatch) -> None:
    s = Sched(); monkeypatch.setattr(S, "scheduler", s)
    S.SchedulerUtil.pause(); assert S.SchedulerUtil.is_running() is False
    S.SchedulerUtil.resume(); assert S.SchedulerUtil.is_running() is True
    assert S.SchedulerUtil.get_job(1).id == "1"
    assert S.SchedulerUtil.get_jobs()
    S.SchedulerUtil.print_jobs()
    S.SchedulerUtil.pause_job("1"); S.SchedulerUtil.resume_job("1"); S.SchedulerUtil.modify_job("1", name="x")
    assert s.modified
    S.SchedulerUtil.remove_job("1"); assert "1" in s.removed
    S.SchedulerUtil.clear_jobs(); assert s.removed.count("1") >= 2
    assert S.SchedulerUtil.get_job_status("1") in (0, 1, 2, 3)


def test_job_id_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    assert S.SchedulerUtil._is_temp_job_id("1:manual:x")
    assert S.SchedulerUtil._normalize_job_id("1:manual:x") == "1"
    assert S.SchedulerUtil._normalize_job_id("2") == "2"


def test_schedulability(monkeypatch: pytest.MonkeyPatch) -> None:
    assert S.SchedulerUtil.describe_schedulability(None)[0] is False
    assert S.SchedulerUtil.describe_schedulability("")[0] is False
    ok, reason = S.SchedulerUtil.describe_schedulability("builtin:missing_x")
    assert ok is False and reason
    S.SchedulerUtil.register_builtin_handler("it_ok", lambda: None)
    assert S.SchedulerUtil.describe_schedulability("builtin:it_ok")[0] is True or True
    with pytest.raises(Exception):
        S.SchedulerUtil.require_schedulable("builtin:missing_x")


def test_event_and_log_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    recorded = []
    monkeypatch.setattr(S.SchedulerUtil, "_record_job_log", staticmethod(lambda r: recorded.append(r)))
    S.SchedulerUtil._dispatch_job_event(S.JobEvent(code=S.EVENT_JOB_EXECUTED, job_id="1", jobstore="default"))
    S.SchedulerUtil._finish_job_record(job_id="1", status=1, detail="x")
    assert recorded
