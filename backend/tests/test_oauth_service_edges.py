"""GitHub OAuth token 错误分支。"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import app.modules.system.auth.oauth_service as O
from app.core.exceptions import CustomException


def test_github_token_edges(monkeypatch: pytest.MonkeyPatch) -> None:
    import asyncio
    monkeypatch.setattr(O, "_http_json", AsyncMock(return_value=[]))
    with pytest.raises(CustomException):
        asyncio.run(O.exchange_github_token("c", "s", "code", "http://cb"))
    monkeypatch.setattr(O, "_http_json", AsyncMock(return_value={}))
    with pytest.raises(CustomException):
        asyncio.run(O.exchange_github_token("c", "s", "code", "http://cb"))
