"""真实 Redis 集成测试：RedisCURD 常用语义（范围 A，不使用 mock）。"""

from __future__ import annotations

import os
import uuid

import pytest
from redis.asyncio import Redis

from app.core.redis_crud import RedisCURD

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 Redis：设置 RUN_INTEGRATION=1",
)


@pytest.fixture
async def redis():
    client = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()


def _key() -> str:
    return f"it:crud:{uuid.uuid4().hex}"


async def test_set_get_delete(redis) -> None:
    c = RedisCURD(redis); k = _key()
    assert await c.set(k, '{"a":1}') is True
    assert await c.get(k) == '{"a":1}'
    assert await c.exists(k)
    assert await c.delete(k)
    assert await c.get(k) is None


async def test_expire_and_ttl(redis) -> None:
    c = RedisCURD(redis); k = _key()
    await c.set(k, "x", expire=30)
    assert 0 < await c.ttl(k) <= 30
    assert await c.expire(k, 60) is True
    assert await c.ttl(k) > 30


async def test_lock_and_unlock(redis) -> None:
    c = RedisCURD(redis); k = _key()
    ok, token = await c.lock(k, 10)
    assert ok is True
    ok2, _token2 = await c.lock(k, 10)
    assert ok2 is False
    assert await c.unlock(k, token) is True
    assert await c.delete(k)


async def test_compare_and_set(redis) -> None:
    c = RedisCURD(redis); k = _key()
    await c.set(k, "1")
    assert await c.compare_and_set(k, "1", "2", 30) is True
    assert await c.compare_and_set(k, "1", "3", 30) is False
    assert await c.get(k) == "2"
    await c.delete(k)


async def test_scan_and_mget(redis) -> None:
    c = RedisCURD(redis); prefix = _key()
    await c.set(prefix + ":a", "1"); await c.set(prefix + ":b", "2")
    keys = await c.scan_keys(prefix + "*")
    assert len(keys) == 2
    assert sorted(await c.mget(sorted(keys))) == ["1", "2"]
    await c.delete_by_pattern(prefix + "*")


async def test_hash(redis) -> None:
    c = RedisCURD(redis); k = _key()
    assert await c.hash_set(k, "a", "1") is True
    assert await c.hash_get(k, ["a"]) == ["1"]
    assert await c.delete(k)
