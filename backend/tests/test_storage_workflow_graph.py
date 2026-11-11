"""存储工作流源/目标派生。"""

from __future__ import annotations

from types import SimpleNamespace

from app.modules.task.storage.workflow.service import WorkflowService


def test_sources_and_targets() -> None:
    nodes={"s1":SimpleNamespace(source_id=1),"s2":SimpleNamespace(source_id=1),"t1":SimpleNamespace(source_id=2,source_path="/a"),"t2":SimpleNamespace(source_id=2,source_path="/b")}
    edges=[SimpleNamespace(source_node_key="s1",target_node_key="t1"),SimpleNamespace(source_node_key="s2",target_node_key="t2"),SimpleNamespace(source_node_key="x",target_node_key="y")]
    assert [x.source_id for x in WorkflowService._sources_from(edges,nodes)]==[1]
    targets=WorkflowService._targets_from(edges,nodes)
    assert len(targets)==1 and targets[0].target_id==2 and targets[0].target_path=="/a"


def test_sources_targets_empty() -> None:
    assert WorkflowService._sources_from([],{})==[]
    assert WorkflowService._targets_from([],{})==[]


def test_split_empty_edges() -> None:
    from app.core.exceptions import CustomException
    import pytest
    with pytest.raises(CustomException, match="连线"):
        WorkflowService._split_graph({})


def test_split_graph_valid_duplicate_self() -> None:
    from app.core.exceptions import CustomException
    import pytest
    nodes=[{"id":"s","data":{"source_id":1,"source_path":"/a"}},{"id":"t","data":{"source_id":2,"source_path":"/b"}}]
    edges=[{"id":"e1","source":"s","target":"t"},{"id":"e2","source":"s","target":"t"}]
    out=WorkflowService._split_graph({"nodes":nodes,"edges":edges})
    assert [x.source_id for x in out.sources]==[1] and [x.target_id for x in out.targets]==[2]
    with pytest.raises(CustomException, match="不能相同"):
        WorkflowService._split_graph({"nodes":nodes,"edges":[{"id":"e","source":"s","target":"s"}]})
    with pytest.raises(CustomException, match="连线"):
        WorkflowService._split_graph({"nodes":nodes,"edges":[{"id":"e","source":"x","target":"y"}]})


async def test_validate_nodes(monkeypatch) -> None:
    import app.modules.task.storage.workflow.service as mod
    from app.modules.task.storage.workflow.schema import WorkflowSourceSchema, WorkflowTargetSchema
    calls=[]
    class N:
        def __init__(self,*a): pass
        async def get_active_sources(self,ids): calls.append(ids)
    monkeypatch.setattr(mod,"StorageNodeService",N)
    s=WorkflowService.__new__(WorkflowService); s.auth=object(); s.db=object()
    await s._validate_nodes([],[])
    assert calls==[]
    await s._validate_nodes([WorkflowSourceSchema(source_id=1)],[WorkflowTargetSchema(target_id=2,target_path="/a")])
    assert calls==[[1,2]]


async def test_workflow_delete(monkeypatch) -> None:
    import pytest
    from app.core.exceptions import CustomException
    import app.modules.task.storage.workflow.service as mod
    calls=[]
    class C:
        def __init__(self,*a): pass
        async def delete(self,ids): calls.append(("flow",ids))
        async def hard_delete_by_flow_ids(self,ids): calls.append(("child",ids))
    monkeypatch.setattr(mod,"WorkflowNodeCRUD",C); monkeypatch.setattr(mod,"WorkflowEdgeCRUD",C)
    s=WorkflowService.__new__(WorkflowService); s.auth=object(); s.db=object()
    s._crud=lambda: C()
    with pytest.raises(CustomException, match="不能为空"):
        await s.delete([])
    await s.delete([1])
    assert len(calls)==3


async def test_workflow_queries(monkeypatch) -> None:
    import pytest
    from app.core.exceptions import CustomException
    class C:
        def __init__(self,*a): pass
        async def get_list(self,**kw): return []
        async def get_or_404(self,**kw): raise CustomException(msg="不存在")
    s=WorkflowService.__new__(WorkflowService); s.auth=object(); s.db=object()
    s._crud=lambda: C()
    async def enrich(objs): return []
    s._to_out_list=enrich
    assert await s.get_list()==[]
    with pytest.raises(CustomException, match="不存在"):
        await s.detail(1)


async def test_load_flow_graph() -> None:
    class R:
        def __init__(self,v): self.v=v
        def scalars(self): return self
        def all(self): return self.v
    class DB:
        def __init__(self): self.n=0
        async def execute(self,stmt):
            self.n+=1; return R(["n"] if self.n==1 else ["e"])
    s=WorkflowService.__new__(WorkflowService); s.auth=object(); s.db=DB()
    nodes,edges=await s._load_flow_graph(1)
    assert nodes==["n"] and edges==["e"]
