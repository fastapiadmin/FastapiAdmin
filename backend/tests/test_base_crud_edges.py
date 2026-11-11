"""CRUDBase 主键/预加载/清空分支。"""

from __future__ import annotations

import os

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


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="需要真实 PostgreSQL")
async def test_base_crud_real_branches() -> None:
    from sqlalchemy import select
    from app.config.setting import settings
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlalchemy.pool import NullPool
    from app.modules.system.user.model import UserModel
    e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
    try:
        async with async_sessionmaker(e, expire_on_commit=False)() as db:
            c = UserCRUD(SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True)), db)
            assert await c.get_list(load_columns=[UserModel.id])
            await c.page(0, 1, [], load_columns=[UserModel.id])
            await c._build_conditions(include_deleted=False, username=None)
            opts = c._loader_options(["roles.menus", "roles.permissions", "roles.menus", "id"])
            assert opts is not None
    finally:
        await e.dispose()


def test_pk_errors(monkeypatch) -> None:
    import app.core.base_crud as b
    c = UserCRUD(SimpleNamespace(user=SimpleNamespace(id=1)), None)
    monkeypatch.setattr(b, "sa_inspect", lambda m: SimpleNamespace(primary_key=[]))
    with pytest.raises(Exception):
        c._get_pk_col()
    monkeypatch.setattr(b, "sa_inspect", lambda m: SimpleNamespace(primary_key=[1, 2]))
    with pytest.raises(Exception):
        c._get_pk_col()
