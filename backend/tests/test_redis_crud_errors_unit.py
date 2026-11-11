"""Redis 连接与锁/发布的异常降级。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from redis import exceptions

import app.core.redis_crud as M
from app.core.redis_crud import RedisCURD, redis_connect


class Bad:
    async def eval(self, *a, **k): raise RuntimeError("x")
    async def delete(self, *a, **k): raise RuntimeError("x")
    async def publish(self, *a, **k): raise RuntimeError("x")


async def test_redis_connect_success_and_close(monkeypatch: pytest.MonkeyPatch) -> None:
    class R:
        def __init__(self): self.closed=False
        async def ping(self): return True
        async def close(self): self.closed=True
    r=R()
    async def from_url(**kw): return r
    monkeypatch.setattr(M.Redis, "from_url", from_url)
    app=SimpleNamespace(state=SimpleNamespace(redis=None))
    assert await redis_connect(app, True) is r
    await redis_connect(app, False)
    assert r.closed


async def test_redis_connect_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    async def bad(**kw): raise exceptions.ConnectionError("no")
    monkeypatch.setattr(M.Redis, "from_url", bad)
    app=SimpleNamespace(state=SimpleNamespace(redis=None))
    with pytest.raises(exceptions.ConnectionError):
        await redis_connect(app, True)


async def test_lock_error_paths() -> None:
    c=RedisCURD(Bad())
    assert await c.compare_and_set("k","a","b",1) is False
    assert await c.lock("k",1) == (False, "")
    assert await c.unlock("k","v") is False
    assert await c.unlock_simple("k") is False
    assert await c.renew_lock("k",1,"v") is False
    assert await c.publish("ch","m") == 0
