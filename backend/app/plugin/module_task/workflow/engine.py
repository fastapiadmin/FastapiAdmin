import asyncio
import json
from collections import defaultdict
from collections.abc import Callable
from datetime import datetime
from typing import Any

from sqlalchemy import select

from app.core.database import async_db_session
from app.core.logger import log
from app.plugin.module_task.node.model import NodeModel
from app.plugin.module_task.workflow.model import WorkflowModel


class WorkflowRunLogModel:
    pass


class NodeExecutionContext:
    def __init__(
        self,
        node_id: str,
        node_type: str,
        args: str | None = None,
        kwargs: str | None = None,
        variables: dict | None = None,
        input_data: Any = None,
    ):
        self.node_id = node_id
        self.node_type = node_type
        self.args = args
        self.kwargs = kwargs
        self.variables = variables or {}
        self.input_data = input_data
        self.output_data: Any = None
        self.status: str = "pending"
        self.error: str | None = None
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None


class WorkflowExecutionContext:
    def __init__(
        self,
        workflow_id: int,
        workflow_name: str,
        variables: dict | None = None,
        business_key: str | None = None,
    ):
        self.workflow_id = workflow_id
        self.workflow_name = workflow_name
        self.variables = variables or {}
        self.business_key = business_key
        self.node_contexts: dict[str, NodeExecutionContext] = {}
        self.status: str = "pending"
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None
        self.current_node: str | None = None


class WorkflowEngine:
    """
    工作流执行引擎

    功能：
    1. 解析工作流节点和边，构建执行图
    2. 按拓扑顺序执行节点
    3. 支持条件分支和并行执行
    4. 记录执行日志
    """

    _node_handlers: dict[str, Callable] = {}

    @classmethod
    def register_handler(cls, node_type: str, handler: Callable) -> None:
        """
        注册节点处理器

        参数:
        - node_type: 节点类型编码
        - handler: 处理函数，签名为 async (context: NodeExecutionContext) -> Any
        """
        cls._node_handlers[node_type] = handler

    @classmethod
    async def execute(cls, workflow: WorkflowModel, variables: dict | None = None, business_key: str | None = None) -> WorkflowExecutionContext:
        """
        执行工作流

        参数:
        - workflow: 工作流模型实例
        - variables: 流程变量
        - business_key: 业务键

        返回:
        - WorkflowExecutionContext: 执行上下文
        """
        context = WorkflowExecutionContext(
            workflow_id=workflow.id,
            workflow_name=workflow.name,
            variables=variables or {},
            business_key=business_key,
        )

        context.start_time = datetime.now()
        context.status = "running"

        try:
            nodes = workflow.nodes if isinstance(workflow.nodes, list) else []
            edges = workflow.edges if isinstance(workflow.edges, list) else []

            if not nodes:
                context.status = "completed"
                context.end_time = datetime.now()
                return context

            node_map = {n.get("id"): n for n in nodes}
            execution_order = cls._build_execution_order(nodes, edges)

            node_type_map = await cls._load_node_types([n.get("type") for n in nodes if n.get("type")])

            for node_id in execution_order:
                node_data = node_map.get(node_id)
                if not node_data:
                    continue

                node_type_code = node_data.get("type")
                node_args = node_data.get("data", {}).get("args", "")
                node_kwargs = node_data.get("data", {}).get("kwargs", "{}")

                input_data = cls._collect_input_data(node_id, edges, context)

                node_context = NodeExecutionContext(
                    node_id=node_id,
                    node_type=node_type_code,
                    args=node_args,
                    kwargs=node_kwargs,
                    variables=context.variables,
                    input_data=input_data,
                )
                context.node_contexts[node_id] = node_context
                context.current_node = node_id

                node_type_info = node_type_map.get(node_type_code)
                await cls._execute_node(node_context, node_type_info)

                if node_context.status == "failed":
                    context.status = "failed"
                    context.end_time = datetime.now()
                    return context

                if node_context.output_data:
                    context.variables[node_id] = node_context.output_data

            context.status = "completed"
        except Exception as e:
            log.error(f"工作流 {workflow.id} 执行失败: {e!s}")
            context.status = "failed"
        finally:
            context.end_time = datetime.now()
            context.current_node = None

        return context

    @classmethod
    def _build_execution_order(cls, nodes: list, edges: list) -> list[str]:
        """
        构建节点执行顺序（拓扑排序）

        参数:
        - nodes: 节点列表
        - edges: 边列表

        返回:
        - list[str]: 节点ID执行顺序
        """
        in_degree = defaultdict(int)
        adjacency = defaultdict(list)
        node_ids = {n.get("id") for n in nodes}

        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            if source in node_ids and target in node_ids:
                adjacency[source].append(target)
                in_degree[target] += 1

        queue = [nid for nid in node_ids if in_degree[nid] == 0]
        result = []

        while queue:
            node_id = queue.pop(0)
            result.append(node_id)

            for neighbor in adjacency[node_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        for nid in node_ids:
            if nid not in result:
                result.append(nid)

        return result

    @classmethod
    async def _load_node_types(cls, type_codes: list[str]) -> dict[str, NodeModel]:
        """
        加载节点类型定义

        参数:
        - type_codes: 节点类型编码列表

        返回:
        - dict[str, NodeModel]: 节点类型映射
        """
        if not type_codes:
            return {}

        async with async_db_session() as session:
            result = await session.execute(select(NodeModel).where(NodeModel.code.in_(type_codes)))
            node_types = result.scalars().all()
            return {nt.code: nt for nt in node_types}

    @classmethod
    def _collect_input_data(cls, node_id: str, edges: list, context: WorkflowExecutionContext) -> dict:
        """
        收集节点输入数据（从上游节点的输出）

        参数:
        - node_id: 当前节点ID
        - edges: 边列表
        - context: 执行上下文

        返回:
        - dict: 输入数据
        """
        input_data = {}
        for edge in edges:
            if edge.get("target") == node_id:
                source_id = edge.get("source")
                source_context = context.node_contexts.get(source_id)
                if source_context and source_context.output_data:
                    edge_label = edge.get("label", "default")
                    input_data[edge_label] = source_context.output_data
        return input_data

    @classmethod
    async def _execute_node(cls, context: NodeExecutionContext, node_type_info: NodeModel | None) -> None:
        """
        执行单个节点

        参数:
        - context: 节点执行上下文
        - node_type_info: 节点类型定义
        """
        context.start_time = datetime.now()
        context.status = "running"

        try:
            handler = cls._node_handlers.get(context.node_type)

            if handler:
                context.output_data = await handler(context)
            elif node_type_info and node_type_info.func:
                context.output_data = await cls._execute_code_block(
                    node_type_info.func,
                    node_type_info.args,
                    node_type_info.kwargs,
                    context,
                )
            else:
                log.warning(f"节点 {context.node_id} 没有注册处理器或代码块，跳过执行")
                context.output_data = None

            context.status = "completed"
        except Exception as e:
            log.error(f"节点 {context.node_id} 执行失败: {e!s}")
            context.status = "failed"
            context.error = str(e)
        finally:
            context.end_time = datetime.now()

    @classmethod
    async def _execute_code_block(
        cls,
        code_block: str,
        args: str | None,
        kwargs: str | None,
        context: NodeExecutionContext,
    ) -> Any:
        """
        执行代码块

        参数:
        - code_block: 代码块
        - args: 位置参数
        - kwargs: 关键字参数
        - context: 节点执行上下文

        返回:
        - Any: 执行结果
        """
        if not code_block or not code_block.strip():
            return None

        local_vars = {
            "context": context,
            "variables": context.variables,
            "input_data": context.input_data,
        }

        exec(code_block, {"__builtins__": __builtins__}, local_vars)

        handler = local_vars.get("handler")
        if handler and callable(handler):
            job_args = []
            if args:
                args_str = str(args).strip()
                if args_str:
                    job_args = [arg.strip() for arg in args_str.split(",") if arg.strip()]

            job_kwargs = {}
            if kwargs:
                kwargs_str = str(kwargs).strip()
                if kwargs_str:
                    try:
                        job_kwargs = json.loads(kwargs_str)
                    except json.JSONDecodeError:
                        pass

            result = handler(*job_args, **job_kwargs)
            if asyncio.iscoroutine(result):
                return await result
            return result

        return local_vars.get("result")


def register_builtin_handlers():
    """
    注册内置节点处理器
    """

    async def input_handler(context: NodeExecutionContext) -> Any:
        return context.variables

    async def output_handler(context: NodeExecutionContext) -> Any:
        return context.input_data

    async def condition_handler(context: NodeExecutionContext) -> Any:
        try:
            kwargs_str = str(context.kwargs or "{}").strip()
            kwargs_data = json.loads(kwargs_str) if kwargs_str else {}
            condition_expr = kwargs_data.get("condition", "True")
            result = eval(condition_expr, {"__builtins__": __builtins__}, context.variables)
            return {"condition_result": bool(result)}
        except Exception as e:
            log.error(f"条件表达式执行失败: {e!s}")
            return {"condition_result": False}

    async def http_request_handler(context: NodeExecutionContext) -> Any:
        import httpx

        kwargs_str = str(context.kwargs or "{}").strip()
        kwargs_data = json.loads(kwargs_str) if kwargs_str else {}

        url = kwargs_data.get("url")
        method = kwargs_data.get("method", "GET").upper()
        headers = kwargs_data.get("headers", {})
        body = kwargs_data.get("body")

        if not url:
            raise ValueError("HTTP请求节点缺少URL配置")

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=body if body else None,
                timeout=30.0,
            )
            return {
                "status_code": response.status_code,
                "body": response.text,
                "headers": dict(response.headers),
            }

    WorkflowEngine.register_handler("input", input_handler)
    WorkflowEngine.register_handler("output", output_handler)
    WorkflowEngine.register_handler("condition", condition_handler)
    WorkflowEngine.register_handler("http_request", http_request_handler)


register_builtin_handlers()
