"""真实 PostgreSQL 上的 AI 会话 CRUD（agno 表）。"""

from __future__ import annotations

import os
import uuid
from types import SimpleNamespace

import pytest

from app.modules.ai.chat.schema import ChatSessionCreateSchema, ChatSessionQueryParam, ChatSessionUpdateSchema
from app.modules.ai.chat.service import ChatService

pytestmark = [
    pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres"),
    pytest.mark.asyncio(loop_scope="session"),
]


@pytest.fixture(autouse=True)
def _reset_agno_db() -> None:
    """其他测试可能已在 TestClient 事件循环创建 agno 单例；本文件用 session loop，重置后重建。"""
    import app.modules.ai.chat.crud as crud
    crud._db_instance = None


def _auth():
    return SimpleNamespace(user=SimpleNamespace(username=f"it_ai_{uuid.uuid4().hex[:8]}", id=0))


async def test_ai_session_roundtrip(test_client) -> None:
    service = ChatService(_auth(), redis=None)
    created = await service.create(ChatSessionCreateSchema(title="IT"))
    assert created.session_id
    got = await service.get_session(created.session_id)
    assert got.session_id == created.session_id
    page = await service.page(1, 10, ChatSessionQueryParam())
    assert page.total >= 1
    await service.update(created.session_id, ChatSessionUpdateSchema(title="IT2"))
    assert (await service.get_session(created.session_id)).title == "IT2"
    await service.delete([created.session_id])
    with pytest.raises(Exception):
        await service.get_session(created.session_id)


async def test_ai_session_missing(test_client) -> None:
    service = ChatService(_auth(), redis=None)
    with pytest.raises(Exception):
        await service.get_session("missing-session")
    with pytest.raises(Exception):
        await service.delete(["missing-session"])


async def test_ai_session_title_search(test_client) -> None:
    service = ChatService(_auth(), redis=None)
    marker = f"IT-search-{uuid.uuid4().hex[:8]}"
    created = await service.create(ChatSessionCreateSchema(title=marker))
    try:
        page = await service.page(1, 10, ChatSessionQueryParam(title=marker))
        assert page.total >= 1
        assert any(item.title == marker for item in page.items)
    finally:
        await service.delete([created.session_id])


async def test_ai_session_update_missing(test_client) -> None:
    service = ChatService(_auth(), redis=None)
    with pytest.raises(Exception):
        await service.update("missing-session", ChatSessionUpdateSchema(title="x"))


async def test_ai_session_delete_mixed_missing(test_client) -> None:
    service = ChatService(_auth(), redis=None)
    created = await service.create(ChatSessionCreateSchema(title="IT"))
    try:
        with pytest.raises(Exception):
            await service.delete([created.session_id, "missing-session"])
        assert (await service.get_session(created.session_id)).session_id == created.session_id
    finally:
        await service.delete([created.session_id])
