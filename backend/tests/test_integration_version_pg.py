"""版本管理服务真实 PG 集成。"""

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
from app.modules.system.versions.service import VersionService

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            yield session
    finally:
        await engine.dispose()


def _title() -> str:
    return f"it_ver_{uuid.uuid4().hex[:8]}"


async def test_version_crud(test_client) -> None:
    from app.modules.system.versions.schema import VersionCreateSchema, VersionStatusSchema, VersionUpdateSchema
    title = _title(); auth = SimpleNamespace(user=SimpleNamespace(id=0)); vid = 0
    try:
        async with _db() as db:
            svc = VersionService(auth, db)
            obj = await svc.create(VersionCreateSchema(version="1.0.0", title=title, date="2026-01-01"))
            vid = obj.id
            assert (await svc.detail(vid)).title == title
            assert (await svc.page(1, 10)).total >= 1
            await svc.update(vid, VersionUpdateSchema(version="1.0.1", title=title, date="2026-01-01"))
            await svc.set_status(vid, VersionStatusSchema(status=1))
            assert any(x.id == vid for x in await svc.get_published())
            with pytest.raises(CustomException):
                await svc.delete([vid, 99999999])
            await svc.delete([vid])
    finally:
        async with _db() as db:
            await db.execute(text("DELETE FROM sys_version WHERE title=:t"), {"t": title})
            await db.commit()
