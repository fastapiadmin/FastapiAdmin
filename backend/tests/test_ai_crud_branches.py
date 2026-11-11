"""AI 会话 CRUD 错误/分支。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import app.modules.ai.chat.crud as C
from app.core.exceptions import CustomException



def test_row_session_name() -> None:
    assert C._row_session_name({"session_data": '{"session_name":"x"}'}) == "x"
    assert C._row_session_name({"session_data": "bad"}) == ""
    assert C._row_session_name({"session_data": {"session_name": "y"}}) == "y"
    assert C._row_session_name({}) == ""


async def test_init_tables_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class D:
        async def _create_all_tables(self): raise RuntimeError("exists")
    monkeypatch.setattr(C, "_get_agno_db", lambda: D())
    await C.init_agno_tables()


async def test_session_crud_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    crud = C.ChatSessionCRUD(SimpleNamespace(user=SimpleNamespace(id=1, username="u")))
    class DB:
        async def get_sessions(self, **k): raise RuntimeError("x")
        async def upsert_session(self, **k): raise RuntimeError("x")
        async def rename_session(self, **k): raise RuntimeError("x")
        async def delete_session(self, **k): raise RuntimeError("x")
    crud.db = DB()
    with pytest.raises(Exception):
        await crud.page(1, 10, None)
    with pytest.raises(Exception):
        await crud.create(C.ChatSessionCreateSchema(title="t"))
    with pytest.raises(Exception):
        await crud.rename("s", C.ChatSessionUpdateSchema(title="t"))
    with pytest.raises(Exception):
        await crud.delete(["s"])


async def test_create_none_and_delete_error(monkeypatch: pytest.MonkeyPatch) -> None:
    crud = C.ChatSessionCRUD(SimpleNamespace(user=SimpleNamespace(id=1, username="u")))
    class DB:
        async def upsert_session(self, **k): return None
        async def delete_session(self, **k): raise RuntimeError("x")
    crud.db = DB()
    with pytest.raises(RuntimeError):
        await crud.create(C.ChatSessionCreateSchema(title="t"))
    with pytest.raises(Exception):
        await crud.delete(["s"])


def test_unsupported_db(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.ai.chat.crud as mod
    monkeypatch.setattr(mod, "_db_instance", None)
    monkeypatch.setattr(mod, "settings", SimpleNamespace(DATABASE_TYPE="oracle", ASYNC_DB_URI="x"))
    with pytest.raises(RuntimeError):
        mod._get_agno_db()
