"""日志服务清理（注入当前事件循环会话，避免全局引擎关闭）。"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


async def test_service_cleanup(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.log.service as m
    engine = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def ctx():
        async with factory() as s:
            yield s

    monkeypatch.setattr(m, "async_db_session", ctx)
    with pytest.raises(ValueError):
        await m.cleanup_expired_logs(0)
    out = await m.cleanup_expired_logs(1)
    assert set(out) == {"days", "operation_deleted", "login_deleted"}
    await engine.dispose()
