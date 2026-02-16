from collections.abc import Sequence
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import WorkflowModel, WorkflowRunLogModel, WorkflowRunModel
from .schema import (
    WorkflowCreateSchema,
    WorkflowOutSchema,
    WorkflowRunCreateSchema,
    WorkflowRunLogCreateSchema,
    WorkflowRunLogOutSchema,
    WorkflowRunOutSchema,
    WorkflowRunUpdateSchema,
    WorkflowUpdateSchema,
)


class WorkflowCRUD(CRUDBase[WorkflowModel, WorkflowCreateSchema, WorkflowUpdateSchema]):
    """工作流数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化CRUD数据层

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=WorkflowModel, auth=auth)

    async def get_by_id_crud(self, id: int, preload: list[str] | None = None) -> WorkflowModel | None:
        """
        详情

        参数:
        - id (int): 工作流ID
        - preload (list[str] | None): 预加载关系，未提供时使用模型默认项

        返回:
        - WorkflowModel | None: 工作流模型实例或None
        """
        return await self.get(id=id, preload=preload)

    async def get_by_code_crud(self, code: str, preload: list[str] | None = None) -> WorkflowModel | None:
        """
        根据编码获取工作流

        参数:
        - code (str): 工作流编码
        - preload (list[str] | None): 预加载关系

        返回:
        - WorkflowModel | None: 工作流模型实例或None
        """
        return await self.get(code=code, preload=preload)

    async def list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict] | None = None,
        preload: list[str] | None = None,
    ) -> Sequence[WorkflowModel]:
        """
        列表查询

        参数:
        - search (dict | None): 查询参数
        - order_by (list[dict] | None): 排序参数
        - preload (list[str] | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[WorkflowModel]: 工作流模型实例序列
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def create_crud(self, data: WorkflowCreateSchema) -> WorkflowModel | None:
        """
        创建

        参数:
        - data (WorkflowCreateSchema): 工作流创建模型

        返回:
        - WorkflowModel | None: 工作流模型实例或None
        """
        return await self.create(data=data)

    async def update_crud(self, id: int, data: WorkflowUpdateSchema) -> WorkflowModel | None:
        """
        更新

        参数:
        - id (int): 工作流ID
        - data (WorkflowUpdateSchema): 工作流更新模型

        返回:
        - WorkflowModel | None: 工作流模型实例或None
        """
        return await self.update(id=id, data=data)

    async def delete_crud(self, ids: list[int]) -> None:
        """
        批量删除

        参数:
        - ids (List[int]): 工作流ID列表

        返回:
        - None
        """
        return await self.delete(ids=ids)

    async def set_available_crud(self, ids: list[int], status: str) -> None:
        """
        批量设置可用状态

        参数:
        - ids (list[int]): 工作流ID列表
        - status (str): 可用状态

        返回:
        - None
        """
        return await self.set(ids=ids, status=status)

    async def page_crud(
        self,
        offset: int,
        limit: int,
        order_by: list[dict] | None = None,
        search: dict | None = None,
        preload: list | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - offset (int): 偏移量
        - limit (int): 每页数量
        - order_by (list[dict] | None): 排序参数
        - search (dict | None): 查询参数
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - dict: 分页数据
        """
        order_by_list = order_by or [{"id": "asc"}]
        search_dict = search or {}

        return await self.page(
            offset=offset,
            limit=limit,
            order_by=order_by_list,
            search=search_dict,
            out_schema=WorkflowOutSchema,
            preload=preload,
        )

    async def list_templates_crud(
        self,
        search: dict | None = None,
        order_by: list[dict] | None = None,
        preload: list[str] | None = None,
    ) -> Sequence[WorkflowModel]:
        """
        获取模板列表

        参数:
        - search (dict | None): 查询参数
        - order_by (list[dict] | None): 排序参数
        - preload (list[str] | None): 预加载关系

        返回:
        - Sequence[WorkflowModel]: 工作流模型实例序列
        """
        search_dict = search or {}
        search_dict["is_template"] = (None, True)
        return await self.list(search=search_dict, order_by=order_by, preload=preload)


class WorkflowRunCRUD(CRUDBase[WorkflowRunModel, WorkflowRunCreateSchema, WorkflowRunUpdateSchema]):
    """工作流运行记录CRUD"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD数据层"""
        super().__init__(model=WorkflowRunModel, auth=auth)

    async def list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict] | None = None,
        preload: list[str | Any] | None = None,
    ) -> Sequence[WorkflowRunModel]:
        """获取工作流运行记录列表"""
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def create_crud(self, data: WorkflowRunCreateSchema) -> WorkflowRunModel | None:
        """创建工作流运行记录"""
        return await self.create(data=data)

    async def get_by_id_crud(self, id: int) -> WorkflowRunModel | None:
        """根据ID获取工作流运行记录"""
        return await self.get(id=id)

    async def update_crud(self, id: int, data: WorkflowRunUpdateSchema) -> WorkflowRunModel | None:
        """更新工作流运行记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, ids: list[int]) -> None:
        """删除工作流运行记录"""
        return await self.delete(ids=ids)

    async def clear_crud(self) -> None:
        """清除所有工作流运行记录"""
        return await self.clear()

    async def page_crud(
        self,
        offset: int,
        limit: int,
        order_by: list[dict] | None = None,
        search: dict | None = None,
        preload: list | None = None,
    ) -> dict:
        """分页查询工作流运行记录"""
        order_by_list = order_by or [{"id": "desc"}]
        search_dict = search or {}

        return await self.page(
            offset=offset,
            limit=limit,
            order_by=order_by_list,
            search=search_dict,
            out_schema=WorkflowRunOutSchema,
            preload=preload,
        )


class WorkflowRunLogCRUD(CRUDBase[WorkflowRunLogModel, WorkflowRunLogCreateSchema, WorkflowRunLogCreateSchema]):
    """工作流运行日志CRUD"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD数据层"""
        super().__init__(model=WorkflowRunLogModel, auth=auth)

    async def list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict] | None = None,
        preload: list[str | Any] | None = None,
    ) -> Sequence[WorkflowRunLogModel]:
        """获取工作流运行日志列表"""
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def create_crud(self, data: WorkflowRunLogCreateSchema) -> WorkflowRunLogModel | None:
        """创建工作流运行日志"""
        return await self.create(data=data)

    async def page_crud(
        self,
        offset: int,
        limit: int,
        order_by: list[dict] | None = None,
        search: dict | None = None,
        preload: list | None = None,
    ) -> dict:
        """分页查询工作流运行日志"""
        order_by_list = order_by or [{"id": "desc"}]
        search_dict = search or {}

        return await self.page(
            offset=offset,
            limit=limit,
            order_by=order_by_list,
            search=search_dict,
            out_schema=WorkflowRunLogOutSchema,
            preload=preload,
        )
