import json
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from typing import Any

from app.core.ap_scheduler import SchedulerUtil
from app.core.logger import logger


def _parse_args(args_str: str | None) -> list[Any]:
    if not args_str or not str(args_str).strip():
        return []
    return [a.strip() for a in str(args_str).split(",") if a.strip()]


def _parse_kwargs(kwargs_str: str | None) -> dict[str, Any]:
    if not kwargs_str or not str(kwargs_str).strip():
        return {}
    try:
        return json.loads(kwargs_str)
    except json.JSONDecodeError:
        return {}


def validate_workflow_graph(nodes: list[dict], edges: list[dict]) -> None:
    if not nodes:
        raise ValueError("工作流至少需要一个节点")
    ids = {n["id"] for n in nodes}
    for e in edges:
        if e.get("source") not in ids or e.get("target") not in ids:
            raise ValueError("连线引用了不存在的节点")
    in_degree: dict[str, int] = dict.fromkeys(ids, 0)
    adj: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        adj[e["source"]].append(e["target"])
        in_degree[e["target"]] += 1
    q: deque[str] = deque([nid for nid in ids if in_degree[nid] == 0])
    visited = 0
    while q:
        u = q.popleft()
        visited += 1
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)
    if visited != len(ids):
        raise ValueError("工作流图存在环路，无法执行")


def _topological_levels(nodes: list[dict], edges: list[dict]) -> list[list[dict]]:
    id_to_node = {n["id"]: n for n in nodes}
    in_degree: dict[str, int] = {n["id"]: 0 for n in nodes}
    adj: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        adj[e["source"]].append(e["target"])
        in_degree[e["target"]] += 1
    levels: list[list[dict]] = []
    current = [nid for nid in in_degree if in_degree[nid] == 0]
    while current:
        levels.append([id_to_node[nid] for nid in current])
        next_level: list[str] = []
        for nid in current:
            for target in adj[nid]:
                in_degree[target] -= 1
                if in_degree[target] == 0:
                    next_level.append(target)
        current = next_level
    return levels


def _execute_node(
    vue_node_id: str,
    node_type_code: str,
    code_block: str,
    args_str: str | None,
    kwargs_str: str | None,
    upstream: dict[str, Any],
    flow_variables: dict[str, Any],
) -> Any:
    job_id = f"wfnode-{vue_node_id}"
    args = _parse_args(args_str)
    kw = _parse_kwargs(kwargs_str)
    kw.setdefault("upstream", upstream)
    kw.setdefault("variables", flow_variables)
    return SchedulerUtil._task_wrapper(job_id, code_block, *args, **kw)


def run_workflow_sync(
    nodes: list[dict],
    edges: list[dict],
    node_templates: dict[str, dict[str, Any]],
    flow_variables: dict[str, Any],
) -> dict[str, Any]:
    """同步执行工作流：按拓扑层级分组，同层节点并行执行。"""
    validate_workflow_graph(nodes, edges)
    levels = _topological_levels(nodes, edges)
    results: dict[str, Any] = {}
    for level in levels:
        with ThreadPoolExecutor(max_workers=len(level)) as executor:
            futures: dict[str, Any] = {}
            for node in level:
                nid = node["id"]
                ntype = node.get("type") or ""
                tpl = node_templates.get(ntype)
                if not tpl or not tpl.get("func"):
                    raise ValueError(f"未知或未配置节点类型: {ntype}")
                data = node.get("data") or {}
                args_str = data.get("args") if data.get("args") is not None else tpl.get("args")
                kwargs_str = data.get("kwargs") if data.get("kwargs") is not None else tpl.get("kwargs")
                upstream: dict[str, Any] = {}
                for e in edges:
                    if e.get("target") == nid and e.get("source") in results:
                        upstream[e["source"]] = results[e["source"]]
                futures[nid] = executor.submit(
                    _execute_node,
                    nid,
                    ntype,
                    tpl["func"],
                    args_str,
                    kwargs_str,
                    upstream,
                    flow_variables,
                )
            for nid, fut in futures.items():
                results[nid] = fut.result()
    logger.info("工作流执行完成: nodes={}", list(results.keys()))
    return {"node_results": results, "status": "completed"}


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()
