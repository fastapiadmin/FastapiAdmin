"""RedisCURD 基础读写/锁/哈希/清空。"""

from __future__ import annotations

import pytest
from fakeredis.aioredis import FakeRedis

from app.core.redis_crud import RedisCURD


@pytest.fixture
async def redis():
    r = FakeRedis(decode_responses=True)
    yield r
    await r.aclose()


async def test_basic_get_set_delete(redis) -> None:
    c = RedisCURD(redis)
    assert await c.set("k", "v") is True
    assert await c.get("k") == "v"
    assert await c.exists("k")
    assert await c.ttl("k") == -1
    await c.set("e", "v", expire=10)
    assert await c.ttl("e") > 0
    assert await c.expire("e", 20) is True
    assert await c.mget(["k", "missing"]) == ["v", None]
    assert await c.get_keys("k") == ["k"]
    assert await c.scan_keys("k*")
    assert await c.delete("k", "e") is True
    assert not await c.exists("k")


async def test_clear_and_pattern_and_hash(redis) -> None:
    c = RedisCURD(redis)
    await c.set("p:a", "1"); await c.set("p:b", "2"); await c.set("x", "3")
    assert await c.clear("p:*")
    assert not await c.exists("p:a")
    await c.set("z:a", "1"); await c.set("z:b", "2")
    assert await c.delete_by_pattern("z:*") >= 0
    assert await c.hash_set("h", "f", "v") is True
    assert await c.hash_get("h", ["f", "no"]) == ["v", None]
    assert await c.db_size() >= 0
    assert isinstance(await c.info(), dict)
    assert isinstance(await c.commandstats(), dict)


async def test_error_fallbacks() -> None:
    class Bad:
        def __getattr__(self, name):
            async def fail(*a, **k): raise RuntimeError()
            return fail
    c = RedisCURD(Bad())
    assert await c.get("x") is None
    assert await c.set("x", "v") is False
    assert await c.mget(["x"]) == []
    assert await c.get_keys() == []
    assert await c.scan_keys() == []
    assert await c.delete("x") is False
    assert await c.clear() is False
    assert await c.exists("x") is False
    assert await c.ttl("x") == -1
    assert await c.expire("x", 1) is False
    assert await c.delete_by_pattern("*") == 0
    assert await c.info() == {}
    assert await c.db_size() == 0
    assert await c.commandstats() == {}
    assert await c.hash_set("h", "k", "v") is False
    assert await c.hash_get("h", ["k"]) == []
