"""AI WebSocket 控制器消息循环（fake WebSocket，不依赖网络）。"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from starlette.websockets import WebSocketDisconnect

import app.modules.ai.chat.controller as C


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=1, username="u", is_superuser=True), permissions=["*:*:*"])


class FakeWS:
    def __init__(self, messages):
        self.messages = list(messages)
        self.sent = []
        self.app = SimpleNamespace(state=SimpleNamespace(redis=None))
        self.headers = {}
        self.query_params = {}
        self.client = ("127.0.0.1", 1)
    async def accept(self, subprotocol=None): self.accepted = subprotocol
    async def close(self, code=1000, reason=""): self.closed = code
    async def receive_text(self):
        if self.messages:
            return self.messages.pop(0)
        raise WebSocketDisconnect(1000)
    async def send_text(self, text):
        if getattr(self, "fail_send", False):
            raise RuntimeError("closed")
        self.sent.append(text)


async def test_ws_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    async def auth(ws): return _auth(), None
    async def model(redis, uid): return None
    class Svc:
        def __init__(self, *a, **k): pass
        async def chat_query(self, query, stop_event=None, model_config=None):
            yield "a"; yield "b"
    monkeypatch.setattr(C, "websocket_authenticate", auth)
    monkeypatch.setattr(C, "get_user_model_config", model)
    monkeypatch.setattr(C, "ChatService", Svc)
    ws = FakeWS([
        "not-json",
        json.dumps({"action": "stop"}),
        json.dumps({"message": "hi", "session_id": "s"}),
    ])
    await C.websocket_chat_controller(ws)
    assert "消息格式错误" in ws.sent[0]
    assert ws.sent[1] == "当前没有正在进行的生成任务"
    assert "a" in ws.sent and "b" in ws.sent and "[DONE]" in ws.sent


async def test_ws_auth_and_permission_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    async def bad(ws): raise RuntimeError("bad")
    monkeypatch.setattr(C, "websocket_authenticate", bad)
    ws = FakeWS([])
    await C.websocket_chat_controller(ws)
    assert ws.closed == 4001
    async def auth(ws): return SimpleNamespace(user=SimpleNamespace(id=2, username="u", is_superuser=False), permissions=[]), None
    monkeypatch.setattr(C, "websocket_authenticate", auth)
    ws2 = FakeWS([])
    await C.websocket_chat_controller(ws2)
    assert ws2.closed == 4003


async def test_ws_error_path_and_close(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.exceptions import CustomException
    async def auth(ws): return _auth(), None
    class Svc:
        def __init__(self, *a, **k): pass
        async def chat_query(self, query, stop_event=None, model_config=None):
            if False: yield None
            raise CustomException(msg="业务错误")
    monkeypatch.setattr(C, "websocket_authenticate", auth)
    monkeypatch.setattr(C, "ChatService", Svc)
    class M:
        async def __call__(self, redis, uid): return None
    monkeypatch.setattr(C, "get_user_model_config", M())
    ws = FakeWS([json.dumps({"message": "hi"})])
    await C.websocket_chat_controller(ws)
    assert any("业务错误" in s for s in ws.sent)


async def test_send_error_and_close(monkeypatch: pytest.MonkeyPatch) -> None:
    class Bad:
        async def send_text(self, *a): raise RuntimeError("x")
        async def close(self, *a, **k): raise RuntimeError("x")
    await C._send_error_and_close(Bad(), "err")


async def test_schema_error_and_unknown(monkeypatch: pytest.MonkeyPatch) -> None:
    async def auth(ws): return _auth(), None
    monkeypatch.setattr(C, "websocket_authenticate", auth)
    ws = FakeWS([json.dumps({"message": {"a": 1}})])
    await C.websocket_chat_controller(ws)
    assert any("消息格式错误" in s for s in ws.sent)
    class BadSvc:
        def __init__(self, *a, **k): raise RuntimeError("x")
    monkeypatch.setattr(C, "ChatService", BadSvc)
    class M:
        async def __call__(self, redis, uid): return None
    monkeypatch.setattr(C, "get_user_model_config", M())
    ws2 = FakeWS([json.dumps({"message": "hi"})])
    await C.websocket_chat_controller(ws2)


async def test_ws_empty_chunk_and_send_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    async def auth(ws): return _auth(), None
    async def model(redis, uid): return None
    class Svc:
        def __init__(self, *a, **k): pass
        async def chat_query(self, query, stop_event=None, model_config=None):
            yield ""; yield "a"
    monkeypatch.setattr(C, "websocket_authenticate", auth)
    monkeypatch.setattr(C, "get_user_model_config", model)
    monkeypatch.setattr(C, "ChatService", Svc)
    ws = FakeWS([json.dumps({"message": "hi"})])
    await C.websocket_chat_controller(ws)
    assert "a" in ws.sent
    ws2 = FakeWS([json.dumps({"message": "hi"})]); ws2.fail_send = True
    await C.websocket_chat_controller(ws2)
