"""工作流明细保存/画布组装覆盖。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.modules.task.storage.workflow.schema import WorkflowEdgeSchema, WorkflowNodeSchema
from app.modules.task.storage.workflow.service import WorkflowService


class DB:
    def __init__(self): self.added = []; self.flushed = False
    def add(self, obj): self.added.append(obj)
    async def flush(self): self.flushed = True


def _svc(db=None):
    s = WorkflowService.__new__(WorkflowService)
    s.auth = SimpleNamespace(user=SimpleNamespace(id=1))
    s.db = db or DB()
    return s


async def test_save_graph_rebuilds_details(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []
    class NodeCRUD:
        def __init__(self, *a): pass
        async def hard_delete_by_flow_ids(self, ids): calls.append(("nodes", ids))
    class EdgeCRUD:
        def __init__(self, *a): pass
        async def hard_delete_by_flow_ids(self, ids): calls.append(("edges", ids))
    monkeypatch.setattr("app.modules.task.storage.workflow.service.WorkflowNodeCRUD", NodeCRUD)
    monkeypatch.setattr("app.modules.task.storage.workflow.service.WorkflowEdgeCRUD", EdgeCRUD)
    db = DB(); s = _svc(db)
    node = WorkflowNodeSchema(node_key="n1", source_id=1, source_path="p")
    edge = WorkflowEdgeSchema(edge_key="e1", source_node_key="n1", target_node_key="n1")
    await s._save_graph(9, [node], [edge])
    assert calls == [("nodes", [9]), ("edges", [9])]
    assert len(db.added) == 2 and db.flushed is True


async def test_build_graph_from_layout_and_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    class SourceCRUD:
        def __init__(self, *a): pass
        async def get_list(self, search=None):
            return [SimpleNamespace(id=1, name="minio", protocol="s3", host=None, bucket="b", endpoint="http://e", region="r", path_prefix=None)]
    monkeypatch.setattr("app.modules.task.storage.workflow.service.StorageNodeCRUD", SourceCRUD)
    flow = SimpleNamespace(graph={"nodes": [{"id": "n1", "position": {"x": 0, "y": 0}}], "edges": [{"id": "e1"}]})
    node = SimpleNamespace(node_key="n1", source_id=1, source_path="p")
    edge = SimpleNamespace(edge_key="e1", source_node_key="n1", target_node_key="n1", enabled=True, transfer_mode="stream", multipart_part_size=50, multipart_concurrency=2)
    graph = await _svc()._build_graph(flow, [node], [edge])
    assert graph["nodes"][0]["data"]["label"] == "minio"
    assert graph["nodes"][0]["data"]["protocol"] == "s3"
    assert graph["edges"][0]["data"]["source_label"] == "minio"
    assert graph["edges"][0]["data"]["enabled"] is True


async def test_workflow_execute_builds_tasks(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    s = _svc()
    async def get_obj(id, msg=None): return SimpleNamespace(name="flow")
    s._crud = lambda: SimpleNamespace(get_or_404=get_obj)
    nodes = [SimpleNamespace(node_key="a", source_id=1, source_path="src"), SimpleNamespace(node_key="b", source_id=2, source_path="dst")]
    edges = [SimpleNamespace(edge_key="e", source_node_key="a", target_node_key="b", enabled=True, transfer_mode=None, multipart_part_size=None, multipart_concurrency=None)]
    async def load(id): return nodes, edges
    s._load_flow_graph = load
    class NodeSvc:
        def __init__(self, *a): pass
        async def get_active_sources(self, ids): return [SimpleNamespace(id=1, name="src"), SimpleNamespace(id=2, name="dst")]
    created = []
    class TransferSvc:
        def __init__(self, *a): pass
        async def create(self, data): created.append(data); return 7
    monkeypatch.setattr("app.modules.task.storage.workflow.service.StorageNodeService", NodeSvc)
    monkeypatch.setattr("app.modules.task.storage.workflow.service.StorageTransferService", TransferSvc)
    assert await s.execute(1) == [7]
    assert created[0].name == "flow-src→dst" and created[0].targets[0].target_path == "dst"


async def test_workflow_execute_rejects_disabled_or_bad_path(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    s = _svc()
    async def get_obj(id, msg=None): return SimpleNamespace(name="flow")
    s._crud = lambda: SimpleNamespace(get_or_404=get_obj)
    nodes = [SimpleNamespace(node_key="a", source_id=1, source_path=""), SimpleNamespace(node_key="b", source_id=2, source_path="")]
    async def load(id): return nodes, []
    s._load_flow_graph = load
    with pytest.raises(Exception, match="没有启用"):
        await s.execute(1)
    async def load2(id): return nodes, [SimpleNamespace(edge_key="e", source_node_key="a", target_node_key="b", enabled=True, transfer_mode=None, multipart_part_size=None, multipart_concurrency=None)]
    s._load_flow_graph = load2
    with pytest.raises(Exception, match="未选择源文件"):
        await s.execute(1)


async def test_workflow_create_update_delete_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    from app.modules.task.storage.workflow.schema import WorkflowCreateSchema, WorkflowUpdateSchema
    s = _svc()
    obj = SimpleNamespace(id=1, name="f", graph={})
    class Crud:
        def __init__(self): self.updated = []; self.deleted = []; self.created = None
        async def get(self, name): return None
        async def create(self, data): self.created = data; return obj
        async def get_or_404(self, id, msg=None): return obj
        async def update(self, id, data): self.updated.append((id, data))
        async def delete(self, ids): self.deleted.append(ids)
    crud = Crud(); s._crud = lambda: crud
    class ChildCRUD:
        def __init__(self, *a): pass
        async def hard_delete_by_flow_ids(self, ids): return None
    monkeypatch.setattr("app.modules.task.storage.workflow.service.WorkflowNodeCRUD", ChildCRUD)
    monkeypatch.setattr("app.modules.task.storage.workflow.service.WorkflowEdgeCRUD", ChildCRUD)
    async def prep(flow_id, data): return ({"name": "f"}, [], [])
    s._prepare_and_save = prep
    async def save(*a): return None
    s._save_graph = save
    async def to_out(o): return o
    s._to_out = to_out
    data = WorkflowCreateSchema(name="f", graph={"nodes": [{"id": "a", "data": {"source_id": 1}}], "edges": [{"id": "e", "source": "a", "target": "a"}]})
    assert await s.create(data) is obj and crud.created["name"] == "f"
    assert await s.update(1, WorkflowUpdateSchema(name="f", graph=data.graph)) is obj
    with pytest.raises(Exception, match="删除对象不能为空"):
        await s.delete([])
    await s.delete([1])
    assert crud.deleted == [[1]]


async def test_workflow_page_and_get_list(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    s = _svc()
    class Crud:
        async def page(self, **kw): return SimpleNamespace(items=[1], page_no=1, page_size=10, total=1, has_next=False)
        async def get_list(self, **kw): return [1]
    s._crud = lambda: Crud()
    async def to_list(objs): return [SimpleNamespace(id=o) for o in objs]
    s._to_out_list = to_list
    page = await s.page(None, 1, 10)
    assert page.total == 1 and page.items[0].id == 1
    got = await s.get_list(None)
    assert got[0].id == 1
