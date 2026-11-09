"""调度器事件、任务状态与执行日志。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from apscheduler.events import EVENT_ALL_JOBS_REMOVED, EVENT_JOB_ADDED, EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_JOB_MISSED, EVENT_JOB_REMOVED, EVENT_JOB_SUBMITTED, JobEvent
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

import app.core.ap_scheduler as S


def test_humanize_and_trigger_and_state(monkeypatch: pytest.MonkeyPatch) -> None:
    assert "超时" in S._humanize_job_error("Timeout")
    assert S._humanize_job_error("other") == "other"
    class F:
        def __init__(self, trig): self.trigger = trig
    monkeypatch.setattr(S.SchedulerUtil, "get_job", classmethod(lambda cls, job_id: F(CronTrigger())))
    assert S.SchedulerUtil._get_trigger_type("1") == "cron"
    monkeypatch.setattr(S.SchedulerUtil, "get_job", classmethod(lambda cls, job_id: F(IntervalTrigger(seconds=1))))
    assert S.SchedulerUtil._get_trigger_type("1") == "interval"
    monkeypatch.setattr(S.SchedulerUtil, "get_job", classmethod(lambda cls, job_id: F(DateTrigger(run_date="2030-01-01"))))
    assert S.SchedulerUtil._get_trigger_type("1") == "date"
    class J:
        def __getstate__(self):
            return {"b": b"x", "d": {"a": 1}, "l": [1, object()], "o": SimpleNamespace(x=1, _y=2)}
    state = S.SchedulerUtil._get_job_state(J())
    assert state and "b" in state


def test_finish_job_temp_and_date(monkeypatch: pytest.MonkeyPatch) -> None:
    rec=[]
    monkeypatch.setattr(S.SchedulerUtil, "_record_job_log", staticmethod(lambda r: rec.append(r)))
    monkeypatch.setattr(S.SchedulerUtil, "_is_temp_job_id", staticmethod(lambda jid: True))
    removed=[]
    monkeypatch.setattr(S.SchedulerUtil, "get_job", classmethod(lambda cls, job_id=None: None))
    monkeypatch.setattr(S.SchedulerUtil, "remove_job", classmethod(lambda cls, job_id: removed.append(job_id)))
    S.SchedulerUtil._finish_job_record(job_id="1:manual:x", status=1, detail="x")
    assert rec and removed == ["1:manual:x"]
    rec.clear(); removed.clear()
    monkeypatch.setattr(S.SchedulerUtil, "_is_temp_job_id", staticmethod(lambda jid: False))
    job = SimpleNamespace(name="n", trigger=DateTrigger(run_date="2030-01-01"), next_run_time=None)
    monkeypatch.setattr(S.SchedulerUtil, "get_job", classmethod(lambda cls, job_id=None: job))
    S.SchedulerUtil._finish_job_record(job_id="2", status=0, detail=None)
    assert rec and "2" in removed


def test_dispatch_events(monkeypatch: pytest.MonkeyPatch) -> None:
    done=[]
    monkeypatch.setattr(S.SchedulerUtil, "_finish_job_record", classmethod(lambda cls, **kw: done.append(kw)))
    for code in (EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_SUBMITTED, EVENT_JOB_REMOVED, EVENT_JOB_ADDED, EVENT_ALL_JOBS_REMOVED):
        S.SchedulerUtil._dispatch_job_event(SimpleNamespace(code=code, job_id="1", retval="x", exception=RuntimeError("e")))
    assert done


def test_record_job_log(monkeypatch: pytest.MonkeyPatch) -> None:
    added=[]; committed=[]
    class Ses:
        def __init__(self, *a): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def add(self, obj): added.append(obj)
        def commit(self): committed.append(1)
    monkeypatch.setattr(S, "Session", Ses)
    S.SchedulerUtil._record_job_log({"job_id": "1"})
    assert added and committed
