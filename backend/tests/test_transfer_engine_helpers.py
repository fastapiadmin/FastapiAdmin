"""传输引擎纯函数与步骤展开测试。"""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.modules.task.storage.core.base import StorageObject
from app.modules.task.storage.transfer import engine
from app.modules.task.storage.transfer.schema import TransferTaskCreateSchema
from app.modules.task.storage.transfer.service import StorageTransferService


def test_local_path_size_and_files(tmp_path: Path) -> None:
    root = tmp_path / "root"
    (root / "a").mkdir(parents=True)
    (root / "a" / "x.txt").write_text("xx")
    (root / "y.txt").write_text("y")
    assert engine._local_path_size(str(root / "y.txt")) == 1
    assert engine._local_path_size(str(root)) == 3
    assert engine._local_path_size(str(root / "missing")) == 0
    files = engine._list_local_files(str(root))
    assert len(files) == 2 and {rel for _, rel, _ in files} == {"a/x.txt", "y.txt"}


def test_prepare_local_dirs(tmp_path: Path) -> None:
    p1 = tmp_path / "a" / "x.txt"
    p2 = tmp_path / "b" / "y.txt"
    engine._prepare_local_dirs([str(p1), str(p2), ""])
    assert p1.parent.is_dir() and p2.parent.is_dir()


async def test_remove_temp_and_size_helpers(tmp_path: Path) -> None:
    f = tmp_path / "f.txt"
    f.write_text("x")
    task = SimpleNamespace(source_type="local", source_path=str(f))
    engine._remove_local_temp(task)
    assert not f.exists()
    d = tmp_path / "d"
    d.mkdir()
    await engine._remove_local_temp_dir(str(d))
    assert not d.exists()
    await engine._remove_local_temp_dir("")


async def test_is_dir_and_resolve_size(tmp_path: Path) -> None:
    class A:
        async def list_files(self, path):
            return [StorageObject(name="d", key="d", is_dir=True), StorageObject(name="f", key="f", size=7)]

        async def list_recursive(self, path):
            return [StorageObject(name="x", key="d/x", is_dir=False, size=3), StorageObject(name="y", key="d/y", is_dir=False, size=4)]

    a = A()
    assert await engine._is_dir_path(a, "d") is True
    assert await engine._resolve_source_size(a, "f") == 7
    assert await engine._resolve_source_size(a, "d") == 7


def test_transfer_steps_parallel_and_chain() -> None:
    targets = [{"target_id": 2, "target_path": "b"}, {"target_id": 3, "target_path": "c"}]
    data = TransferTaskCreateSchema(name="t", task_type="parallel", source_id=1, source_path="a", targets=targets)
    steps = StorageTransferService._build_steps(data)
    assert [s.target_id for s in steps] == [2, 3]
    data2 = TransferTaskCreateSchema(name="t", task_type="chain", source_id=1, source_path="a", targets=targets)
    steps2 = StorageTransferService._build_steps(data2)
    assert steps2[0].source_id == 1 and steps2[0].source_path == "a"
    assert steps2[1].source_id == 2 and steps2[1].source_path == "b"


def test_transfer_service_remove_local_temp(tmp_path: Path) -> None:
    from app.modules.task.storage.transfer.service import StorageTransferService
    f = tmp_path / "tmp.txt"
    f.write_text("x")
    StorageTransferService._remove_local_temp(SimpleNamespace(source_type="local", source_path=str(f)))
    assert not f.exists()
    StorageTransferService._remove_local_temp(SimpleNamespace(source_type="remote", source_path=str(f)))
    StorageTransferService._remove_local_temp(SimpleNamespace(source_type="local", source_path=str(f)))


async def test_run_step_success_and_missing_source(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    from app.modules.task.storage.transfer import engine
    class DB:
        async def commit(self): return None
        async def execute(self, stmt): return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: []))
    class Dst:
        def __init__(self): self.up = []
        async def upload(self, local, remote): self.up.append((local, remote))
        async def close(self): pass
    dst = Dst()
    async def config(db, sid): return object()
    monkeypatch.setattr(engine, "_build_config", config)
    monkeypatch.setattr(engine, "_broadcast", lambda *a: asyncio.sleep(0))
    monkeypatch.setattr(engine, "_load_steps", lambda db, tid: asyncio.sleep(0, result=[]))
    monkeypatch.setattr(engine.StorageAdapterFactory, "create", staticmethod(lambda cfg: dst))
    task = SimpleNamespace(id=1, transferred_size=0, speed=0, total_size=2, progress=0, status="running", error_msg=None, finished_at=None)
    step = SimpleNamespace(id=1, step_order=0, source_id=None, target_id=2, source_path=str(tmp_path / "a.txt"), target_path="r.txt", transfer_mode=None, multipart_part_size=None, multipart_concurrency=None, status="pending", progress=0, total_size=0, transferred_size=0, speed=0, error_msg=None, started_at=None, finished_at=None)
    (tmp_path / "a.txt").write_text("xx")
    assert await engine._run_step(DB(), task, step) is True
    assert step.status == "success" and dst.up[0][1] == "r.txt"
    bad = SimpleNamespace(**{**step.__dict__, "source_path": str(tmp_path / "missing.txt"), "status": "pending", "progress": 0})
    assert await engine._run_step(DB(), task, bad) is False


async def test_execute_transfer_task_no_steps_and_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    from app.modules.task.storage.transfer import engine
    from app.modules.task.storage.transfer.registry import transfer_task_registry
    class DB:
        def __init__(self, task): self.task = task; self.commits = 0
        async def get(self, model, tid): return self.task
        async def commit(self): self.commits += 1
        async def refresh(self, obj): return None
        async def refresh(self, obj): return None
    class Ctx:
        def __init__(self, db): self.db = db
        async def __aenter__(self): return self.db
        async def __aexit__(self, *a): return False
    async def load(db, tid): return []
    monkeypatch.setattr(engine, "_load_steps", load)
    task = SimpleNamespace(id=1, status="pending", is_deleted=False, source_type="local", source_path=None, source_size=0, total_size=0, started_at=None, finished_at=None, error_msg=None, progress=0)
    db = DB(task); monkeypatch.setattr(engine, "async_db_session", lambda: Ctx(db))
    await engine._execute_transfer_task(1)
    assert task.status == "failed" and db.commits == 1

    step = SimpleNamespace(status="pending", finished_at=None)
    async def load2(db, tid): return [step]
    monkeypatch.setattr(engine, "_load_steps", load2)
    async def run_step(db, task, step): return True
    monkeypatch.setattr(engine, "_run_step", run_step)
    async def broadcast(*a): return None
    monkeypatch.setattr(engine, "_broadcast", broadcast)
    task2 = SimpleNamespace(id=2, status="pending", is_deleted=False, source_type="local", source_path=str(tmp_path / "x"), source_size=0, total_size=0, started_at=None, finished_at=None, error_msg=None, progress=0)
    (tmp_path / "x").write_text("x")
    db2 = DB(task2); monkeypatch.setattr(engine, "async_db_session", lambda: Ctx(db2))
    await engine._execute_transfer_task(2)
    assert task2.status == "success" and task2.progress == 100


async def test_execute_transfer_task_canceled_and_deleted(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    from app.modules.task.storage.transfer import engine
    from app.modules.task.storage.transfer.registry import transfer_task_registry
    class DB:
        def __init__(self, task): self.task = task; self.commits = 0
        async def get(self, model, tid): return self.task
        async def commit(self): self.commits += 1
        async def refresh(self, obj): return None
    class Ctx:
        def __init__(self, db): self.db = db
        async def __aenter__(self): return self.db
        async def __aexit__(self, *a): return False
    async def broadcast(*a): return None
    monkeypatch.setattr(engine, "_broadcast", broadcast)
    step = SimpleNamespace(status="pending", finished_at=None)
    async def load(db, tid): return [step]
    monkeypatch.setattr(engine, "_load_steps", load)
    task = SimpleNamespace(id=1, status="pending", is_deleted=False, source_type="remote", source_id=None, source_path=None, started_at=None, finished_at=None, error_msg=None, progress=0, total_size=0, transferred_size=0, speed=0, source_size=0)
    transfer_task_registry.mark_cancel(1)
    db = DB(task); monkeypatch.setattr(engine, "async_db_session", lambda: Ctx(db))
    await engine._execute_transfer_task(1)
    assert task.status == "canceled" and step.status == "canceled"
    deleted = SimpleNamespace(id=2, status="pending", is_deleted=True, source_type="remote", source_id=None, source_path=None, source_size=0)
    transfer_task_registry.clear(2)
    db2 = DB(deleted); monkeypatch.setattr(engine, "async_db_session", lambda: Ctx(db2))
    await engine._execute_transfer_task(2)
    assert deleted.status == "running"


async def test_execute_transfer_task_missing_source(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    from app.modules.task.storage.transfer import engine
    class DB:
        def __init__(self, task): self.task=task; self.commits=0
        async def get(self,model,tid): return self.task
        async def commit(self): self.commits+=1
        async def refresh(self,obj): return None
    class Ctx:
        def __init__(self,db): self.db=db
        async def __aenter__(self): return self.db
        async def __aexit__(self,*a): return False
    async def load(db,tid): return [SimpleNamespace(status="pending",finished_at=None)]
    monkeypatch.setattr(engine,"_load_steps",load)
    async def config(db,sid): return None
    monkeypatch.setattr(engine,"_build_config",config)
    async def broadcast(*a): return None
    monkeypatch.setattr(engine,"_broadcast",broadcast)
    task=SimpleNamespace(id=1,status="pending",is_deleted=False,source_type="remote",source_id=9,source_path="x",source_size=0,total_size=0,started_at=None,finished_at=None,error_msg=None,progress=0,transferred_size=0,speed=0)
    db=DB(task); monkeypatch.setattr(engine,"async_db_session",lambda:Ctx(db))
    await engine._execute_transfer_task(1)
    assert task.status=="failed" and "不存在或已停用" in task.error_msg


async def test_local_file_helpers(tmp_path: Path) -> None:
    from app.modules.task.storage.transfer import engine
    f=tmp_path/"a.txt"; f.write_text("123")
    assert engine._local_path_size(str(f))==3
    assert engine._local_path_size(str(tmp_path/"none"))==0
    assert engine._local_path_size(str(tmp_path))>=0
    files=engine._list_local_files(str(tmp_path))
    assert files and files[0][1]=="a.txt"
    out=tmp_path/"sub"/"b.txt"
    engine._prepare_local_dirs([str(out)])
    assert out.parent.exists()
    d=tmp_path/"rm"; d.mkdir(); (d/"x").write_text("x")
    await engine._remove_local_temp_dir(str(d))
    assert not d.exists()


async def test_resolve_source_and_dir(tmp_path: Path) -> None:
    from app.modules.task.storage.core.base import StorageObject
    from app.modules.task.storage.transfer import engine
    class A:
        def __init__(self): self.downloaded=[]
        async def list_files(self,p):
            if p=="bad": raise RuntimeError()
            if p=="f": return [StorageObject(name="f",key="f",is_dir=False,size=5)]
            return [StorageObject(name="d",key="d",is_dir=True)]
        async def list_recursive(self,p): return [StorageObject(name="a",key="d/a",is_dir=False,size=3),StorageObject(name="sub",key="d/sub",is_dir=True)] if p=="d" else []
        async def download(self,k,l): self.downloaded.append((k,l))
    a=A()
    assert await engine._resolve_source_size(a,"d")==3
    assert await engine._resolve_source_size(a,"f")==5
    assert await engine._resolve_source_size(a,"bad")==0
    assert await engine._is_dir_path(a,"d") is True
    assert await engine._is_dir_path(a,"f") is False
    await engine._download_dir(a,"d",str(tmp_path))
    assert a.downloaded and a.downloaded[0][0]=="d/a"


async def test_remove_local_temp_and_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    from app.modules.task.storage.transfer import engine
    f=tmp_path/"a"; f.write_text("x")
    engine._remove_local_temp(SimpleNamespace(source_type="local",source_path=str(f)))
    assert not f.exists()
    d=tmp_path/"d"; d.mkdir()
    engine._remove_local_temp(SimpleNamespace(source_type="local",source_path=str(d)))
    assert d.exists()
    class DB:
        def __init__(self,obj): self.obj=obj
        async def get(self,model,id): return self.obj
    assert await engine._build_config(DB(None),1) is None
    assert await engine._build_config(DB(SimpleNamespace(status=1)),1) is None
    obj=SimpleNamespace(status=0)
    monkeypatch.setattr(engine.StorageNodeService,"_build_config",staticmethod(lambda s:"cfg"))
    assert await engine._build_config(DB(obj),1)=="cfg"


async def test_broadcast_and_empty_temp(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    from app.modules.task.storage.transfer import engine
    sent=[]
    async def send(uid,data): sent.append(uid)
    monkeypatch.setattr(engine.transfer_stream_manager,"send_to_user",send)
    monkeypatch.setattr(engine,"_task_payload",lambda t,s: {})
    await engine._broadcast(SimpleNamespace(created_id=1,id=1),[])
    assert sent==[1]
    async def bad(uid,data): raise RuntimeError()
    monkeypatch.setattr(engine.transfer_stream_manager,"send_to_user",bad)
    await engine._broadcast(SimpleNamespace(created_id=1,id=1),[])
    await engine._remove_local_temp_dir("")
