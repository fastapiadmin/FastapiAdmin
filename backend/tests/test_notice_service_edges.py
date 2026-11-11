"""公告服务广播/删除守卫。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import CustomException
from app.modules.system.notice import service as S


async def test_notice_broadcast_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(S.notice_stream_manager, "broadcast", AsyncMock(side_effect=RuntimeError("x")))
    await S._broadcast_notice_update()


async def test_notice_delete_empty() -> None:
    svc = S.NoticeService(SimpleNamespace(user=SimpleNamespace(id=1)), None)
    with pytest.raises(CustomException):
        await svc.delete([])
