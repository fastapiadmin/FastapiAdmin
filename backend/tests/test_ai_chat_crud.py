"""AI 会话 CRUD 数据层分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.ai.chat.crud import ChatSessionCRUD
from app.modules.ai.chat.schema import ChatSessionCreateSchema, ChatSessionUpdateSchema


def _crud(db):
    c = ChatSessionCRUD.__new__(ChatSessionCRUD)
    c.auth = object(); c.user_id = "u"; c.team_id = "t"; c.db = db
    return c


async def test_get_by_id_success_and_error() -> None:
    class DB:
        async def get_session(self, **kw): return "s"
    assert await _crud(DB()).get_by_id("x") == "s"
    class Bad:
        async def get_session(self, **kw): raise RuntimeError()
    assert await _crud(Bad()).get_by_id("x") is None


async def test_list_page_tuple_and_title() -> None:
    class DB:
        async def get_sessions(self, **kw):
            return ([{"session_data": '{"session_name":"Alpha"}'}, {"session_data": '{"session_name":"Beta"}'}], 2)
    rows, total = await _crud(DB()).list_page(1, 10)
    assert total == 2 and len(rows) == 2
    rows, total = await _crud(DB()).list_page(1, 10, title="alp", order_by=[{"created_time": "asc"}])
    assert total == 1 and len(rows) == 1


async def test_create_rename_delete() -> None:
    from agno.team.team import TeamSession
    class DB:
        def __init__(self): self.renamed = []; self.deleted = []
        async def upsert_session(self, session): return session
        async def rename_session(self, **kw): self.renamed.append(kw); return True
        async def delete_session(self, **kw): self.deleted.append(kw)
    db = DB(); c = _crud(db)
    session = await c.create(ChatSessionCreateSchema(title="T"))
    assert session.session_data["session_name"] == "T"
    await c.rename("s", ChatSessionUpdateSchema(title="N"))
    assert db.renamed[0]["session_name"] == "N"
    await c.delete(["s"])
    assert db.deleted[0]["session_id"] == "s"


async def test_rename_missing_and_delete_error() -> None:
    class DB:
        async def rename_session(self, **kw): return None
        async def delete_session(self, **kw): raise RuntimeError()
    c = _crud(DB())
    with pytest.raises(CustomException, match="会话不存在"):
        await c.rename("s", ChatSessionUpdateSchema(title="N"))
    with pytest.raises(RuntimeError):
        await c.delete(["s"])
