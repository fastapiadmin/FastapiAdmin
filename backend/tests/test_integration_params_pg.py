"""真实 PostgreSQL + Redis 系统参数集成。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.modules.system.params.model import ParamsModel
from app.modules.system.params.schema import ParamsUpdateSchema
from app.modules.system.params.service import ParamsService

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL/Redis：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            yield session
    finally:
        await engine.dispose()


def _key() -> str:
    return f"it_param_{uuid.uuid4().hex[:10]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


async def _cleanup(key: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_param WHERE config_key=:k"), {"k": key})
        await db.commit()


async def _create(key: str) -> int:
    async with _db() as db:
        obj = ParamsModel(config_name="IT", config_key=key, config_value="1", config_type=False, status=0)
        db.add(obj); await db.commit(); await db.refresh(obj)
        return obj.id


async def test_update_and_cache(test_client) -> None:
    key = _key(); uid = await _create(key); r = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    try:
        async with _db() as db:
            out = await ParamsService(_auth(), db).update(r, uid, ParamsUpdateSchema(config_name="IT2", config_key=key, config_value="2"))
            await db.commit()
            assert out.config_value == "2"
        assert await r.exists(f"system_config:{key}") == 1
    finally:
        await r.delete(f"system_config:{key}"); await r.aclose(); await _cleanup(key)


async def test_update_missing(test_client) -> None:
    r = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    try:
        async with _db() as db:
            with pytest.raises(CustomException, match="不存在"):
                await ParamsService(_auth(), db).update(r, 99999999, ParamsUpdateSchema(config_name="IT", config_key=_key(), config_value="1"))
    finally:
        await r.aclose()


async def test_update_key_change_rejected(test_client) -> None:
    key = _key(); uid = await _create(key); r = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    try:
        async with _db() as db:
            with pytest.raises(CustomException, match="不允许修改"):
                await ParamsService(_auth(), db).update(r, uid, ParamsUpdateSchema(config_name="IT", config_key=key + "_x", config_value="2"))
    finally:
        await r.aclose(); await _cleanup(key)


async def test_init_cache_empty(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    async def none(): return []
    monkeypatch.setattr(ParamsService, "_load_all_configs_from_db", staticmethod(none))
    r = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    try:
        keys = await r.keys("system_config:*")
        if keys:
            await r.delete(*keys)
        with pytest.raises(CustomException, match="不存在"):
            await ParamsService.init_cache(r)
        assert await ParamsService.get_init_cache(r) == []
    finally:
        await r.aclose()


async def test_sync_configs_redis_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    class Bad:
        def __init__(self,*a): pass
        async def set(self,**kw): raise RuntimeError("redis down")
    monkeypatch.setattr("app.modules.system.params.service.RedisCURD", Bad)
    cfg = SimpleNamespace(config_name="IT", config_key="k", config_value="1", status=0, config_type=False, id=1)
    assert await ParamsService._sync_configs_to_redis(object(), [cfg]) == []


async def test_get_init_cache_with_config(test_client) -> None:
    import json
    key = _key(); r = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    try:
        await r.set(f"system_config:{key}", json.dumps({"config_name": "IT", "config_key": key, "config_value": "1", "config_type": False, "status": 0}))
        rows = await ParamsService.get_init_cache(r)
        assert any(x["config_key"] == key for x in rows)
    finally:
        await r.delete(f"system_config:{key}"); await r.aclose()
