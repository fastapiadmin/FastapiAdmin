"""传输服务取消/删除分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.modules.task.storage.transfer.service import StorageTransferService


class Crud:
    def __init__(self, task=None): self.task = task; self.updated = []; self.deleted = []
    async def get_or_404(self, id): return self.task
    async def update(self, id, data): self.updated.append((id, data))
    async def delete(self, ids): self.deleted.append(ids)


class DB:
    def __init__(self, tasks=None): self.tasks = tasks or []; self.execute_calls = 0
    async def execute(self, stmt):
        self.execute_calls += 1
        return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: self.tasks))


def _svc(crud, db):
    s = StorageTransferService.__new__(StorageTransferService)
    s.auth = SimpleNamespace(user=SimpleNamespace(id=1))
    s.db = db
    s._crud = lambda: crud
    return s


async def test_cancel_pending_and_running(monkeypatch: pytest.MonkeyPatch) -> None:
    task = SimpleNamespace(id=1, status="pending", source_type="remote", source_path=None)
    crud = Crud(task); svc = _svc(crud, DB())
    pushed = []
    async def push(t): pushed.append(t.id)
    svc._push_task = push
    await svc.cancel(1)
    assert crud.updated[0][0] == 1 and pushed == [1]

    task2 = SimpleNamespace(id=2, status="running", source_type="remote", source_path=None)
    svc2 = _svc(Crud(task2), DB())
    from app.modules.task.storage.transfer.registry import transfer_task_registry
    marked = []
    monkeypatch.setattr(transfer_task_registry, "mark_cancel", lambda i: marked.append(i))
    await svc2.cancel(2)
    assert marked == [2]


async def test_delete_marks_cancel_and_removes_temp(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    f = tmp_path / "t.txt"; f.write_text("x")
    task = SimpleNamespace(id=3, source_type="local", source_path=str(f))
    crud = Crud(); svc = _svc(crud, DB([task]))
    from app.modules.task.storage.transfer.registry import transfer_task_registry
    marked = []
    monkeypatch.setattr(transfer_task_registry, "mark_cancel", lambda i: marked.append(i))
    await svc.delete([3])
    assert marked == [3] and crud.deleted == [[3]] and not f.exists()
