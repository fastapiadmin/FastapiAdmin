"""数据库引擎创建/建表失败分支。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import app.core.database as D


def test_create_sync_engine_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(D, "create_engine", lambda **k: (_ for _ in ()).throw(RuntimeError("x")))
    with pytest.raises(RuntimeError):
        D.create_sync_engine("sqlite://")


async def test_create_async_sqlite_pragma(monkeypatch: pytest.MonkeyPatch) -> None:
    eng, factory = D.create_async_engine_and_session("sqlite+aiosqlite:///:memory:")
    try:
        async with eng.connect() as conn:
            await conn.exec_driver_sql("SELECT 1")
    finally:
        await eng.dispose()


def test_create_async_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(D, "create_async_engine", lambda **k: (_ for _ in ()).throw(RuntimeError("x")))
    with pytest.raises(RuntimeError):
        D.create_async_engine_and_session("postgresql+asyncpg://x")


async def test_create_drop_tables_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class Ctx:
        async def __aenter__(self): raise RuntimeError("x")
        async def __aexit__(self, *a): return False
    class Eng:
        def begin(self): return Ctx()
    monkeypatch.setattr(D, "async_engine", Eng())
    with pytest.raises(RuntimeError):
        await D.create_tables()
    with pytest.raises(RuntimeError):
        await D.drop_tables()
