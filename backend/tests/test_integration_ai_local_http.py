"""本地 OpenAI 兼容 mock 服务上的 AI 探测（不依赖外部模型）。"""

from __future__ import annotations

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from app.core.exceptions import CustomException
from app.modules.ai.chat.service import probe_available_models, probe_model_connection

pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要集成环境")


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path.endswith("/models"):
            body = json.dumps({"data": [{"id": "mock-model", "owned_by": "mock"}]}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        else:
            self.send_response(404); self.end_headers()
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); self.rfile.read(n)
        if self.path.endswith("/chat/completions"):
            body = json.dumps({"id": "x", "object": "chat.completion", "choices": [{"index": 0, "message": {"role": "assistant", "content": "pong"}, "finish_reason": "stop"}], "usage": {"total_tokens": 1}}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        else:
            self.send_response(404); self.end_headers()


@pytest.fixture()
def mock_ai():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True); t.start()
    try:
        yield f"http://127.0.0.1:{srv.server_address[1]}/v1"
    finally:
        srv.shutdown(); srv.server_close(); t.join(timeout=2)


async def test_ai_probe_local_openai_compatible(mock_ai) -> None:
    models = await probe_available_models(mock_ai, "k")
    assert models == [{"id": "mock-model", "owned_by": "mock"}]
    result = await probe_model_connection(mock_ai, "k", "mock-model")
    assert result["ok"] is True and result["model_id"] == "mock-model"
    with pytest.raises(CustomException):
        await probe_model_connection("http://127.0.0.1:1/v1", "k", "m")
