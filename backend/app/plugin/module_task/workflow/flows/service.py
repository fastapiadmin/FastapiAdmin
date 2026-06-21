
import asyncio
from typing import Any

from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException

from ..handlers.workflow_engine import run_workflow_sync, utc_now_iso, validate_workflow_graph
from ..nodes.crud import WorkflowNodeTypeCRUD
from .crud import WorkflowCRUD
from .schema import (
    WorkflowCreateSchema,
    WorkflowExecuteResultSchema,
    WorkflowExecuteSchema,
    WorkflowOutSchema,
    WorkflowQueryParam,
    WorkflowUpdateSchema,
)


class WorkflowService:
    """工作流：画布存储 + 发布校验 + 分层并行执行"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    def _out(self, obj: Any) -> WorkflowOutSchema:
        return WorkflowOutSchema.model_validate(obj)

    async def get_workflow_detail(self, id: int) -> WorkflowOutSchema:
        obj = await WorkflowCRUD(self.auth).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="工作流不存在")
        return self._out(obj)

    async def get_workflow_list(
        self,
        search: WorkflowQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[WorkflowOutSchema]:
        if order_by is None:
            order_by = [{"updated_time": "desc"}]
        obj_list = await WorkflowCRUD(self.auth).get_obj_list_crud(
            search=vars(search) if search else None,
            order_by=order_by,
        )
        return [self._out(o) for o in obj_list]

    async def get_workflow_page(
        self,
        page_no: int,
        page_size: int,
        search: WorkflowQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        offset = (page_no - 1) * page_size
        order = order_by or [{"updated_time": "desc"}]
        result = await WorkflowCRUD(self.auth).page(
            offset=offset,
            limit=page_size,
            order_by=order,
            search=vars(search) if search else None,
            out_schema=WorkflowOutSchema,
        )
        result.items = [WorkflowOutSchema.model_validate(item).model_dump(mode="json") for item in result.items]
        return result

    async def create_workflow(self, data: WorkflowCreateSchema) -> WorkflowOutSchema:
        exist = await WorkflowCRUD(self.auth).get(code=data.code)
        if exist:
            raise CustomException(msg="流程编码已存在")
        obj = await WorkflowCRUD(self.auth).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建工作流失败")
        return self._out(obj)

    async def update_workflow(self, id: int, data: WorkflowUpdateSchema) -> WorkflowOutSchema:
        exist = await WorkflowCRUD(self.auth).get_obj_by_id_crud(id=id)
        if not exist:
            raise CustomException(msg="工作流不存在")
        if exist.code != data.code:
            other = await WorkflowCRUD(self.auth).get(code=data.code)
            if other:
                raise CustomException(msg="流程编码已存在")
        obj = await WorkflowCRUD(self.auth).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新工作流失败")
        return self._out(obj)

    async def delete_workflow(self, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除ID不能为空")
        await WorkflowCRUD(self.auth).delete_obj_crud(ids=ids)

    async def publish_workflow(self, id: int) -> WorkflowOutSchema:
        obj = await WorkflowCRUD(self.auth).get_obj_by_id_crud(id=id)
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
        updated = await WorkflowCRUD(self.auth).update_obj_crud(id=id, data=data)
        if not updated:
            raise CustomException(msg="发布失败")
        return self._out(updated)

    async def execute_workflow(self, body: WorkflowExecuteSchema) -> WorkflowExecuteResultSchema:
        obj = await WorkflowCRUD(self.auth).get_obj_by_id_crud(id=body.workflow_id)
        if not obj:
            raise CustomException(msg="工作流不存在")
        if obj.workflow_status != "published":
            raise CustomException(msg="仅已发布的工作流可执行")

        nodes = obj.nodes or []
        edges = obj.edges or []
        if not nodes:
            raise CustomException(msg="工作流没有节点")

        codes_set = {n.get("type") for n in nodes if n.get("type")}
        code_list = list(codes_set)
        templates: dict[str, dict[str, Any]] = {}
        type_objs = await WorkflowNodeTypeCRUD(self.auth).get_obj_list_crud(search={"code": ("in", code_list)})
        type_map = {t.code: t for t in type_objs}
        for code in codes_set:
            node_type = type_map.get(code)
            if not node_type:
                raise CustomException(msg=f"编排节点类型未注册（请在「工作流编排节点类型」中维护，非定时任务节点）: {code}")
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
                run_workflow_sync,
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
            return err

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
        return ok
