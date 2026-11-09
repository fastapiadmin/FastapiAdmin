"""传输引擎辅助函数/外层失败回写。"""

from __future__ import annotations

import os
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import app.modules.task.storage.transfer.engine as E


def test_local_helpers(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    f = tmp_path / "a.txt"; f.write_text("x")
    task = SimpleNamespace(source_type="local", source_path=str(f))
    E._remove_local_temp(task)
    assert not f.exists()
    monkeypatch.setattr(os, "unlink", lambda *a: (_ for _ in ()).throw(OSError("x")))
    E._remove_local_temp(SimpleNamespace(source_type="local", source_path=str(f)))
    d = tmp_path / "d"; d.mkdir(); (d / "a").write_text("x")
    monkeypatch.setattr(os.path, "getsize", lambda p: (_ for _ in ()).throw(OSError("x")))
    assert E._list_local_files(str(d))[0][2] == 0


async def test_execute_transfer_task_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    class DB:
        def __init__(self): self.task = SimpleNamespace(status="pending", error_msg=None, finished_at=None)
        async def get(self, *a): return self.task
        async def commit(self): pass
    class Ctx:
        async def __aenter__(self): return DB()
        async def __aexit__(self, *a): return False
    monkeypatch.setattr(E, "async_db_session", lambda: Ctx())
    async def fail(_): raise RuntimeError("boom")
    monkeypatch.setattr(E, "_execute_transfer_task", fail)
    monkeypatch.setattr(E, "_load_steps", AsyncMock(return_value=[]))
    monkeypatch.setattr(E, "_broadcast", AsyncMock())
    await E.execute_transfer_task(1)
