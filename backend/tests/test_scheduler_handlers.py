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
