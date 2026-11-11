"""用户服务守卫分支（真实 PG）。"""

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
from app.modules.system.user.service import UserService

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    f = async_sessionmaker(e, expire_on_commit=False)
    try:
        async with f() as s:
            yield s
    finally:
        await e.dispose()


def _auth(uid, superuser=True):
    return SimpleNamespace(user=SimpleNamespace(id=uid, is_superuser=superuser))


async def test_user_service_no_id_guards(test_client) -> None:
    async with _db() as db:
        svc = UserService(_auth(None), db)
        with pytest.raises(CustomException):
            await svc.current_info()
        with pytest.raises(CustomException):
            await svc.update_current_info(SimpleNamespace(mobile=None, email=None, name="x", avatar=None))


async def test_user_import_errors(test_client) -> None:
    import io
    from starlette.datastructures import UploadFile
    from app.core.exceptions import CustomException
    async with _db() as db:
        svc = UserService(_auth(0), db)
        with pytest.raises(CustomException):
            await svc.batch_import(UploadFile(filename="a.txt", file=io.BytesIO(b"not excel")))
        with pytest.raises(CustomException):
            await svc.batch_import(UploadFile(filename="a.txt", file=io.BytesIO(b"")))


async def test_user_load_menus_empty(test_client) -> None:
    async with _db() as db:
        from app.core.base_schema import AuthSchema
        auth = AuthSchema(user=__import__("types").SimpleNamespace(id=1, is_superuser=False), menu_ids=[])
        svc = UserService(auth, db)
        assert await svc._load_menus() == []


async def test_user_import_custom_and_fields(test_client) -> None:
    import io
    from starlette.datastructures import UploadFile
    from openpyxl import Workbook
    from app.core.exceptions import CustomException
    import app.modules.system.user.service as m
    class E:
        @staticmethod
        async def aread_excel_to_dicts(c): raise CustomException(msg="x")
    old = m.ExcelUtil
    m.ExcelUtil = E
    try:
        async with _db() as db:
            with pytest.raises(CustomException):
                await UserService(_auth(0), db).batch_import(UploadFile(filename="a.xlsx", file=io.BytesIO(b"x")))
    finally:
        m.ExcelUtil = old
    wb = Workbook(); ws = wb.active; ws.append(["部门编号", "账号", "昵称"]); ws.append([None, "u", "n"])
    bio = io.BytesIO(); wb.save(bio); bio.seek(0)
    async with _db() as db:
        with pytest.raises(CustomException):
            await UserService(_auth(0), db).batch_import(UploadFile(filename="a.xlsx", file=bio))
