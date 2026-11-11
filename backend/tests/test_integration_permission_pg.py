"""真实 PostgreSQL 数据权限条件集成。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.setting import settings
from app.core.permission import Permission

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


@asynccontextmanager
async def _db() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            yield session
    finally:
        await engine.dispose()


def _tag() -> str:
    return uuid.uuid4().hex[:8]


async def _make_user(scope: int) -> tuple[object, int, str, str]:
    from app.modules.system.role.schema import RoleCreateSchema
    from app.modules.system.role.service import RoleService
    from app.modules.system.user.schema import UserCreateSchema
    from app.modules.system.user.service import UserService

    tag = _tag(); username = f"it_perm_{tag}"; role_name = f"it_perm_role_{tag}"; code = f"it_perm_{tag}"
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    async with _db() as db:
        dept_id = (await db.execute(text("SELECT id FROM sys_dept LIMIT 1"))).scalar_one_or_none()
        if not dept_id:
            pytest.skip("测试库缺少部门")
        role = await RoleService(auth, db).create(RoleCreateSchema(name=role_name, code=code, data_scope=scope))
        user = await UserService(auth, db).create(UserCreateSchema(username=username, password="Abc123!x", name="IT", dept_id=dept_id, role_ids=[role.id]))
        await db.commit()
    auth_user = SimpleNamespace(id=user.id, username=username, is_superuser=False, dept_id=dept_id)
    return SimpleNamespace(user=auth_user), user.id, username, role_name


async def _cleanup(username: str, role_name: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_user WHERE username=:u"), {"u": username})
        await db.execute(text("DELETE FROM sys_role WHERE name=:n"), {"n": role_name})
        await db.commit()


async def test_scope_all(test_client) -> None:
    auth, _, username, role_name = await _make_user(Permission.DATA_SCOPE_ALL)
    try:
        async with _db() as db:
            assert await Permission(__import__("app.modules.system.user.model", fromlist=["UserModel"]).UserModel, auth, db)._permission_condition() is None
    finally:
        await _cleanup(username, role_name)


async def test_scope_self(test_client) -> None:
    from app.modules.system.user.model import UserModel
    auth, uid, username, role_name = await _make_user(Permission.DATA_SCOPE_SELF)
    try:
        async with _db() as db:
            cond = await Permission(UserModel, auth, db)._permission_condition()
            assert cond is not None
            assert "sys_user.id" in str(cond)
    finally:
        await _cleanup(username, role_name)


async def test_scope_dept(test_client) -> None:
    from app.modules.system.user.model import UserModel
    auth, uid, username, role_name = await _make_user(Permission.DATA_SCOPE_DEPT_AND_CHILD)
    try:
        async with _db() as db:
            cond = await Permission(UserModel, auth, db)._permission_condition()
            assert cond is not None
            assert "dept_id" in str(cond)
    finally:
        await _cleanup(username, role_name)


async def test_superuser_and_anonymous(test_client) -> None:
    from app.modules.system.user.model import UserModel
    async with _db() as db:
        p = Permission(UserModel, SimpleNamespace(user=None), db)
        assert await p._permission_condition() is None
        p2 = Permission(UserModel, SimpleNamespace(user=SimpleNamespace(id=None, is_superuser=False)), db)
        assert await p2._permission_condition() is None
        p3 = Permission(UserModel, SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True)), db)
        assert await p3._permission_condition() is None


def test_permission_helpers() -> None:
    from types import SimpleNamespace
    from app.core.permission import Permission
    class Target:
        dept_id = "dept"
    rel = SimpleNamespace(property=SimpleNamespace(mapper=SimpleNamespace(class_=Target)))
    assert Permission._relationship_column(rel, "dept_id") == "dept"
    assert Permission._relationship_column(rel, "missing") is None
    assert Permission._relationship_column(None, "dept_id") is None


async def test_permission_dept_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    from app.core.permission import Permission
    svc = Permission(object, SimpleNamespace(user=SimpleNamespace(id=1, dept_id=7)), object())
    async def fail(_): raise RuntimeError("x")
    monkeypatch.setattr(Permission, "_load_dept_children", fail)
    ids = await svc._get_accessible_dept_ids({Permission.DATA_SCOPE_DEPT_AND_CHILD})
    assert ids == {7}
