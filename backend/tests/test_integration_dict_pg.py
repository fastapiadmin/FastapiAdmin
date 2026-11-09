"""真实 PostgreSQL + Redis 字典类型/数据集成。"""

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
from app.modules.system.dict.service import DictDataService, DictTypeService

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


def _tag() -> str:
    return f"it_dict_{uuid.uuid4().hex[:8]}"


async def _cleanup(code: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_dict_data WHERE dict_type=:c"), {"c": code})
        await db.execute(text("DELETE FROM sys_dict_type WHERE dict_type=:c"), {"c": code})
        await db.commit()


async def _redis() -> Redis:
    return Redis(host="localhost", port=6379, db=1, decode_responses=True)


async def test_dict_type_roundtrip(test_client) -> None:
    from app.modules.system.dict.schema import DictTypeCreateSchema, DictTypeUpdateSchema
    code = _tag(); auth = SimpleNamespace(user=SimpleNamespace(id=0)); r = await _redis()
    try:
        async with _db() as db:
            service = DictTypeService(auth, db)
            item = await service.create(r, DictTypeCreateSchema(dict_name=code, dict_type=code))
            assert item.dict_type == code
            assert (await service.detail(item.id)).dict_name == code
            await service.update(r, item.id, DictTypeUpdateSchema(dict_name=code, dict_type=code, status=1))
            assert (await service.detail(item.id)).status == 1
            await service.delete(r, [item.id])
            with pytest.raises(CustomException):
                await service.detail(item.id)
    finally:
        await r.aclose(); await _cleanup(code)


async def test_dict_type_duplicate(test_client) -> None:
    from app.modules.system.dict.schema import DictTypeCreateSchema
    code = _tag(); auth = SimpleNamespace(user=SimpleNamespace(id=0)); r = await _redis()
    try:
        async with _db() as db:
            service = DictTypeService(auth, db)
            await service.create(r, DictTypeCreateSchema(dict_name=code, dict_type=code))
            with pytest.raises(CustomException, match="已存在"):
                await service.create(r, DictTypeCreateSchema(dict_name=code + "_x", dict_type=code))
    finally:
        await r.aclose(); await _cleanup(code)


async def test_dict_data_roundtrip_and_cascade(test_client) -> None:
    from app.modules.system.dict.schema import DictDataCreateSchema, DictTypeCreateSchema
    code = _tag(); auth = SimpleNamespace(user=SimpleNamespace(id=0)); r = await _redis()
    try:
        async with _db() as db:
            ts = DictTypeService(auth, db)
            typ = await ts.create(r, DictTypeCreateSchema(dict_name=code, dict_type=code))
            ds = DictDataService(auth, db)
            item = await ds.create(r, DictDataCreateSchema(dict_sort=1, dict_label="A", dict_value="a", dict_type=code, dict_type_id=typ.id))
            assert item.dict_value == "a"
            assert (await ds.detail(item.id)).dict_label == "A"
            with pytest.raises(CustomException, match="存在字典数据"):
                await ts.delete(r, [typ.id])
            await ds.delete(r, [item.id])
            await ts.delete(r, [typ.id])
    finally:
        await r.aclose(); await _cleanup(code)
