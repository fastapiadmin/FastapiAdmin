"""真实 PostgreSQL 菜单服务集成。"""

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
from app.modules.system.menu.service import MenuService

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


async def _cleanup(title: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM sys_menu WHERE title=:t"), {"t": title})
        await db.commit()


def _data(tag: str, title: str):
    from app.modules.system.menu.schema import MenuCreateSchema
    return MenuCreateSchema(name=f"it_{tag}", type=2, order=1, title=title, route_name=f"it_{tag}", route_path=f"/it_{tag}", component_path=f"it/{tag}")


async def test_menu_roundtrip(test_client) -> None:
    tag = _tag(); title = f"it_menu_{tag}"; auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = MenuService(auth, db)
            menu = await service.create(_data(tag, title))
            assert menu.title == title
            assert (await service.detail(menu.id)).title == title
            assert any(item["title"] == title for item in await service.tree())
            await service.delete([menu.id])
            with pytest.raises(CustomException):
                await service.detail(menu.id)
    finally:
        await _cleanup(title)


async def test_menu_duplicate_title(test_client) -> None:
    tag = _tag(); title = f"it_menu_{tag}"; auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = MenuService(auth, db)
            await service.create(_data(tag, title))
            with pytest.raises(CustomException, match="已存在"):
                await service.create(_data(tag + "_b", title))
    finally:
        await _cleanup(title)


async def test_menu_update_and_status(test_client) -> None:
    from app.modules.system.menu.schema import MenuUpdateSchema
    tag = _tag(); title = f"it_menu_{tag}"; auth = SimpleNamespace(user=SimpleNamespace(id=0))
    try:
        async with _db() as db:
            service = MenuService(auth, db)
            menu = await service.create(_data(tag, title))
            updated = await service.update(menu.id, MenuUpdateSchema(name=f"it_{tag}", type=2, order=2, title=title, route_name=f"it_{tag}", route_path=f"/it_{tag}", component_path=f"it/{tag}", status=1))
            assert updated.status == 1
    finally:
        await _cleanup(title)


async def test_menu_delete_missing_and_parent_invalid(test_client) -> None:
    tag = _tag(); title = f"it_menu_{tag}"; auth = SimpleNamespace(user=SimpleNamespace(id=0))
    async with _db() as db:
        service = MenuService(auth, db)
        await service.delete([99999999])
        data = _data(tag, title); data.parent_id = 99999999
        with pytest.raises(CustomException):
            await service.create(data)
