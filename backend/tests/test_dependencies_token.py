"""WebSocket 握手令牌解析。"""

from __future__ import annotations

from types import SimpleNamespace

from app.core.dependencies import get_websocket_token


def test_token_from_subprotocol() -> None:
    ws = SimpleNamespace(headers={"sec-websocket-protocol": "access_token, access_token.jwt123"}, query_params={})
    assert get_websocket_token(ws) == ("jwt123", "access_token")


def test_token_from_query() -> None:
    ws = SimpleNamespace(headers={}, query_params={"token": "q"})
    assert get_websocket_token(ws) == ("q", None)


def test_no_token() -> None:
    ws = SimpleNamespace(headers={"sec-websocket-protocol": "access_token."}, query_params={})
    assert get_websocket_token(ws) == (None, None)
