"""真实 PostgreSQL 工单/评论服务集成。"""

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
from app.modules.system.ticket.service import TicketCommentService, TicketService

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
    return f"it_ticket_{uuid.uuid4().hex[:10]}"


async def _auth():
    async with _db() as db:
        uid = (await db.execute(text("SELECT id FROM sys_user LIMIT 1"))).scalar_one_or_none()
    if not uid:
        pytest.skip("测试库缺少用户")
    return SimpleNamespace(user=SimpleNamespace(id=uid, username=f"it_{uid}", is_superuser=True))


async def _cleanup(title: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_ticket_comment WHERE ticket_id IN (SELECT id FROM sys_ticket WHERE title=:t)"), {"t": title})
        await db.execute(text("DELETE FROM sys_ticket WHERE title=:t"), {"t": title})
        await db.commit()


async def test_ticket_roundtrip(test_client) -> None:
    from app.modules.system.ticket.schema import TicketCreateSchema, TicketUpdateSchema
    title = _title(); auth = await _auth()
    try:
        async with _db() as db:
            service = TicketService(auth, db)
            ticket = await service.create(TicketCreateSchema(title=title, ticket_content="body"))
            assert ticket.id
            assert (await service.detail(ticket.id)).title == title
            assert (await service.create(TicketCreateSchema(title=title + "_2"))).id
            await service.update(ticket.id, TicketUpdateSchema(status=1))
            await service.update(ticket.id, TicketUpdateSchema(status=2))
            assert (await service.detail(ticket.id)).status == 2
            page = await service.page(1, 10, None, None)
            assert page.total >= 1
            stats = await service.stats()
            assert stats.done >= 1
            await service.delete([ticket.id])
            with pytest.raises(CustomException):
                await service.detail(ticket.id)
    finally:
        await _cleanup(title); await _cleanup(title + "_2")


async def test_ticket_invalid_transition(test_client) -> None:
    from app.modules.system.ticket.schema import TicketCreateSchema, TicketUpdateSchema
    title = _title(); auth = await _auth()
    try:
        async with _db() as db:
            service = TicketService(auth, db)
            ticket = await service.create(TicketCreateSchema(title=title))
            with pytest.raises(CustomException):
                await service.update(ticket.id, TicketUpdateSchema(status=2))
    finally:
        await _cleanup(title)


async def test_ticket_comment_roundtrip(test_client) -> None:
    from app.modules.system.ticket.schema import TicketCommentCreateSchema, TicketCreateSchema
    title = _title(); auth = await _auth()
    try:
        async with _db() as db:
            service = TicketService(auth, db)
            ticket = await service.create(TicketCreateSchema(title=title))
            comments = TicketCommentService(auth, db)
            c = await comments.create(ticket.id, TicketCommentCreateSchema(content="hello"))
            assert c.ticket_id == ticket.id
            page = await comments.page(ticket.id, 1, 10)
            assert page.total == 1
            await comments.delete(c.id)
            with pytest.raises(CustomException):
                await comments.delete(c.id)
    finally:
        await _cleanup(title)


async def test_ticket_delete_missing(test_client) -> None:
    auth = await _auth()
    async with _db() as db:
        await TicketService(auth, db).delete([99999999])


async def test_ticket_batch_and_export(test_client) -> None:
    from app.modules.system.ticket.schema import TicketBatchSchema, TicketCreateSchema
    title = _title(); auth = await _auth()
    try:
        async with _db() as db:
            svc = TicketService(auth, db)
            a = await svc.create(TicketCreateSchema(title=title))
            b = await svc.create(TicketCreateSchema(title=title + "_b"))
            await svc.batch(TicketBatchSchema(ids=[a.id], status=1))
            data = await TicketService.export_list([a.model_dump(), b.model_dump()])
            assert data
            with pytest.raises(CustomException):
                await svc.batch(TicketBatchSchema(ids=[99999999], status=1))
    finally:
        await _cleanup(title); await _cleanup(title + "_b")
