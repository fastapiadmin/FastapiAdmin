"""定时任务节点服务基础分支。"""

from __future__ import annotations

import pytest
from types import SimpleNamespace

import app.modules.task.cronjob.node.service as mod
from app.core.exceptions import CustomException
from app.modules.task.cronjob.node.schema import NodeCreateSchema
from app.modules.task.cronjob.node.service import NodeService


def _svc(crud):
    monkeypatch = pytest.MonkeyPatch(); monkeypatch.setattr(mod, "NodeCRUD", lambda *a: crud)
    s = NodeService.__new__(NodeService); s.auth = object(); s.db = object()
    return s, monkeypatch


async def test_options_and_detail_missing() -> None:
    class C:
        async def get_obj_list_crud(self): return []
        async def get_obj_by_id_crud(self, **kw): return None
    s, m = _svc(C())
    try:
        assert await s.options() == []
        with pytest.raises(CustomException, match="不存在"):
            await s.detail(1)
    finally:
        m.undo()


async def test_create_duplicate_and_invalid_trigger() -> None:
    class C:
        async def get(self, **kw): return SimpleNamespace(id=1)
    s, m = _svc(C())
    try:
        with pytest.raises(CustomException, match="已存在"):
            await s.create(NodeCreateSchema(name="n", func="builtin:x"))
    finally:
        m.undo()
    class C2:
        async def get(self, **kw): return None
    s, m = _svc(C2())
    try:
        with pytest.raises(Exception):
            data = NodeCreateSchema(name="n", func="builtin:x", trigger="cron", trigger_args="bad")
            await s.create(data)
    finally:
        m.undo()


async def test_batch_set_status_empty() -> None:
    class C: ...
    s, m = _svc(C())
    try:
        with pytest.raises(CustomException, match="请选择"):
            await s.batch_set_status([], 0)
    finally:
        m.undo()


async def test_node_update_delete_execute(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.task.cronjob.node.schema import NodeUpdateSchema
    class C:
        def __init__(self,obj=None): self.obj=obj; self.deleted=None; self.cleared=False
        async def get_obj_by_id_crud(self,**kw): return self.obj
        async def update_obj_crud(self,**kw): return self.obj
        async def delete_obj_crud(self,ids): self.deleted=ids
        async def clear_obj_crud(self): self.cleared=True
    c=C(None); monkeypatch.setattr(mod,"NodeCRUD",lambda *a:c)
    s=NodeService.__new__(NodeService); s.auth=object(); s.db=object()
    with pytest.raises(CustomException, match="更新失败"):
        await s.update(1,NodeUpdateSchema(name="n",func="builtin:x"))
    with pytest.raises(CustomException, match="删除失败"):
        await s.delete([1])
    with pytest.raises(CustomException, match="执行失败"):
        await s.execute(1)
    async def noop(*a,**k): return None
    monkeypatch.setattr(mod,"unregister_node_job",noop)
    monkeypatch.setattr(mod,"SchedulerUtil",SimpleNamespace(clear_jobs=lambda:None))
    await s.clear(); assert c.cleared
    obj=SimpleNamespace(id=1,name="n",func="builtin:x",status=0)
    c.obj=obj
    async def ok(*a,**k): return None
    monkeypatch.setattr(mod,"register_node_job",ok)
    async def enrich(items): return None
    s._enrich_runtime=enrich
    out=await s.update(1,NodeUpdateSchema(name="n",func="builtin:x"))
    assert out.id==1
    monkeypatch.setattr(mod,"run_node_once",lambda **kw:"tmp")
    assert (await s.execute(1)).job_id=="tmp"
