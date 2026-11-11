"""认证会话滑动续期/状态分支。"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

import app.core.dependencies as D
from app.core.exceptions import CustomException


class R:
    def __init__(self, raw, ttl=100):
        self.raw = raw; self.ttl_val = ttl; self.calls = []
    async def get(self, key): return self.raw
    async def ttl(self, key): return self.ttl_val
    async def expire(self, **k): self.calls.append(("expire", k))
    async def delete(self, key): self.calls.append(("delete", key))
    async def set(self, **k): self.calls.append(("set", k))


def _payload(): return SimpleNamespace(is_refresh=False, sub="s")


async def test_ws_no_token() -> None:
    ws = SimpleNamespace(headers={}, query_params={}, subprotocols=[], app=SimpleNamespace(state=SimpleNamespace(redis=None)))
    with pytest.raises(CustomException):
        await D.websocket_authenticate(ws)


async def test_session_missing_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(D, "decode_access_token", lambda *a, **k: _payload())
    r = R(json.dumps({"user_name": "u"}))
    monkeypatch.setattr(D, "RedisCURD", lambda _: r)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, object())


async def test_sliding_expire_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(D, "decode_access_token", lambda *a, **k: _payload())
    monkeypatch.setattr(D.settings, "TOKEN_SLIDING_EXPIRE", True)
    r = R(json.dumps({"session_id": "s", "user_name": "u", "user_id": 1, "user_status": 1}), ttl=-1)
    monkeypatch.setattr(D, "RedisCURD", lambda _: r)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, object())
    assert any(c[0] == "expire" for c in r.calls)
    r2 = R(json.dumps({"session_id": "s", "user_name": "u", "user_id": 1, "created_at": "2000-01-01T00:00:00+00:00"}), ttl=1)
    monkeypatch.setattr(D, "RedisCURD", lambda _: r2)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, object())
    assert any(c[0] == "delete" for c in r2.calls)
    r3 = R(json.dumps({"session_id": "s", "user_name": "u", "user_id": 1, "created_at": "bad"}), ttl=1)
    monkeypatch.setattr(D, "RedisCURD", lambda _: r3)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, object())
    r4 = R(json.dumps({"session_id": "s", "user_name": "u", "user_id": 1, "user_status": 1}), ttl=1)
    monkeypatch.setattr(D, "RedisCURD", lambda _: r4)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, object())
    assert any(c[0] == "set" for c in r4.calls)


async def test_disabled_user(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(D, "decode_access_token", lambda *a, **k: _payload())
    monkeypatch.setattr(D.settings, "TOKEN_SLIDING_EXPIRE", False)
    r = R(json.dumps({"session_id": "s", "user_name": "u", "user_id": 1, "user_status": 1}))
    monkeypatch.setattr(D, "RedisCURD", lambda _: r)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, object())
