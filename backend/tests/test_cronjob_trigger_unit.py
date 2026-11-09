"""调度节点 trigger 解析与添加任务。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from apscheduler.jobstores.base import ConflictingIdError

import app.modules.task.cronjob.node.service as M


def test_build_triggers() -> None:
    assert M._build_job_trigger("cron", "0 * * * * ? *", None, None)
    assert M._build_job_trigger("cron", "0 0 1 * * *", None, None)
    with pytest.raises(ValueError):
        M._build_job_trigger("cron", "* * * * * ? *", None, None)
    with pytest.raises(ValueError):
        M._build_job_trigger("cron", "bad", None, None)
    with pytest.raises(ValueError):
        M._build_job_trigger("cron", "0 0 0 0 0 0 0", None, None)
    assert M._build_job_trigger("interval", "* 1 2 3 0", None, None)
    with pytest.raises(ValueError):
        M._build_job_trigger("interval", "1 2", None, None)
    assert M._build_job_trigger("date", "2030-01-01 00:00:00", None, None)
    with pytest.raises(ValueError):
        M._build_job_trigger("date", "", None, None)
    with pytest.raises(ValueError):
        M._build_job_trigger("date", "bad", None, None)
    with pytest.raises(ValueError):
        M._build_job_trigger("unknown", "x", None, None)


class Sched:
    def __init__(self, conflict=False):
        self.calls=[]; self.conflict=conflict; self.removed=[]
    def add_job(self, **kw):
        self.calls.append(kw)
        if self.conflict and len(self.calls) == 1: raise ConflictingIdError(kw["id"])
        return SimpleNamespace(id=kw["id"])
    def remove_job(self, **kw): self.removed.append(kw)


def _node(**kw):
    base = dict(id=1, name="n", func="builtin:it_ok", jobstore="default", executor="threadpool", args="a,b", kwargs='{"x":1}', coalesce=False, max_instances=1)
    base.update(kw); return SimpleNamespace(**base)


def test_add_job(monkeypatch: pytest.MonkeyPatch) -> None:
    s=Sched(); monkeypatch.setattr(M, "scheduler", s)
    M.SchedulerUtil.register_builtin_handler("it_ok", lambda: None)
    job=M._add_job_with_trigger(_node(), object())
    assert job.id == "1" and s.calls[0]["args"] == ["1", "builtin:it_ok", "a", "b"]
    with pytest.raises(ValueError):
        M._add_job_with_trigger(_node(func=""), object())
    with pytest.raises(ValueError):
        M._add_job_with_trigger(_node(kwargs="bad"), object())
    s2=Sched(conflict=True); monkeypatch.setattr(M, "scheduler", s2)
    assert M._add_job_with_trigger(_node(), object()).id == "1"
    assert s2.removed
