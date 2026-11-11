"""传输 SSE 控制器生成器分支。"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

import app.modules.task.storage.transfer.controller as C


async def test_stream_generator(monkeypatch: pytest.MonkeyPatch) -> None:
    class Q:
        def __init__(self, *a, **k): self.n = 0
        async def get(self):
            self.n += 1
            if self.n == 1: return {"type": "task_update", "data": {"id": 1}}
            raise asyncio.CancelledError
    class M:
        def connect(self, *a, **k): pass
        def disconnect(self, *a, **k): pass
    monkeypatch.setattr(C.asyncio, "Queue", Q)
    monkeypatch.setattr(C, "transfer_stream_manager", M())
    req = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(redis=None)))
    auth = SimpleNamespace(user=SimpleNamespace(id=1))
    gen = C.transfer_stream_controller(auth, req)
    ev = await anext(gen)
    assert ev.event == "task_update"
    with pytest.raises(asyncio.CancelledError):
        await anext(gen)
    await gen.aclose()
