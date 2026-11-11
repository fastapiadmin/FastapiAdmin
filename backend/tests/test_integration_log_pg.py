"""真实 PostgreSQL 登录/操作日志服务集成。"""

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
from app.core.exceptions import CustomException
from app.modules.system.log.model import LoginLogModel, OperationLogModel
from app.modules.system.log.service import LoginLogService, OperationLogService

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


async def _cleanup(username: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_login_log WHERE username=:u"), {"u": username})
        await db.execute(text("DELETE FROM sys_operation_log WHERE username=:u"), {"u": username})
        await db.commit()


async def test_login_log_service(test_client) -> None:
    username = f"it_log_{uuid.uuid4().hex[:8]}"
    try:
        async with _db() as db:
            obj = LoginLogModel(username=username, status=1, login_ip="127.0.0.1", msg="ok")
            db.add(obj); await db.commit(); await db.refresh(obj)
            svc = LoginLogService(_auth(), db)
            assert (await svc.page(1, 10)).total >= 1
            assert (await svc.detail(obj.id)).username == username
            with pytest.raises(CustomException):
                await svc.delete([obj.id, 99999999])
            await svc.delete([obj.id])
    finally:
        await _cleanup(username)


async def test_operation_log_service(test_client) -> None:
    username = f"it_op_{uuid.uuid4().hex[:8]}"
    try:
        async with _db() as db:
            obj = OperationLogModel(username=username, status=0, request_path="/x", request_method="GET", response_code=200)
            db.add(obj); await db.commit(); await db.refresh(obj)
            svc = OperationLogService(_auth(), db)
            assert (await svc.page(1, 10)).total >= 1
            assert (await svc.detail(obj.id)).username == username
            rows = await svc.get_list()
            assert rows
            data = await svc.export_list([x.model_dump() for x in rows])
            assert data
            with pytest.raises(CustomException):
                await svc.delete([obj.id, 99999999])
            await svc.delete([obj.id])
    finally:
        await _cleanup(username)
