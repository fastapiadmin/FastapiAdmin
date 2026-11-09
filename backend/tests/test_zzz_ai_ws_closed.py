"""AI WebSocket 无效令牌握手（放最后）。"""

from __future__ import annotations

import os

import pytest
from starlette.websockets import WebSocketDisconnect

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要集成环境")


def test_ai_ws_rejects_without_token(test_client) -> None:
    with pytest.raises((WebSocketDisconnect, Exception)):
        with test_client.websocket_connect("/api/v1/ai/chat/ws"):
            pass
