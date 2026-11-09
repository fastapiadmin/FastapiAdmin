"""初始化种子数据逻辑（DB 以轻量 fake 替代）。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.scripts.initialize import InitializeData


class _Result:
    def __init__(self, rows=None, scalar=0):
        self._rows = rows or []; self._scalar = scalar
    def all(self): return self._rows
    def scalar(self): return self._scalar


async def test_init_data_skips_empty_and_existing(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.dict.model import DictDataModel
    svc = object.__new__(InitializeData)
    svc.prepare_init_models = [DictDataModel]
    monkeypatch.setattr(svc, "_InitializeData__load_json", lambda name: [])
    class DB:
        async def execute(self,*a,**k): return _Result(scalar=1)
    await svc._InitializeData__init_data(DB())


async def test_init_data_existing_rows_skipped(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.dict.model import DictDataModel
    svc = object.__new__(InitializeData); svc.prepare_init_models=[DictDataModel]
    monkeypatch.setattr(svc, "_InitializeData__load_json", lambda name: [{"dict_label":"x"}])
    class DB:
        async def execute(self,*a,**k): return _Result(scalar=1)
    await svc._InitializeData__init_data(DB())


async def test_create_dict_data_objs(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.dict.model import DictDataModel
    class DB:
        async def execute(self,*a,**k): return _Result(rows=[("k", 1)])
    objs = await InitializeData._InitializeData__create_dict_data_objs(DB(), [{"dict_type":"k","dict_label":"x"},{"dict_type":"missing"},{"dict_type":1}])
    assert len(objs) == 1 and objs[0].dict_type_id == 1


def test_create_objects_with_children() -> None:
    class M:
        def __init__(self, **kw): self.__dict__.update(kw)
    objs = InitializeData._InitializeData__create_objects_with_children([{"name":"p","children":[{"name":"c"}]}], M)
    assert objs[0].name == "p" and objs[0].children[0].name == "c"


def test_load_json_missing(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.scripts.initialize.SCRIPT_DIR", tmp_path)
    assert InitializeData._InitializeData__load_json("nope") == []


async def test_init_data_writes_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.dict.model import DictDataModel
    svc = object.__new__(InitializeData); svc.prepare_init_models=[DictDataModel]
    monkeypatch.setattr(svc, "_InitializeData__load_json", lambda name: [{"dict_type":"k","dict_label":"x"}])
    class R:
        def __init__(self,rows=None,scalar=0): self._rows=rows or []; self._scalar=scalar
        def all(self): return self._rows
        def scalar(self): return self._scalar
    class DB:
        def __init__(self): self.added=[]; self.flushed=False
        async def execute(self,*a,**k):
            return R(rows=[("k",1)]) if "dict_type" in str(a[0]).lower() else R(scalar=0)
        def add_all(self,objs): self.added.extend(objs)
        async def flush(self): self.flushed=True
    db=DB(); await svc._InitializeData__init_data(db)
    assert db.added and db.flushed
