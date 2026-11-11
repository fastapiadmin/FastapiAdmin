"""角色关联 CRUD / 数据库异常分类。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import handle_exception
from app.modules.system.role.crud import RoleCRUD


async def test_role_relations() -> None:
    class Items(list):
        pass
    class DB:
        def __init__(self): self.flushed = 0
        async def flush(self): self.flushed += 1
    r = RoleCRUD(SimpleNamespace(user=SimpleNamespace(id=1)), DB())
    obj = SimpleNamespace(menus=Items([1]), depts=Items([2]))
    await r.set_role_menus_crud([obj], [9])
    await r.set_role_depts_crud([obj], [8])
    assert list(obj.menus) == [9] and list(obj.depts) == [8]


def test_integrity_error_variants() -> None:
    app = FastAPI(); handle_exception(app)
    @app.get("/fk")
    async def fk(): raise IntegrityError("stmt", {}, Exception("foreign key constraint"))
    @app.get("/null")
    async def nu(): raise IntegrityError("stmt", {}, Exception("cannot be null"))
    @app.get("/conn")
    async def co(): raise IntegrityError("stmt", {}, Exception("connection refused"))
    c = TestClient(app, raise_server_exceptions=False)
    assert c.get("/fk").status_code == 409
    assert c.get("/null").status_code == 409
    assert c.get("/conn").status_code == 503
