"""健康检查服务 DB/Redis 探活。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.modules.monitor.health.service import HealthService


class Ctx:
    def __init__(self, fail=False): self.fail = fail
    async def __aenter__(self):
        if self.fail: raise RuntimeError()
        return SimpleNamespace(execute=self.execute)
    async def execute(self, stmt): return 1
    async def __aexit__(self, *a): return False


async def test_check_database(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.monitor.health.service as mod
    monkeypatch.setattr(mod, "async_db_session", lambda: Ctx())
    assert await HealthService.check_database() == 1
    monkeypatch.setattr(mod, "async_db_session", lambda: Ctx(fail=True))
    assert await HealthService.check_database() == 0


async def test_check_redis() -> None:
    assert await HealthService.check_redis(None) == 0
    class R:
        async def ping(self): return True
    assert await HealthService.check_redis(R()) == 1
    class Bad:
        async def ping(self): raise RuntimeError()
    assert await HealthService.check_redis(Bad()) == 0


async def test_collect(monkeypatch: pytest.MonkeyPatch) -> None:
    async def db(): return 1
    async def redis(r): return 0
    monkeypatch.setattr(HealthService, "check_database", db)
    monkeypatch.setattr(HealthService, "check_redis", redis)
    out = await HealthService.collect(None)
    assert out.db_status == 1 and out.redis_status == 0
