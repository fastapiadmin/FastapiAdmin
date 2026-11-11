"""认证核心分支与权限校验。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.dependencies import AuthPermission, _authenticate
from app.core.exceptions import CustomException


async def test_authenticate_invalid_tokens() -> None:
    for token in ("", "Bearer", "Bearer   "):
        with pytest.raises(CustomException):
            await _authenticate(token, None, None)
    with pytest.raises(CustomException):
        await _authenticate("bad.token.value", None, None)


def _auth(superuser=False, uid=1, perms=None):
    return SimpleNamespace(user=SimpleNamespace(id=uid, is_superuser=superuser), permissions=perms or [])


async def test_auth_permission() -> None:
    a = _auth(superuser=True)
    assert await AuthPermission(["x"])(a) is a
    assert await AuthPermission([])(_auth()) is not None
    assert await AuthPermission(["*"])(_auth()) is not None
    with pytest.raises(CustomException):
        await AuthPermission(["x"])(_auth())
    with pytest.raises(CustomException):
        await AuthPermission(["x"])(_auth(perms=["y"]))
    assert await AuthPermission(["x"])(_auth(perms=["x"])) is not None
