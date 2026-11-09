"""SSE 连接管理器本地推送语义。"""

from __future__ import annotations

import asyncio

import pytest

from app.core.sse_manager import SSEConnectionManager


async def test_connect_disconnect() -> None:
    m = SSEConnectionManager("it")
    q1, q2 = asyncio.Queue(), asyncio.Queue()
    m.connect(1, q1); m.connect(1, q2); m.connect(2, asyncio.Queue())
    assert len(m.all_connections()) == 3
    m.disconnect(1, q1); m.disconnect(1, q1)
    assert len(m.all_connections()) == 2
    m.disconnect(1, q2); m.disconnect(99, q2)
    assert len(m.all_connections()) == 1


async def test_send_to_user() -> None:
    m = SSEConnectionManager("it"); q = asyncio.Queue()
    m.connect(1, q)
    await m.send_to_user(None, {"a": 1})
    assert q.empty()
    await m.send_to_user(1, {"a": 1})
    assert q.get_nowait() == {"a": 1}


async def test_send_to_users_dedup() -> None:
    m = SSEConnectionManager("it"); q1, q2 = asyncio.Queue(), asyncio.Queue()
    m.connect(1, q1); m.connect(2, q2)
    await m.send_to_users([1, 2, 1], {"x": 1})
    assert q1.get_nowait() == {"x": 1} and q2.get_nowait() == {"x": 1}
    await m.send_to_users([], {"x": 2})
    assert q1.empty()


async def test_broadcast_all() -> None:
    m = SSEConnectionManager("it"); q1, q2 = asyncio.Queue(), asyncio.Queue()
    m.connect(1, q1); m.connect(2, q2)
    await m.broadcast({"all": True})
    assert q1.get_nowait() == {"all": True} and q2.get_nowait() == {"all": True}


async def test_slow_consumer_removed() -> None:
    m = SSEConnectionManager("it"); q = asyncio.Queue(maxsize=1)
    m.connect(1, q)
    await m.send_to_user(1, {"a": 1})
    await m.send_to_user(1, {"a": 2})
    assert q.qsize() == 1
    assert m.all_connections() == []


async def test_relay_redis_publish() -> None:
    m = SSEConnectionManager("it"); q = asyncio.Queue(); m.connect(1, q)
    class R:
        def __init__(self): self.messages=[]
        async def publish(self, channel, message): self.messages.append((channel, message))
    r=R(); m._redis=r
    await m.send_to_user(1, {"a": 1})
    assert r.messages and q.get_nowait() == {"a": 1}


async def test_listen_dispatch_and_skip() -> None:
    import json
    from app.core.sse_manager import _PROCESS_TOKEN
    m = SSEConnectionManager("it"); q = asyncio.Queue(); m.connect(1, q)
    class PS:
        async def subscribe(self, c): pass
        async def unsubscribe(self, c): pass
        async def close(self): pass
        async def listen(self):
            yield {"type": "message", "data": json.dumps({"sender": "other", "target": {"users": [1]}, "data": {"a": 1}})}
            yield {"type": "message", "data": "bad-json"}
            yield {"type": "message", "data": json.dumps({"sender": _PROCESS_TOKEN, "target": {"users": [1]}, "data": {"a": 2}})}
            yield {"type": "subscribe", "data": 1}
    class R:
        def pubsub(self): return PS()
    await m._listen(R())
    assert q.get_nowait() == {"a": 1}
    assert q.empty()
