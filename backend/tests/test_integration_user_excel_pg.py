"""真实 PostgreSQL + Excel 用户导入/导出集成。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from io import BytesIO
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from fastapi import UploadFile
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.modules.system.user.service import UserService

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


def _username() -> str:
    return f"it_xls_{uuid.uuid4().hex[:8]}"


def _file(rows: list[list], headers: list[str] | None = None) -> UploadFile:
    from openpyxl import Workbook
    wb = Workbook(); ws = wb.active
    ws.append(headers or ["部门编号", "账号", "昵称", "邮箱", "手机号", "性别", "状态"])
    for row in rows:
        ws.append(row)
    buf = BytesIO(); wb.save(buf); buf.seek(0)
    return UploadFile(filename="users.xlsx", file=buf)


async def _cleanup(username: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_user WHERE username=:u"), {"u": username})
        await db.commit()


async def test_template_headers(test_client) -> None:
    data = UserService.get_import_template()
    from openpyxl import load_workbook
    wb = load_workbook(BytesIO(data)); ws = wb.active
    assert [c.value for c in ws[1]] == ["部门编号", "账号", "昵称", "邮箱", "手机号", "性别", "状态"]


async def test_import_success(test_client) -> None:
    async with _db() as db:
        dept_id = (await db.execute(text("SELECT id FROM sys_dept LIMIT 1"))).scalar_one_or_none()
    if not dept_id:
        pytest.skip("测试库缺少部门")
    username = _username(); auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = UserService(auth, db)
            result = await service.batch_import(_file([[dept_id, username, "IT", None, None, "男", "正常"]]))
            await db.commit()
            assert "成功导入 1" in result
        async with _db() as db:
            assert (await db.execute(text("SELECT name FROM sys_user WHERE username=:u"), {"u": username})).scalar_one() == "IT"
    finally:
        await _cleanup(username)


async def test_import_missing_header(test_client) -> None:
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    async with _db() as db:
        service = UserService(auth, db)
        with pytest.raises(Exception, match="缺少必要"):
            await service.batch_import(_file([[1, _username(), "IT"]], headers=["部门编号", "账号"]))
