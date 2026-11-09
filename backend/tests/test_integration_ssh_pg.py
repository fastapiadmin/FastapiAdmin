"""真实 PostgreSQL SSH 主机服务集成（连接层 mock，无本地 sshd）。"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.modules.ops.ssh import service as ssh_mod
from app.modules.ops.ssh.service import SshHostService

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


def _name() -> str:
    return f"it_ssh_{uuid.uuid4().hex[:10]}"


def _auth():
    return SimpleNamespace(user=SimpleNamespace(id=0, username="it"))


def _data(name: str):
    from app.modules.ops.ssh.schema import SshHostCreateSchema
    return SshHostCreateSchema(name=name, host="127.0.0.1", port=22, username="root", auth_type="password", password="x")


async def _cleanup(name: str) -> None:
    async with _db() as db:
        await db.execute(text("DELETE FROM ops_ssh_host WHERE name=:n"), {"n": name})
        await db.commit()


async def test_ssh_host_crud(test_client) -> None:
    from app.modules.ops.ssh.schema import SshHostUpdateSchema
    name = _name()
    try:
        async with _db() as db:
            service = SshHostService(_auth(), db)
            host = await service.create(_data(name))
            assert host.name == name and host.has_password is True
            assert (await service.detail(host.id)).name == name
            assert any(x.name == name for x in await service.get_list())
            await service.update(host.id, SshHostUpdateSchema(name=name, host="127.0.0.1", port=2222, username="root", auth_type="password"))
            assert (await service.detail(host.id)).port == 2222
            await service.delete([host.id])
            with pytest.raises(CustomException):
                await service.detail(host.id)
    finally:
        await _cleanup(name)


async def test_ssh_host_duplicate(test_client) -> None:
    name = _name()
    try:
        async with _db() as db:
            service = SshHostService(_auth(), db)
            await service.create(_data(name))
            with pytest.raises(CustomException, match="已存在"):
                await service.create(_data(name))
    finally:
        await _cleanup(name)


async def test_ssh_test_connection(test_client, monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def close(self): pass
    monkeypatch.setattr(ssh_mod, "connect_client", lambda **kw: C())
    async with _db() as db:
        service = SshHostService(_auth(), db)
        assert await service.test_connection(_data(_name())) is True
    def bad(**kw): raise RuntimeError("refused")
    monkeypatch.setattr(ssh_mod, "connect_client", bad)
    async with _db() as db:
        with pytest.raises(CustomException, match="连接失败"):
            await SshHostService(_auth(), db).test_connection(_data(_name()))
