from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.exceptions import CustomException
from app.utils.common_util import search_to_dict

from .crud import WorkflowNodeTypeCRUD
from .schema import (
    WorkflowNodeTypeCreateSchema,
    WorkflowNodeTypeOutSchema,
    WorkflowNodeTypeQueryParam,
    WorkflowNodeTypeUpdateSchema,
)


class WorkflowNodeTypeService:
    """工作流节点类型（与定时任务 task_node 无关）"""

    def __init__(self, auth: AuthSchema, db: AsyncSession) -> None:
        self.auth = auth
        self.db = db

    @staticmethod
    def _out(obj) -> WorkflowNodeTypeOutSchema:
        return WorkflowNodeTypeOutSchema.model_validate(obj)

    async def get_options(self) -> list[dict]:
        objs = await WorkflowNodeTypeCRUD(self.auth, self.db).list_active_options_crud()
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
        obj = await WorkflowNodeTypeCRUD(self.auth, self.db).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="节点类型不存在")
        return self._out(obj)

    async def get_list(
        self,
        search: WorkflowNodeTypeQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[WorkflowNodeTypeOutSchema]:
        if order_by is None:
            order_by = [{"sort_order": "asc"}, {"id": "asc"}]
        obj_list = await WorkflowNodeTypeCRUD(self.auth, self.db).get_obj_list_crud(
            search=search_to_dict(search, {}),
            order_by=order_by,
        )
        return [self._out(o) for o in obj_list]

    async def get_page(
        self,
        page_no: int,
        page_size: int,
        search: WorkflowNodeTypeQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> PageResultSchema[WorkflowNodeTypeOutSchema]:
        offset = (page_no - 1) * page_size
        order = order_by or [{"sort_order": "asc"}, {"id": "asc"}]
        result = await WorkflowNodeTypeCRUD(self.auth, self.db).page(
            offset=offset,
            limit=page_size,
            order_by=order,
            search=search_to_dict(search, {}),
            out_schema=WorkflowNodeTypeOutSchema,
        )
        return result

    async def create(self, data: WorkflowNodeTypeCreateSchema) -> WorkflowNodeTypeOutSchema:
        exist = await WorkflowNodeTypeCRUD(self.auth, self.db).get(code=data.code)
        if exist:
            raise CustomException(msg="节点编码已存在")
        obj = await WorkflowNodeTypeCRUD(self.auth, self.db).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建失败")
        return self._out(obj)

    async def update(self, id: int, data: WorkflowNodeTypeUpdateSchema) -> WorkflowNodeTypeOutSchema:
        exist = await WorkflowNodeTypeCRUD(self.auth, self.db).get_obj_by_id_crud(id=id)
        if not exist:
            raise CustomException(msg="节点类型不存在")
        if exist.code != data.code:
            other = await WorkflowNodeTypeCRUD(self.auth, self.db).get(code=data.code)
            if other:
                raise CustomException(msg="节点编码已存在")
        obj = await WorkflowNodeTypeCRUD(self.auth, self.db).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败")
        return self._out(obj)

    async def delete(self, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除ID不能为空")
        await WorkflowNodeTypeCRUD(self.auth, self.db).delete_obj_crud(ids=ids)

    async def get_select(self) -> list[dict]:
        objs = await WorkflowNodeTypeCRUD(self.auth, self.db).get_obj_list_crud()
        return [{"id": o.id, "name": o.name} for o in objs]
