"""登录前用户可用性准备。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.auth.service import LoginService


async def test_prepare_disabled() -> None:
    with pytest.raises(CustomException, match="停用"):
        await LoginService.prepare_user_for_login(db=object(), user=SimpleNamespace(status=1, id=1))


async def test_prepare_missing_after_refresh(monkeypatch) -> None:
    import app.modules.system.auth.service as mod
    class C:
        def __init__(self,*a): pass
        async def update_last_login(self, **k): return None
    monkeypatch.setattr(mod, "UserCRUD", C)
    with pytest.raises(CustomException, match="不存在"):
        await LoginService.prepare_user_for_login(db=object(), user=SimpleNamespace(status=0, id=1))
