"""CRUDBase 主键/预加载/清空分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.user.crud import UserCRUD


def test_loader_options() -> None:
    c = UserCRUD(SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True)), None)
    opts = c._loader_options(["roles", "roles.menus", "id", "roles"])
    assert opts is not None


async def test_clear_non_soft() -> None:
    class DB:
        async def execute(self, *a): return None
        async def flush(self): pass
    class C(UserCRUD):
        _supports_soft_delete = False
    c = C(SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True)), DB())
    await c.clear()
