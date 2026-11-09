"""真实 PostgreSQL 公告与已读状态集成。"""

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
from app.modules.system.notice.service import NoticeService

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


def _title() -> str:
    return f"it_notice_{uuid.uuid4().hex[:10]}"


async def _auth() -> SimpleNamespace:
    async with _db() as db:
        uid = (await db.execute(text("SELECT id FROM sys_user LIMIT 1"))).scalar_one_or_none()
    if not uid:
        pytest.skip("测试库缺少用户")
    return SimpleNamespace(user=SimpleNamespace(id=uid, username=f"it_{uid}", is_superuser=False))


async def _cleanup(title: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_notice_read WHERE notice_id IN (SELECT id FROM sys_notice WHERE notice_title=:t)"), {"t": title})
        await db.execute(text("DELETE FROM sys_notice WHERE notice_title=:t"), {"t": title})
        await db.commit()


async def test_notice_read_state(test_client) -> None:
    from app.modules.system.notice.schema import NoticeCreateSchema
    title = _title(); auth = await _auth()
    try:
        async with _db() as db:
            service = NoticeService(auth, db)
            notice = await service.create(NoticeCreateSchema(notice_title=title, notice_type="1", notice_content="body", status=0))
            await db.commit()
            page = await service.available_page()
            assert page.page_size == 10 and page.total >= 1
            ids = await service.read_ids(auth.user.id)
            assert notice.id not in ids
            assert await service.unread_count(auth.user.id) >= 0
            assert await service.mark_read(auth.user.id, [notice.id]) >= 1
            await db.commit()
            assert notice.id in await service.read_ids(auth.user.id)
            assert await service.unread_count(auth.user.id) >= 0
    finally:
        await _cleanup(title)


async def test_notice_crud(test_client) -> None:
    from app.modules.system.notice.schema import NoticeCreateSchema, NoticeUpdateSchema
    title = _title(); auth = await _auth()
    try:
        async with _db() as db:
            service = NoticeService(auth, db)
            notice = await service.create(NoticeCreateSchema(notice_title=title, notice_type="2", notice_content="body", status=0))
            assert (await service.detail(notice.id)).notice_title == title
            updated = await service.update(notice.id, NoticeUpdateSchema(notice_title=title, notice_type="2", status=1))
            assert updated.status == 1
            await service.delete([notice.id])
    finally:
        await _cleanup(title)
