"""调度器可调度性/内置处理器纯逻辑。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.ap_scheduler import SchedulerUtil
from app.core.exceptions import CustomException


def test_describe_and_require_schedulable(monkeypatch: pytest.MonkeyPatch) -> None:
    assert SchedulerUtil.describe_schedulability(None)[0] is False
    monkeypatch.setattr("app.core.ap_scheduler.settings.SCHEDULER_ALLOW_CODE_EXEC", False)
    assert SchedulerUtil.describe_schedulability("print(1)")[0] is False
    with pytest.raises(CustomException):
        SchedulerUtil.require_schedulable("print(1)")
    monkeypatch.setattr("app.core.ap_scheduler.settings.SCHEDULER_ALLOW_CODE_EXEC", True)
    assert SchedulerUtil.describe_schedulability("print(1)")[0] is True
    assert SchedulerUtil.describe_schedulability("builtin:no_such_module")[0] is False


def test_builtin_registry() -> None:
    def handler(): return "ok"
    SchedulerUtil.register_builtin_handler("demo_fn", handler)
    assert SchedulerUtil.resolve_builtin_handler("builtin:demo_fn") is handler
    assert SchedulerUtil.resolve_builtin_handler("plain") is None
    with pytest.raises(ValueError):
        SchedulerUtil.resolve_builtin_handler("builtin:bad name!")
    with pytest.raises(ValueError):
        SchedulerUtil.resolve_builtin_handler("builtin:no_such_module")
    assert SchedulerUtil.resolve_builtin_handler("builtin:system_log.cleanup_expired_logs") is not None


def test_job_code_and_unschedulable(monkeypatch: pytest.MonkeyPatch) -> None:
    assert SchedulerUtil.job_code_block(None) is None
    assert SchedulerUtil.job_code_block(SimpleNamespace(args=[1])) is None
    assert SchedulerUtil.job_code_block(SimpleNamespace(args=[1, "x"])) == "x"
    jobs = [SimpleNamespace(id=1, name="a", args=[1, None]), SimpleNamespace(id=2, name="b", args=[1, "code"])]
    monkeypatch.setattr(SchedulerUtil, "get_jobs", classmethod(lambda cls: jobs))
    monkeypatch.setattr("app.core.ap_scheduler.settings.SCHEDULER_ALLOW_CODE_EXEC", False)
    found = SchedulerUtil.iter_unschedulable_jobs()
    assert len(found) == 2
    assert SchedulerUtil.log_unschedulable_jobs(context="test") == found


def test_job_id_helpers_and_trigger_types(monkeypatch: pytest.MonkeyPatch) -> None:
    from datetime import datetime, timedelta
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.date import DateTrigger
    from apscheduler.triggers.interval import IntervalTrigger
    assert SchedulerUtil._is_temp_job_id("a:manual:1") is True
    assert SchedulerUtil._is_temp_job_id("a_run_now_1") is True
    assert SchedulerUtil._is_temp_job_id("a") is False
    assert SchedulerUtil._normalize_job_id("a:manual:1") == "a"
    assert SchedulerUtil._normalize_job_id("a_run_now_1") == "a"
    assert SchedulerUtil._normalize_job_id("a") == "a"
    monkeypatch.setattr(SchedulerUtil, "get_job", classmethod(lambda cls, job_id: None))
    assert SchedulerUtil._get_trigger_type("x") == "manual"
    def with_trigger(trigger):
        return classmethod(lambda cls, job_id: SimpleNamespace(trigger=trigger))
    monkeypatch.setattr(SchedulerUtil, "get_job", with_trigger(CronTrigger(second="*")))
    assert SchedulerUtil._get_trigger_type("x") == "cron"
    monkeypatch.setattr(SchedulerUtil, "get_job", with_trigger(IntervalTrigger(seconds=1)))
    assert SchedulerUtil._get_trigger_type("x") == "interval"
    monkeypatch.setattr(SchedulerUtil, "get_job", with_trigger(DateTrigger(run_date=datetime.now() + timedelta(days=1))))
    assert SchedulerUtil._get_trigger_type("x") == "date"


def test_job_status(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(SchedulerUtil, "get_job", classmethod(lambda cls, job_id: None))
    assert SchedulerUtil.get_job_status(1) == 3
    monkeypatch.setattr(SchedulerUtil, "get_job", classmethod(lambda cls, job_id: SimpleNamespace(next_run_time=None)))
    assert SchedulerUtil.get_job_status(1) == 1
    monkeypatch.setattr(SchedulerUtil, "get_job", classmethod(lambda cls, job_id: SimpleNamespace(next_run_time="x")))
    import app.core.ap_scheduler as mod
    monkeypatch.setattr(mod.scheduler, "state", 0)
    assert SchedulerUtil.get_job_status(1) == 2
    monkeypatch.setattr(mod.scheduler, "state", 1)
    assert SchedulerUtil.get_job_status(1) == 0


def test_dispatch_event(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.core.ap_scheduler as mod
    calls = []
    monkeypatch.setattr(SchedulerUtil, "_finish_job_record", classmethod(lambda cls, **kw: calls.append(kw)))
    SchedulerUtil._dispatch_job_event(SimpleNamespace(job_id=None, code=1))
    SchedulerUtil._dispatch_job_event(SimpleNamespace(job_id="1", code=mod.EVENT_JOB_EXECUTED, retval="ok"))
    SchedulerUtil._dispatch_job_event(SimpleNamespace(job_id="1", code=mod.EVENT_JOB_ERROR, exception=ValueError("x")))
    SchedulerUtil._dispatch_job_event(SimpleNamespace(job_id="1", code=mod.EVENT_JOB_MISSED))
    assert len(calls) == 2


def test_task_wrapper_builtin_disabled_and_exec(monkeypatch: pytest.MonkeyPatch) -> None:
    def handler(x=1): return x + 1
    SchedulerUtil.register_builtin_handler("wrap_fn", handler)
    assert SchedulerUtil._task_wrapper(1, "builtin:wrap_fn", 2) == 3
    monkeypatch.setattr("app.core.ap_scheduler.settings.SCHEDULER_ALLOW_CODE_EXEC", False)
    with pytest.raises(RuntimeError):
        SchedulerUtil._task_wrapper(1, "print(1)")
    monkeypatch.setattr("app.core.ap_scheduler.settings.SCHEDULER_ALLOW_CODE_EXEC", True)
    assert SchedulerUtil._task_wrapper(1, "def handler(x=1):\n    return x * 2", 3) == 6
    with pytest.raises(ValueError):
        SchedulerUtil._task_wrapper(1, "x=1")
    assert SchedulerUtil._task_wrapper(1, "") is None


def test_get_job_state_serialization() -> None:
    class J:
        def __getstate__(self):
            return {"a": 1, "b": b"bytes", "c": [1, "x"], "d": {"n": None}, "e": object()}
    text = SchedulerUtil._get_job_state(J())
    assert '"a": 1' in text and '"c"' in text
    assert SchedulerUtil._get_job_state(None) is None


def test_trigger_date_manual(monkeypatch: pytest.MonkeyPatch) -> None:
    from datetime import datetime
    from apscheduler.triggers.date import DateTrigger
    monkeypatch.setattr(SchedulerUtil, "get_job", classmethod(lambda cls, job_id: SimpleNamespace(trigger=DateTrigger(run_date=datetime.now()))))
    assert SchedulerUtil._get_trigger_type("x") == "manual"


def test_finish_job_record_temp_and_date(monkeypatch: pytest.MonkeyPatch) -> None:
    from datetime import datetime, timedelta
    from apscheduler.triggers.date import DateTrigger
    records=[]; removed=[]
    monkeypatch.setattr(SchedulerUtil, "_record_job_log", staticmethod(lambda r: records.append(r)))
    monkeypatch.setattr(SchedulerUtil, "remove_job", classmethod(lambda cls, job_id: removed.append(job_id)))
    monkeypatch.setattr(SchedulerUtil, "get_job", classmethod(lambda cls, job_id: None))
    SchedulerUtil._finish_job_record(job_id="1:manual:2", status=2, detail="ok")
    assert records[0]["trigger_type"] == "manual" and removed == ["1:manual:2"]
    job = SimpleNamespace(name="n", next_run_time=None, trigger=DateTrigger(run_date=datetime.now()+timedelta(days=1)))
    monkeypatch.setattr(SchedulerUtil, "get_job", classmethod(lambda cls, job_id: job))
    SchedulerUtil._finish_job_record(job_id="2", status=2, detail="ok")
    assert "2" in removed


async def test_reconcile_node_jobs(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    from datetime import datetime, timedelta
    import app.core.database as dbmod
    import app.core.ap_scheduler as mod
    nodes = [
        SimpleNamespace(id=1, status=0, trigger="cron", trigger_args="* * * * *", func="builtin:x", name="a"),
        SimpleNamespace(id=2, status=1, trigger="cron", trigger_args="* * * * *", func="x", name="b"),
        SimpleNamespace(id=3, status=0, trigger="date", trigger_args=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), func="x", name="c"),
        SimpleNamespace(id=4, status=0, trigger="date", trigger_args=(datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), func="x", name="d"),
    ]
    class R:
        def scalars(self): return self
        def all(self): return nodes
    class S:
        async def execute(self, stmt): return R()
    class Ctx:
        async def __aenter__(self): return S()
        async def __aexit__(self,*a): return False
    monkeypatch.setattr(dbmod,"async_db_session",lambda: Ctx())
    monkeypatch.setattr(SchedulerUtil,"get_jobs",classmethod(lambda cls: [SimpleNamespace(id="1"),SimpleNamespace(id="2"),SimpleNamespace(id="tmp")]))
    removed=[]; registered=[]
    monkeypatch.setattr(SchedulerUtil,"remove_job",classmethod(lambda cls, jid: removed.append(jid)))
    import app.modules.task.cronjob.node.service as ns
    monkeypatch.setattr(ns,"register_node_job",lambda node: registered.append(node.id))
    monkeypatch.setattr("app.core.ap_scheduler.SchedulerUtil.describe_schedulability",classmethod(lambda cls, func: (True,None)))
    monkeypatch.setattr(SchedulerUtil,"log_unschedulable_jobs",classmethod(lambda cls, context=None: []))
    await SchedulerUtil.reconcile_node_jobs()
    assert "2" in removed and 1 in registered and 4 in registered


def test_scheduler_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    assert SchedulerUtil.job_code_block(None) is None
    assert SchedulerUtil.job_code_block(SimpleNamespace(args=["1"])) is None
    assert SchedulerUtil.job_code_block(SimpleNamespace(args=["1","builtin:x"])) == "builtin:x"
    monkeypatch.setattr(SchedulerUtil,"describe_schedulability",classmethod(lambda cls,c: (True,None)))
    SchedulerUtil.require_schedulable("x")
    monkeypatch.setattr(SchedulerUtil,"describe_schedulability",classmethod(lambda cls,c: (False,"bad")))
    with pytest.raises(CustomException, match="bad"):
        SchedulerUtil.require_schedulable("x")
    SchedulerUtil.register_builtin_handler("t", lambda: 1)
    assert SchedulerUtil.resolve_builtin_handler("builtin:t")() == 1
    assert SchedulerUtil.resolve_builtin_handler("exec") is None
    with pytest.raises(ValueError):
        SchedulerUtil.resolve_builtin_handler("builtin:bad/name")


def test_unschedulable_jobs(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    monkeypatch.setattr(SchedulerUtil,"get_jobs",classmethod(lambda cls: [SimpleNamespace(id=1,name="n",args=["1","x"])]))
    monkeypatch.setattr(SchedulerUtil,"job_code_block",classmethod(lambda cls,j: "x"))
    monkeypatch.setattr(SchedulerUtil,"describe_schedulability",classmethod(lambda cls,c: (False,"bad")))
    out=SchedulerUtil.iter_unschedulable_jobs()
    assert out==[("1","n","bad")]
    assert SchedulerUtil.log_unschedulable_jobs(context="test")==out
