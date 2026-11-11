"""存储基类并发/字段定义、OAuth 渠道错误、初始化杂项。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import app.modules.task.storage.core.base as B
import app.modules.system.auth.oauth_service as O
from app.core.exceptions import CustomException


def test_field_defs() -> None:
    from pydantic import BaseModel
    class N(BaseModel):
        x: int = 1
    class M(BaseModel):
        n: N = N()
        y: int = 1
        f: float | None = None
    defs = B._field_defs(M, "local")
    assert defs


async def test_upload_many_serial(tmp_path) -> None:
    class A(B.BaseStorageAdapter):
        def _sync_upload(self, *a): return "x"
        def _sync_download(self, *a): return "x"
        def _sync_list(self, p): return []
        def _sync_delete(self, p): pass
        def _sync_exists(self, p): return False
        def _sync_mkdir(self, p): pass
        def _sync_rmdir(self, p): pass
        def _sync_rename(self, a, b): pass
        def _sync_copy(self, a, b): pass
        def _sync_test_connection(self): return True
    a = A.__new__(A)
    a.concurrency_safe = False
    a._sync_upload = lambda *x: "x"
    (tmp_path / "f").write_text("x")
    assert await a.upload_dir(str(tmp_path), "d", concurrency=1) >= 0
    a._sync_download = lambda *x: "x"
    assert await a.download_dir("d", str(tmp_path), concurrency=1) >= 0


def test_oauth_channel_edges(monkeypatch) -> None:
    import asyncio
    monkeypatch.setattr(O, "_http_json", AsyncMock(return_value=[]))
    with pytest.raises(CustomException):
        asyncio.run(O.exchange_wechat_token("a", "s", "c"))
    monkeypatch.setattr(O, "_http_text", AsyncMock(return_value="a=1"))
    with pytest.raises(CustomException):
        asyncio.run(O.exchange_qq_token("c", "s", "code", "http://cb"))
    monkeypatch.setattr(O, "_http_json", AsyncMock(return_value=[]))
    with pytest.raises(CustomException):
        asyncio.run(O.fetch_qq_profile("t", "c", "o"))
