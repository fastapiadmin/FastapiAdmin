"""SSE 管理器连接/订阅/广播边缘。"""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import app.core.sse_manager as S


async def test_connect_relay_listener(monkeypatch: pytest.MonkeyPatch) -> None:
    class Redis:
        async def publish(self, *a): raise RuntimeError("x")
        def pubsub(self):
            class P:
                async def subscribe(self, *a): pass
                async def listen(self):
                    yield {"type": "message", "data": "bad"}
                    yield {"type": "message", "data": json.dumps({"sender": S._PROCESS_TOKEN})}
                    yield {"type": "message", "data": json.dumps({"sender": "other", "target": {}, "data": {}})}
                async def unsubscribe(self, *a): pass
                async def close(self): pass
            return P()
    m = S.SSEConnectionManager("it")
    q = asyncio.Queue()
    m.connect(1, q, Redis())
    await m._relay({"all": True}, {"x": 1})
    await asyncio.sleep(0.01)
    m.stop_listener()
    m.disconnect(1, q)


async def test_listener_guards(monkeypatch: pytest.MonkeyPatch) -> None:
    m = S.SSEConnectionManager("it2")
    m._start_listener()
    task = SimpleNamespace(done=lambda: False, cancel=lambda: None)
    m._listener = task
    m._redis = object()
    m._start_listener()
    assert m._listener is task
    m.stop_listener()
    assert m._listener is None


async def test_listen_exception() -> None:
    class P:
        async def subscribe(self, *a): raise RuntimeError("x")
        async def unsubscribe(self, *a): pass
        async def close(self): pass
    m = S.SSEConnectionManager("it3")
    await m._listen(SimpleNamespace(pubsub=lambda: P()))


def test_stop_all(monkeypatch) -> None:
    called = []
    class M:
        def stop_listener(self): called.append(True)
    monkeypatch.setattr(S, "_managers", [M()])
    S.stop_sse_relays()
    assert called
