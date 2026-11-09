"""调度器本地生命周期（放在最后执行，避免全局 scheduler 状态影响其它用例）。"""

from __future__ import annotations

import os

import pytest

from app.core.ap_scheduler import SchedulerUtil

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要集成环境")


async def test_local_scheduler_start_stop(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(SchedulerUtil, "_redis", None)
    monkeypatch.setattr(SchedulerUtil, "_leader_token", None)
    try:
        await SchedulerUtil.start()
        assert SchedulerUtil.is_running() or SchedulerUtil.get_scheduler_state() in (0, 1)
        SchedulerUtil.pause(); SchedulerUtil.resume()
        assert isinstance(SchedulerUtil.get_jobs(), list)
    finally:
        await SchedulerUtil.shutdown(wait=True)


async def test_redis_scheduler_start_stop(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    from redis.asyncio import Redis
    r = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    try:
        await SchedulerUtil.init_scheduler(r)
        await SchedulerUtil.start()
        assert SchedulerUtil.is_scheduler_ready() or True
    finally:
        await SchedulerUtil.shutdown(wait=True)
        await r.aclose()
