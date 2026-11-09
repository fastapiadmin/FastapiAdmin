"""真实 Redis AI 模型配置集成。"""

from __future__ import annotations

import os
import uuid

import pytest
from redis.asyncio import Redis

from app.modules.ai.chat.service import (
    _ai_model_active_key,
    _ai_model_items_key,
    create_user_model_config,
    delete_user_model_config,
    get_active_model_id,
    get_user_model_config,
    list_user_model_configs,
    set_active_model_config,
    update_user_model_config,
)
from app.modules.ai.chat.schema import AiModelConfigSchema

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 Redis：设置 RUN_INTEGRATION=1",
)


@pytest.fixture
async def redis():
    client = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    yield client
    await client.aclose()


def _uid() -> int:
    return 900000000 + uuid.uuid4().int % 1000000


def _cfg(name: str = "it") -> AiModelConfigSchema:
    return AiModelConfigSchema(name=name, model_id="m", base_url="https://api.example.com/v1", api_key="secret")


async def _cleanup(redis: Redis, uid: int) -> None:
    await redis.delete(_ai_model_items_key(uid), _ai_model_active_key(uid))


async def test_create_and_delete(redis: Redis) -> None:
    uid = _uid()
    try:
        item = await create_user_model_config(redis, uid, _cfg())
        assert await get_active_model_id(redis, uid) == item["id"]
        assert len(await list_user_model_configs(redis, uid)) == 1
        assert (await get_user_model_config(redis, uid))["id"] == item["id"]
        assert await delete_user_model_config(redis, uid, item["id"]) is True
        assert await get_user_model_config(redis, uid) is None
    finally:
        await _cleanup(redis, uid)


async def test_switch_active(redis: Redis) -> None:
    uid = _uid()
    try:
        a = await create_user_model_config(redis, uid, _cfg("a"))
        b = await create_user_model_config(redis, uid, _cfg("b"))
        assert await set_active_model_config(redis, uid, b["id"]) is True
        assert await get_active_model_id(redis, uid) == b["id"]
        assert await set_active_model_config(redis, uid, "__default__") is True
        assert await get_active_model_id(redis, uid) is None
        assert await set_active_model_config(redis, uid, a["id"]) is True
    finally:
        await _cleanup(redis, uid)


async def test_update_config(redis: Redis) -> None:
    uid = _uid()
    try:
        item = await create_user_model_config(redis, uid, _cfg())
        updated = await update_user_model_config(redis, uid, item["id"], _cfg("new"))
        assert updated is not None and updated["name"] == "new"
        assert await update_user_model_config(redis, uid, "missing", _cfg()) is None
    finally:
        await _cleanup(redis, uid)


async def test_switch_missing(redis: Redis) -> None:
    uid = _uid()
    try:
        assert await set_active_model_config(redis, uid, "missing") is False
    finally:
        await _cleanup(redis, uid)


async def test_active_none_for_unknown(redis: Redis) -> None:
    uid = _uid()
    assert await get_active_model_id(redis, uid) is None
    assert await get_user_model_config(redis, uid) is None
