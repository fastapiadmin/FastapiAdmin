"""真实 PostgreSQL 服务层集成：角色/用户 CRUD 与约束。"""

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
from app.core.exceptions import CustomException

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
    return uuid.uuid4().hex[:10]


async def _cleanup_user(username: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_user WHERE username=:u"), {"u": username})
        await db.commit()


async def _cleanup_role(name: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_role WHERE name=:n"), {"n": name})
        await db.commit()


async def test_role_service_roundtrip(test_client) -> None:
    from app.modules.system.role.schema import RoleCreateSchema, RoleUpdateSchema
    from app.modules.system.role.service import RoleService

    tag = _tag(); name = f"it_role_{tag}"; code = f"it_{tag}"
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = RoleService(auth, db)
            role = await service.create(RoleCreateSchema(name=name, code=code))
            assert role.name == name
            updated = await service.update(role.id, RoleUpdateSchema(name=name + "_x", code=code))
            assert updated.name == name + "_x"
            page = await service.page(1, 10, None, None)
            assert page.total >= 1
            await service.delete([role.id])
    finally:
        await _cleanup_role(name); await _cleanup_role(name + "_x")


async def test_role_service_duplicate(test_client) -> None:
    from app.modules.system.role.schema import RoleCreateSchema
    from app.modules.system.role.service import RoleService

    tag = _tag(); name = f"it_role_{tag}"; code = f"it_{tag}"
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = RoleService(auth, db)
            await service.create(RoleCreateSchema(name=name, code=code))
            with pytest.raises(CustomException, match="已存在"):
                await service.create(RoleCreateSchema(name=name, code=code + "b"))
    finally:
        await _cleanup_role(name)


async def test_user_service_roundtrip(test_client) -> None:
    from app.modules.system.user.schema import UserCreateSchema, UserUpdateSchema
    from app.modules.system.user.service import UserService

    tag = _tag(); username = f"it_{tag}"
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = UserService(auth, db)
            user = await service.create(UserCreateSchema(username=username, password="Abc123!x", name="IT"))
            assert user.username == username
            got = await service.detail(user.id)
            assert got.id == user.id
            await service.update(user.id, UserUpdateSchema(name="IT2"))
            assert (await service.detail(user.id)).name == "IT2"
            page = await service.page(1, 10)
            assert page.total >= 1
            await service.delete([user.id])
    finally:
        await _cleanup_user(username)


async def test_user_service_duplicate(test_client) -> None:
    from app.modules.system.user.schema import UserCreateSchema
    from app.modules.system.user.service import UserService

    tag = _tag(); username = f"it_{tag}"
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = UserService(auth, db)
            await service.create(UserCreateSchema(username=username, password="Abc123!x", name="IT"))
            with pytest.raises(CustomException, match="已存在"):
                await service.create(UserCreateSchema(username=username, password="Abc123!x", name="IT"))
    finally:
        await _cleanup_user(username)


async def test_user_role_assignment(test_client) -> None:
    from app.modules.system.role.schema import RoleCreateSchema
    from app.modules.system.role.service import RoleService
    from app.modules.system.user.schema import UserCreateSchema, UserUpdateSchema
    from app.modules.system.user.service import UserService

    tag = _tag(); username = f"it_{tag}"; role_name = f"it_role_{tag}"; code = f"it_{tag}"
    auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            role = await RoleService(auth, db).create(RoleCreateSchema(name=role_name, code=code))
            us = UserService(auth, db)
            user = await us.create(UserCreateSchema(username=username, password="Abc123!x", name="IT", role_ids=[role.id]))
            got = await us.detail(user.id)
            assert got.role_ids == [role.id]
            await us.update(user.id, UserUpdateSchema(role_ids=[]))
            assert (await us.detail(user.id)).role_ids == []
    finally:
        await _cleanup_user(username); await _cleanup_role(role_name)


async def test_user_role_invalid_id(test_client) -> None:
    from app.modules.system.user.schema import UserCreateSchema
    from app.modules.system.user.service import UserService

    tag = _tag(); username = f"it_{tag}"; auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            with pytest.raises(CustomException, match="角色不存在"):
                await UserService(auth, db).create(UserCreateSchema(username=username, password="Abc123!x", name="IT", role_ids=[99999999]))
    finally:
        await _cleanup_user(username)
