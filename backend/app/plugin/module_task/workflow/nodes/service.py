
from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException

from .crud import WorkflowNodeTypeCRUD
from .schema import (
    WorkflowNodeTypeCreateSchema,
    WorkflowNodeTypeOutSchema,
    WorkflowNodeTypeQueryParam,
    WorkflowNodeTypeUpdateSchema,
)


class WorkflowNodeTypeService:
    """工作流编排节点类型（与定时任务 task_node 无关）"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    @staticmethod
    def _out(obj) -> WorkflowNodeTypeOutSchema:
        return WorkflowNodeTypeOutSchema.model_validate(obj)

    async def get_options(self) -> list[dict]:
        objs = await WorkflowNodeTypeCRUD(self.auth).list_active_options_crud()
        return [
            {
                "id": o.id,
                "code": o.code,
                "name": o.name,
                "category": o.category,
                "args": o.args or "",
                "kwargs": o.kwargs or "{}",
            }
            for o in objs
        ]

    async def get_detail(self, id: int) -> WorkflowNodeTypeOutSchema:
        obj = await WorkflowNodeTypeCRUD(self.auth).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="编排节点类型不存在")
        return self._out(obj)

    async def get_list(
        self,
        search: WorkflowNodeTypeQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[WorkflowNodeTypeOutSchema]:
        if order_by is None:
            order_by = [{"sort_order": "asc"}, {"id": "asc"}]
        obj_list = await WorkflowNodeTypeCRUD(self.auth).get_obj_list_crud(
            search=vars(search) if search else None,
            order_by=order_by,
        )
        return [self._out(o) for o in obj_list]

    async def get_page(
        self,
        page_no: int,
        page_size: int,
        search: WorkflowNodeTypeQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        offset = (page_no - 1) * page_size
        order = order_by or [{"sort_order": "asc"}, {"id": "asc"}]
        result = await WorkflowNodeTypeCRUD(self.auth).page(
            offset=offset,
            limit=page_size,
            order_by=order,
            search=vars(search) if search else None,
            out_schema=WorkflowNodeTypeOutSchema,
        )
        result.items = [WorkflowNodeTypeOutSchema.model_validate(item).model_dump(mode="json") for item in result.items]
        return result

    async def create(self, data: WorkflowNodeTypeCreateSchema) -> WorkflowNodeTypeOutSchema:
        exist = await WorkflowNodeTypeCRUD(self.auth).get(code=data.code)
        if exist:
            raise CustomException(msg="节点编码已存在")
        obj = await WorkflowNodeTypeCRUD(self.auth).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建失败")
        return self._out(obj)

    async def update(self, id: int, data: WorkflowNodeTypeUpdateSchema) -> WorkflowNodeTypeOutSchema:
        exist = await WorkflowNodeTypeCRUD(self.auth).get_obj_by_id_crud(id=id)
        if not exist:
            raise CustomException(msg="编排节点类型不存在")
        if exist.code != data.code:
            other = await WorkflowNodeTypeCRUD(self.auth).get(code=data.code)
            if other:
                raise CustomException(msg="节点编码已存在")
        obj = await WorkflowNodeTypeCRUD(self.auth).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败")
        return self._out(obj)

    async def delete(self, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除ID不能为空")
        await WorkflowNodeTypeCRUD(self.auth).delete_obj_crud(ids=ids)

    async def get_select(self) -> list[dict]:
        objs = await WorkflowNodeTypeCRUD(self.auth).get_obj_list_crud()
        return [{"id": o.id, "name": o.name} for o in objs]
