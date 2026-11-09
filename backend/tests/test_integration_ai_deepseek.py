"""真实 OpenAI 兼容 AI 端点（凭据来自 env/.env.dev，不落仓库）。"""

from __future__ import annotations

import os
import uuid
from types import SimpleNamespace

import pytest

from app.config.setting import settings

pytestmark = [
    pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1" or not settings.OPENAI_API_KEY, reason="需要真实 AI 凭据"),
    pytest.mark.asyncio(loop_scope="session"),
]


@pytest.fixture(autouse=True)
def _reset_agno_db() -> None:
    import app.modules.ai.chat.crud as crud
    crud._db_instance = None


async def test_real_ai_non_stream(test_client) -> None:
    from app.modules.ai.chat.service import ChatService
    auth = SimpleNamespace(user=SimpleNamespace(id=1, username=f"it_ai_{uuid.uuid4().hex[:6]}", is_superuser=False))
    out = await ChatService(auth, redis=None).chat_non_stream(
        "只回复 pong",
        None,
        {"base_url": settings.OPENAI_BASE_URL, "api_key": settings.OPENAI_API_KEY, "model_id": settings.OPENAI_MODEL},
    )
    assert out["session_id"]
    assert out["response"] and "AI 服务暂时不可用" not in out["response"]
