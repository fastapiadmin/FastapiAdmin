"""字典类型/数据 HTTP 接口（真实 PG）。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from app.config.setting import settings

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
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


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0))


def _name() -> str:
    return f"it_dict_{uuid.uuid4().hex[:8]}"


async def _cleanup(code: str) -> None:
    from app.config.setting import settings
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.pool import NullPool
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    try:
        async with e.begin() as c:
            await c.execute(text("DELETE FROM sys_dict_data WHERE dict_type=:t"), {"t": code})
            await c.execute(text("DELETE FROM sys_dict_type WHERE dict_type=:t"), {"t": code})
    finally:
        await e.dispose()


async def test_dict_api(test_client, auth_headers) -> None:
    code = _name()
    paths = test_client.get("/openapi.json").json()["paths"]
    base = next(p for p in paths if p.endswith("/dict/type/list")).rsplit("/type/list", 1)[0]
    try:
        t = test_client.post(f"{base}/type/create", json={"dict_name": code, "dict_type": code}, headers=auth_headers)
        assert t.status_code in (200, 201), t.text
        tid = t.json()["data"]["id"]
        assert test_client.get(f"{base}/type/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/type/optionselect", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/type/detail/{tid}", headers=auth_headers).status_code == 200
        assert test_client.put(f"{base}/type/update/{tid}", json={"dict_name": code, "dict_type": code, "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/type/status/batch", json={"ids": [tid], "status": 0}, headers=auth_headers).status_code == 200
        d = test_client.post(f"{base}/data/create", json={"dict_type": code, "dict_type_id": tid, "dict_label": "L", "dict_value": "1", "dict_sort": 1, "status": 0}, headers=auth_headers)
        assert d.status_code in (200, 201), d.text
        did = d.json()["data"]["id"]
        assert test_client.get(f"{base}/data/list", params={"dict_type": code, "page_no": 1, "page_size": 10}, headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/data/info/{code}", headers=auth_headers).status_code == 200
        assert test_client.get(f"{base}/data/detail/{did}", headers=auth_headers).status_code == 200
        assert test_client.patch(f"{base}/data/status/batch", json={"ids": [did], "status": 1}, headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/data/delete", json=[did], headers=auth_headers).status_code == 200
        assert test_client.request("DELETE", f"{base}/type/delete", json=[tid], headers=auth_headers).status_code == 200
    finally:
        await _cleanup(code)


async def test_dict_cache_failures(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.exceptions import CustomException
    from app.modules.system.dict.service import DictDataService, DictTypeService
    from app.modules.system.dict.schema import DictTypeCreateSchema
    import app.modules.system.dict.service as m
    name = _name()
    class R:
        async def set(self, **k): raise RuntimeError("redis")
        async def get(self, **k): return "bad"
    async def boom(*a, **k): raise RuntimeError("redis")
    monkeypatch.setattr(m.RedisCURD, "set", boom)
    async with _db() as db:
        svc = DictTypeService(_auth(), db)
        with pytest.raises(Exception):
            await svc.create(R(), DictTypeCreateSchema(dict_name=name, dict_type=name))
    monkeypatch.setattr(m.DictDataService, "init_cache", staticmethod(boom))
    async with _db() as db:
        with pytest.raises(Exception):
            await DictDataService.get_init_cache(R(), name)
    await _cleanup(name)
