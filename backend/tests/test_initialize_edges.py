"""初始化迁移/种子数据错误分支。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from alembic import command

import pytest

import app.scripts.initialize as I


class Conn:
    def __init__(self, has): self.has = has
    async def run_sync(self, fn): return self.has
    async def execute(self, *a, **k): return SimpleNamespace()
    async def __aenter__(self): return self
    async def __aexit__(self, *a): return False


class Engine:
    def __init__(self, has): self.has = has
    def connect(self): return Conn(self.has)


async def test_apply_empty_db(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(I, "async_engine", Engine(False))
    monkeypatch.setattr(I, "create_tables", AsyncMock())
    monkeypatch.setattr(I, "ALEMBIC_VERSION_DIR", tmp_path)
    (tmp_path / "x.py").write_text("")
    monkeypatch.setattr(I.settings, "ENVIRONMENT", I.EnvironmentEnum.DEV)
    monkeypatch.setattr(I, "InitializeData", I.InitializeData)
    with patch.object(command, "stamp") as stamp, patch.object(command, "upgrade") as up:
        monkeypatch.setattr(I.InitializeData, "_InitializeData__autogen_migration", staticmethod(lambda cfg: False))
        await I.InitializeData._InitializeData__apply_migrations()
    assert stamp.called


async def test_apply_existing_and_autogen(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(I, "async_engine", Engine(True))
    monkeypatch.setattr(I, "ALEMBIC_VERSION_DIR", tmp_path)
    monkeypatch.setattr(I.settings, "ENVIRONMENT", I.EnvironmentEnum.DEV)
    monkeypatch.setattr(I.InitializeData, "_InitializeData__clear_unresolvable_alembic_version", AsyncMock())
    monkeypatch.setattr(I.InitializeData, "_InitializeData__autogen_migration", staticmethod(lambda cfg: True))
    with patch.object(command, "upgrade") as up:
        await I.InitializeData._InitializeData__apply_migrations()
    assert up.called


async def test_init_data_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.menu.model import MenuModel as M
    class DB:
        async def execute(self, *a, **k): return SimpleNamespace(scalar=lambda: 0)
    obj = object.__new__(I.InitializeData)
    obj.prepare_init_models = [M]
    monkeypatch.setattr(I.InitializeData, "_InitializeData__load_json", staticmethod(lambda n: [{"bad": 1}]))
    with pytest.raises(Exception):
        await obj._InitializeData__init_data(DB())


def test_load_json_errors(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(I, "SCRIPT_DIR", tmp_path)
    (tmp_path / "bad.json").write_text("{bad")
    with pytest.raises(Exception):
        I.InitializeData._InitializeData__load_json("bad")
    (tmp_path / "x.json").write_text("[1]")
    assert I.InitializeData._InitializeData__load_json("x") == [1]


async def test_apply_empty_no_migrations(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(I, "async_engine", Engine(False))
    monkeypatch.setattr(I, "create_tables", AsyncMock())
    monkeypatch.setattr(I, "ALEMBIC_VERSION_DIR", tmp_path)
    (tmp_path / "__init__.py").write_text("")
    monkeypatch.setattr(I.settings, "ENVIRONMENT", I.EnvironmentEnum.DEV)
    monkeypatch.setattr(I.InitializeData, "_InitializeData__autogen_migration", staticmethod(lambda cfg: False))
    with patch.object(command, "stamp") as stamp:
        await I.InitializeData._InitializeData__apply_migrations()
    assert not stamp.called


def test_load_json_directory(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(I, "SCRIPT_DIR", tmp_path)
    (tmp_path / "d.json").mkdir()
    with pytest.raises(Exception):
        I.InitializeData._InitializeData__load_json("d")


async def test_init_dict_data_empty(monkeypatch) -> None:
    from app.modules.system.dict.model import DictDataModel
    class DB:
        async def execute(self, *a, **k): return SimpleNamespace(scalar=lambda: 0)
        async def flush(self): pass
    obj = object.__new__(I.InitializeData)
    obj.prepare_init_models = [DictDataModel]
    monkeypatch.setattr(I.InitializeData, "_InitializeData__load_json", staticmethod(lambda n: [{"x": 1}]))
    monkeypatch.setattr(I.InitializeData, "_InitializeData__create_dict_data_objs", AsyncMock(return_value=[]))
    await obj._InitializeData__init_data(DB())
