"""Row 序列化分支（真实 PG）。"""

from __future__ import annotations

import os

import pytest
from sqlalchemy import select

from app.modules.system.user.model import UserModel
from app.modules.system.role.model import RoleModel
import app.utils.common_util as U

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


async def test_row_serialization_branches() -> None:
    from app.config.setting import settings
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    from sqlalchemy.pool import NullPool
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    try:
        async with async_sessionmaker(e, expire_on_commit=False)() as db:
            r1 = (await db.execute(select(UserModel).limit(1))).first()
            if r1:
                assert U.SqlalchemyUtil.serialize_result(r1) is not None
                assert U.SqlalchemyUtil.serialize_result(r1, "snake_to_camel") is not None
            r2 = (await db.execute(select(UserModel, RoleModel).limit(1))).first()
            if r2:
                assert U.SqlalchemyUtil.serialize_result(r2) is not None
            r3 = (await db.execute(select(UserModel.id, UserModel.username).limit(1))).first()
            if r3:
                assert U.SqlalchemyUtil.serialize_result(r3, "snake_to_camel") is not None
                assert U.SqlalchemyUtil.serialize_result(r3, "camel_to_snake") is not None
    finally:
        await e.dispose()
