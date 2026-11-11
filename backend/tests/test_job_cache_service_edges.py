"""调度日志服务/缓存浏览边缘。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import CustomException
from app.modules.task.cronjob.job.service import JobService
import app.modules.monitor.cache.browser as B


def test_job_service_edges(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, *a): pass
        async def get_obj_by_id_crud(self, **k): return None
        async def get_obj_list_crud(self, **k): return []
        async def clear_obj_crud(self): pass
    monkeypatch.setattr("app.modules.task.cronjob.job.service.JobCRUD", C)
    svc = JobService(SimpleNamespace(user=SimpleNamespace(id=1)), None)
    import asyncio
    with pytest.raises(CustomException):
        asyncio.run(svc.get_job_log_detail(1))
    assert asyncio.run(svc.get_job_log_list()) == []
    asyncio.run(svc.clear_job_log())
    with pytest.raises(CustomException):
        asyncio.run(svc.delete_job_log([]))


async def test_cache_browser_edges() -> None:
    assert B._text(b"abc")[0] == "abc"
    with pytest.raises(CustomException):
        await B.RedisBrowserService.get_value(None, db=0, key="")
    class R:
        connection_pool = SimpleNamespace(connection_kwargs={"db": 0})
        async def aclose(self): pass
        async def type(self, k): return "set"
        async def sscan(self, k, count=200): return (0, [b"a", b"b"])
        async def get(self, k): return b"x"
        async def ttl(self, k): return -1
        async def memory_usage(self, k): return 1
    out = await B.RedisBrowserService.get_value(R(), db=0, key="k")
    assert out is not None
