"""工作流画布拆分/源目标派生测试（纯函数）。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.task.storage.workflow.service import WorkflowService


def _graph() -> dict:
    return {
        "nodes": [
            {"id": "n1", "type": "storage", "position": {"x": 1, "y": 2}, "data": {"source_id": 1, "source_path": "a"}},
            {"id": "n2", "position": {"x": 3, "y": 4}, "data": {"source_id": 2, "source_path": "b"}},
            {"id": "n3", "data": {}},
        ],
        "edges": [
            {"id": "e1", "source": "n1", "target": "n2", "data": {"enabled": True, "transfer_mode": "stream"}},
            {"id": "e2", "source": "n1", "target": "n2", "data": {}},
            {"id": "e3", "source": "n1", "target": "missing"},
        ],
    }


def test_split_graph_valid_and_dedup() -> None:
    result = WorkflowService._split_graph(_graph())
    assert [n.node_key for n in result.nodes] == ["n1", "n2"]
    assert result.sources[0].source_id == 1
    assert result.targets[0].target_id == 2 and result.targets[0].target_path == "b"
    assert len(result.edges) == 1 and result.edges[0].enabled is True
    assert len(result.layout["nodes"]) == 3 and len(result.layout["edges"]) == 1


def test_split_graph_invalid_edges() -> None:
    with pytest.raises(CustomException):
        WorkflowService._split_graph({"nodes": [], "edges": []})
    with pytest.raises(CustomException):
        WorkflowService._split_graph({"nodes": [], "edges": [{"id": "e", "source": "a", "target": "b"}]})


def test_split_graph_same_source_target() -> None:
    graph = {
        "nodes": [
            {"id": "a", "data": {"source_id": 1}},
            {"id": "b", "data": {"source_id": 1}},
        ],
        "edges": [{"id": "e", "source": "a", "target": "b"}],
    }
    with pytest.raises(CustomException, match="源与目标不能相同"):
        WorkflowService._split_graph(graph)


def test_sources_and_targets_from_edges() -> None:
    rows = [
        SimpleNamespace(source_node_key="a", target_node_key="b"),
        SimpleNamespace(source_node_key="missing", target_node_key="c"),
    ]
    node_map = {
        "a": SimpleNamespace(source_id=1, source_path="a"),
        "b": SimpleNamespace(source_id=2, source_path="b"),
        "c": SimpleNamespace(source_id=3, source_path=None),
    }
    sources = WorkflowService._sources_from(rows, node_map)
    targets = WorkflowService._targets_from(rows, node_map)
    assert [s.source_id for s in sources] == [1]
    assert [(t.target_id, t.target_path) for t in targets] == [(2, "b"), (3, "")]
