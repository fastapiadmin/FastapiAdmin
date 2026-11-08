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
