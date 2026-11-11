"""用户服务/工作流服务错误分支（mock CRUD）。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.user.service import UserService
from app.modules.task.storage.workflow.service import WorkflowService


def _auth(uid=1):
    return SimpleNamespace(user=SimpleNamespace(id=uid, is_superuser=False), menu_ids=[])


async def test_user_update_dept_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as m
    class U:
        def __init__(self, *a): pass
        async def get(self, **k): return None
    class D:
        def __init__(self, *a): pass
        async def get(self, **k): return None
    monkeypatch.setattr(m, "UserCRUD", U); monkeypatch.setattr(m, "DeptCRUD", D)
    svc = UserService(_auth(), None)
    with pytest.raises(CustomException):
        await svc.update(1, SimpleNamespace(username="u", name="n", mobile=None, email=None, dept_id=9, model_dump=lambda **k: {"dept_id": 9}, role_ids=[], position_ids=[]))


async def test_user_current_update_duplicate_email(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as m
    class U:
        def __init__(self, *a): pass
        async def get(self, **k): return SimpleNamespace(id=2)
    monkeypatch.setattr(m, "UserCRUD", U)
    svc = UserService(_auth(1), None)
    with pytest.raises(CustomException):
        await svc.update_current_info(SimpleNamespace(mobile=None, email="a@b.com", model_dump=lambda: {"email": "a@b.com"}))


async def test_user_forget_password(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as m
    class U:
        def __init__(self, *a): pass
        async def get(self, **k): return SimpleNamespace(status=0, is_superuser=False)
    monkeypatch.setattr(m, "UserCRUD", U)
    assert await UserService(_auth(), None).forget_password(SimpleNamespace(username="u")) is None


async def test_user_import_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as m
    class F:
        async def read(self): return b"x"
        async def close(self): pass
    class E:
        @staticmethod
        async def aread_excel_to_dicts(c): raise RuntimeError("x")
    monkeypatch.setattr(m, "ExcelUtil", E)
    with pytest.raises(CustomException):
        await UserService(_auth(), None).batch_import(F())


async def test_workflow_prepare_empty_graph() -> None:
    svc = WorkflowService(_auth(), None)
    data = SimpleNamespace(model_dump=lambda **k: {"name": "x", "graph": None})
    with pytest.raises(CustomException):
        await svc._prepare_and_save(None, data)
