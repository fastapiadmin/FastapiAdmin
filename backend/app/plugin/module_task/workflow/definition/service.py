import asyncio
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException

from ..engine.prefect_engine import run_prefect_workflow_sync, utc_now_iso, validate_workflow_graph
from ..node_type.crud import WorkflowNodeTypeCRUD
from .crud import WorkflowCRUD
from .schema import (
    WorkflowCreateSchema,
    WorkflowExecuteResultSchema,
    WorkflowExecuteSchema,
    WorkflowOutSchema,
    WorkflowPublishSchema,
    WorkflowQueryParam,
    WorkflowUpdateSchema,
)


class WorkflowService:
    """工作流：画布存储 + 发布校验 + Prefect 执行"""

    @staticmethod
    def _out(obj: Any) -> dict:
        return WorkflowOutSchema.model_validate(obj).model_dump(mode="json")

    @classmethod
    async def get_workflow_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取工作流详情。

        参数:
        - auth (AuthSchema): 认证信息。
        - id (int): 工作流 ID。

        返回:
        - dict: 序列化后的工作流详情。

        异常:
        - CustomException: 不存在时抛出。
        """
        obj = await WorkflowCRUD(auth).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="工作流不存在")
        return cls._out(obj)

    @classmethod
    async def get_workflow_list_service(
        cls,
        auth: AuthSchema,
        search: WorkflowQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        获取工作流列表（非分页）。

        参数:
        - auth (AuthSchema): 认证信息。
        - search (WorkflowQueryParam | None): 查询条件。
        - order_by (list[dict[str, str]] | None): 排序。

        返回:
        - list[dict]: 工作流字典列表。
        """
        if order_by is None:
            order_by = [{"updated_time": "desc"}]
        obj_list = await WorkflowCRUD(auth).get_obj_list_crud(
            search=search.__dict__ if search else None,
            order_by=order_by,
        )
        return [cls._out(o) for o in obj_list]

    @classmethod
    async def get_workflow_page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: WorkflowQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询工作流（数据库 OFFSET/LIMIT）。

        参数:
        - auth (AuthSchema): 认证信息。
        - page_no (int): 页码。
        - page_size (int): 每页条数。
        - search (WorkflowQueryParam | None): 查询条件。
        - order_by (list[dict[str, str]] | None): 排序。

        返回:
        - dict: 分页结果（items 已 JSON 友好序列化）。
        """
        offset = (page_no - 1) * page_size
        order = order_by or [{"updated_time": "desc"}]
        result = await WorkflowCRUD(auth).page(
            offset=offset,
            limit=page_size,
            order_by=order,
            search=search.__dict__ if search else {},
            out_schema=WorkflowOutSchema,
        )
        result["items"] = [
            WorkflowOutSchema.model_validate(item).model_dump(mode="json")
            for item in result["items"]
        ]
        return result

    @classmethod
    async def create_workflow_service(cls, auth: AuthSchema, data: WorkflowCreateSchema) -> dict:
        """
        创建工作流草稿。

        参数:
        - auth (AuthSchema): 认证信息。
        - data (WorkflowCreateSchema): 创建体。

        返回:
        - dict: 新建工作流字典。

        异常:
        - CustomException: 编码重复或创建失败。
        """
        exist = await WorkflowCRUD(auth).get(code=data.code)
        if exist:
            raise CustomException(msg="流程编码已存在")
        obj = await WorkflowCRUD(auth).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建工作流失败")
        return cls._out(obj)

    @classmethod
    async def update_workflow_service(
        cls, auth: AuthSchema, id: int, data: WorkflowUpdateSchema
    ) -> dict:
        """
        更新工作流。

        参数:
        - auth (AuthSchema): 认证信息。
        - id (int): 工作流 ID。
        - data (WorkflowUpdateSchema): 更新体。

        返回:
        - dict: 更新后工作流字典。

        异常:
        - CustomException: 不存在、编码冲突或更新失败。
        """
        exist = await WorkflowCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist:
            raise CustomException(msg="工作流不存在")
        if exist.code != data.code:
            other = await WorkflowCRUD(auth).get(code=data.code)
            if other:
                raise CustomException(msg="流程编码已存在")
        obj = await WorkflowCRUD(auth).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新工作流失败")
        return cls._out(obj)

    @classmethod
    async def delete_workflow_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除工作流。

        参数:
        - auth (AuthSchema): 认证信息。
        - ids (list[int]): ID 列表。

        返回:
        - None

        异常:
        - CustomException: ID 为空时抛出。
        """
        if not ids:
            raise CustomException(msg="删除ID不能为空")
        await WorkflowCRUD(auth).delete_obj_crud(ids=ids)

    @classmethod
    async def publish_workflow_service(
        cls, auth: AuthSchema, id: int, body: WorkflowPublishSchema | None = None
    ) -> dict:
        """
        校验 DAG 后发布工作流。

        参数:
        - auth (AuthSchema): 认证信息。
        - id (int): 工作流 ID。
        - body (WorkflowPublishSchema | None): 可选附加参数。

        返回:
        - dict: 发布后工作流字典。

        异常:
        - CustomException: 不存在、图无效或发布失败。
        """
        obj = await WorkflowCRUD(auth).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="工作流不存在")
        nodes = obj.nodes or []
        edges = obj.edges or []

        try:
            validate_workflow_graph(nodes, edges)
        except ValueError as e:
            raise CustomException(msg=str(e)) from e

        data = WorkflowUpdateSchema(
            name=obj.name,
            code=obj.code,
            description=obj.description,
            nodes=obj.nodes,
            edges=obj.edges,
            workflow_status="published",
        )
        updated = await WorkflowCRUD(auth).update_obj_crud(id=id, data=data)
        if not updated:
            raise CustomException(msg="发布失败")
        return cls._out(updated)

    @classmethod
    async def execute_workflow_service(cls, auth: AuthSchema, body: WorkflowExecuteSchema) -> dict:
        """
        执行已发布工作流（Prefect 同步入口在线程池中运行）。

        参数:
        - auth (AuthSchema): 认证信息。
        - body (WorkflowExecuteSchema): 工作流 ID 与变量。

        返回:
        - dict: 执行结果摘要（成功或失败结构）。

        异常:
        - CustomException: 未发布、缺节点、节点类型未注册等。
        """
        obj = await WorkflowCRUD(auth).get_obj_by_id_crud(id=body.workflow_id)
        if not obj:
            raise CustomException(msg="工作流不存在")
        if obj.workflow_status != "published":
            raise CustomException(msg="仅已发布的工作流可执行")

        nodes = obj.nodes or []
        edges = obj.edges or []
        if not nodes:
            raise CustomException(msg="工作流没有节点")

        codes = {n.get("type") for n in nodes if n.get("type")}
        templates: dict[str, dict[str, Any]] = {}
        for code in codes:
            node_type = await WorkflowNodeTypeCRUD(auth).get(code=code)
            if not node_type:
                raise CustomException(
                    msg=f"编排节点类型未注册（请在「工作流编排节点类型」中维护，非定时任务节点）: {code}"
                )
            if not node_type.func or not str(node_type.func).strip():
                raise CustomException(msg=f"编排节点类型未配置 func 代码块: {code}")
            templates[code] = {
                "func": node_type.func,
                "args": node_type.args,
                "kwargs": node_type.kwargs,
            }

        variables = body.variables or {}
        start = utc_now_iso()
        try:
            raw = await asyncio.to_thread(
                run_prefect_workflow_sync,
                nodes,
                edges,
                templates,
                variables,
            )
        except ValueError as e:
            raise CustomException(msg=str(e)) from e
        except CustomException:
            raise
        except Exception as e:
            end = utc_now_iso()
            err = WorkflowExecuteResultSchema(
                workflow_id=obj.id,
                workflow_name=obj.name,
                status="failed",
                start_time=start,
                end_time=end,
                variables=variables,
                node_results=None,
                error=str(e),
            )
            return err.model_dump(mode="json")

        end = utc_now_iso()
        ok = WorkflowExecuteResultSchema(
            workflow_id=obj.id,
            workflow_name=obj.name,
            status="completed",
            start_time=start,
            end_time=end,
            variables=variables,
            node_results=raw.get("node_results"),
            error=None,
        )
        return ok.model_dump(mode="json")
