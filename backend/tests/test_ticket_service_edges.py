"""工单服务错误/查询分支。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import CustomException
from app.modules.system.ticket.service import TicketService


def _svc():
    return TicketService(SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True)), None)


async def test_ticket_create_none(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = _svc()
    monkeypatch.setattr("app.modules.system.ticket.service.TicketCRUD", lambda *a: SimpleNamespace(create=AsyncMock(return_value=None)))
    with pytest.raises(CustomException):
        await svc.create(SimpleNamespace())


async def test_ticket_update_none(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = _svc()
    class C:
        def __init__(self, *a): pass
        async def get_or_404(self, **k): return SimpleNamespace(status=0, created_id=1, assigned_id=2)
        async def update(self, **k): return None
    monkeypatch.setattr("app.modules.system.ticket.service.TicketCRUD", C)
    with pytest.raises(CustomException):
        await svc.update(1, SimpleNamespace(status=None, assigned_id=None))


async def test_ticket_update_assignee_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = _svc()
    class U:
        def __init__(self, *a): pass
        async def exists(self, **k): return False
    monkeypatch.setattr("app.modules.system.ticket.service.UserCRUD", U)
    class C:
        def __init__(self, *a): pass
        async def get_or_404(self, **k): return SimpleNamespace(status=0, created_id=1, assigned_id=2)
    monkeypatch.setattr("app.modules.system.ticket.service.TicketCRUD", C)
    with pytest.raises(CustomException):
        await svc.update(1, SimpleNamespace(status=None, assigned_id=99))


async def test_ticket_delete_empty() -> None:
    with pytest.raises(CustomException):
        await _svc().delete([])
