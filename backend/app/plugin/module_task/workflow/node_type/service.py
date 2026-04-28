from app.api.v1.module_system.auth.schema import AuthSchema
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

    @classmethod
    def _out(cls, obj) -> dict:
        return WorkflowNodeTypeOutSchema.model_validate(obj).model_dump(mode="json")

    @classmethod
    async def get_options_service(cls, auth: AuthSchema) -> list[dict]:
        """
        画布左侧 palette：仅返回启用项，结构与前端 Node options 对齐。

        参数:
        - auth (AuthSchema): 认证信息。

        返回:
        - list[dict]: 选项字典列表。
        """
        objs = await WorkflowNodeTypeCRUD(auth).list_active_options_crud()
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

    @classmethod
    async def get_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取编排节点类型详情。

        参数:
        - auth (AuthSchema): 认证信息。
        - id (int): 主键。

        返回:
        - dict: 序列化后的详情。

        异常:
        - CustomException: 不存在时抛出。
        """
        obj = await WorkflowNodeTypeCRUD(auth).get_obj_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="编排节点类型不存在")
        return cls._out(obj)

    @classmethod
    async def get_list_service(
        cls,
        auth: AuthSchema,
        search: WorkflowNodeTypeQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        获取编排节点类型列表（非分页）。

        参数:
        - auth (AuthSchema): 认证信息。
        - search (WorkflowNodeTypeQueryParam | None): 查询条件。
        - order_by (list[dict[str, str]] | None): 排序。

        返回:
        - list[dict]: 字典列表。
        """
        if order_by is None:
            order_by = [{"sort_order": "asc"}, {"id": "asc"}]
        obj_list = await WorkflowNodeTypeCRUD(auth).get_obj_list_crud(
            search=search.__dict__ if search else None,
            order_by=order_by,
        )
        return [cls._out(o) for o in obj_list]

    @classmethod
    async def get_page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: WorkflowNodeTypeQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询编排节点类型（数据库 OFFSET/LIMIT）。

        参数:
        - auth (AuthSchema): 认证信息。
        - page_no (int): 页码。
        - page_size (int): 每页条数。
        - search (WorkflowNodeTypeQueryParam | None): 查询条件。
        - order_by (list[dict[str, str]] | None): 排序。

        返回:
        - dict: 分页结果（items 已 JSON 友好序列化）。
        """
        offset = (page_no - 1) * page_size
        order = order_by or [{"sort_order": "asc"}, {"id": "asc"}]
        result = await WorkflowNodeTypeCRUD(auth).page(
            offset=offset,
            limit=page_size,
            order_by=order,
            search=search.__dict__ if search else {},
            out_schema=WorkflowNodeTypeOutSchema,
        )
        result["items"] = [
            WorkflowNodeTypeOutSchema.model_validate(item).model_dump(mode="json")
            for item in result["items"]
        ]
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: WorkflowNodeTypeCreateSchema) -> dict:
        """
        创建编排节点类型。

        参数:
        - auth (AuthSchema): 认证信息。
        - data (WorkflowNodeTypeCreateSchema): 创建体。

        返回:
        - dict: 新建记录字典。

        异常:
        - CustomException: 编码重复或创建失败。
        """
        exist = await WorkflowNodeTypeCRUD(auth).get(code=data.code)
        if exist:
            raise CustomException(msg="节点编码已存在")
        obj = await WorkflowNodeTypeCRUD(auth).create_obj_crud(data=data)
        if not obj:
            raise CustomException(msg="创建失败")
        return cls._out(obj)

    @classmethod
    async def update_service(
        cls, auth: AuthSchema, id: int, data: WorkflowNodeTypeUpdateSchema
    ) -> dict:
        """
        更新编排节点类型。

        参数:
        - auth (AuthSchema): 认证信息。
        - id (int): 主键。
        - data (WorkflowNodeTypeUpdateSchema): 更新体。

        返回:
        - dict: 更新后字典。

        异常:
        - CustomException: 不存在、编码冲突或更新失败。
        """
        exist = await WorkflowNodeTypeCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist:
            raise CustomException(msg="编排节点类型不存在")
        if exist.code != data.code:
            other = await WorkflowNodeTypeCRUD(auth).get(code=data.code)
            if other:
                raise CustomException(msg="节点编码已存在")
        obj = await WorkflowNodeTypeCRUD(auth).update_obj_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败")
        return cls._out(obj)

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除编排节点类型。

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
        await WorkflowNodeTypeCRUD(auth).delete_obj_crud(ids=ids)
