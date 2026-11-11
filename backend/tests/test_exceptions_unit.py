"""异常基类、HTTP 状态与超管装饰器。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core import exceptions as E


def test_resolve_http_status() -> None:
    assert E.resolve_http_status(None) == 400
    assert E.resolve_http_status(400) == 400
    assert E.resolve_http_status(999) == 400


def test_is_connection_detail() -> None:
    assert E._is_connection_detail("connection refused") is True
    assert E._is_connection_detail("timed out") is True
    assert E._is_connection_detail("bad request") is False
    assert E._is_connection_detail(None) is False


def test_custom_exception() -> None:
    e = E.CustomException(msg="x")
    assert str(e) == "x"
    assert e.code is not None


async def test_require_superadmin() -> None:
    class S:
        def __init__(self, auth): self.auth = auth
        @E.require_superadmin
        async def f(self): return "ok"
    assert await S(SimpleNamespace(user=SimpleNamespace(is_superuser=True))).f() == "ok"
    with pytest.raises(E.CustomException):
        await S(SimpleNamespace(user=SimpleNamespace(is_superuser=False))).f()
