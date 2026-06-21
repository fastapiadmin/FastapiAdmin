from collections.abc import Sequence
from typing import Any

from app.common.enums import QueueEnum
from app.core.base_crud import CRUDBase
from app.core.base_schema import AuthSchema

from .model import WorkflowNodeTypeModel
from .schema import WorkflowNodeTypeCreateSchema, WorkflowNodeTypeUpdateSchema


class WorkflowNodeTypeCRUD(CRUDBase[WorkflowNodeTypeModel, WorkflowNodeTypeCreateSchema, WorkflowNodeTypeUpdateSchema]):
    """编排节点类型 CRUD"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化编排节点类型 CRUD。

        参数:
        - auth (AuthSchema): 认证信息。

        返回:
        - None
        """
        super().__init__(model=WorkflowNodeTypeModel, auth=auth)

    async def get_obj_by_id_crud(self, id: int, preload: list[str | Any] | None = None) -> WorkflowNodeTypeModel | None:
        """
        按主键查询节点类型。

        参数:
        - id (int): 主键。
        - preload (list[str | Any] | None): 预加载关系。

        返回:
        - WorkflowNodeTypeModel | None: 实体或 None。
        """
        return await self.get(id=id, preload=preload)

    async def get_obj_list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
        preload: list[str | Any] | None = None,
    ) -> Sequence[WorkflowNodeTypeModel]:
        """
        条件列表查询节点类型。

        参数:
        - search (dict | None): 查询条件。
        - order_by (list[dict[str, str]] | None): 排序。
        - preload (list[str | Any] | None): 预加载关系。

        返回:
        - Sequence[WorkflowNodeTypeModel]: 列表。
        """
        return await self.get_list(search=search, order_by=order_by, preload=preload)

    async def create_obj_crud(self, data: WorkflowNodeTypeCreateSchema) -> WorkflowNodeTypeModel | None:
        """
        创建节点类型。

        参数:
        - data (WorkflowNodeTypeCreateSchema): 创建模型。

        返回:
        - WorkflowNodeTypeModel | None: 新建实体或 None。
        """
        return await self.create(data=data)

    async def update_obj_crud(self, id: int, data: WorkflowNodeTypeUpdateSchema) -> WorkflowNodeTypeModel | None:
        """
        更新节点类型。

        参数:
        - id (int): 主键。
        - data (WorkflowNodeTypeUpdateSchema): 更新模型。

        返回:
        - WorkflowNodeTypeModel | None: 更新后实体或 None。
        """
        return await self.update(id=id, data=data)

    async def delete_obj_crud(self, ids: list[int]) -> None:
        """
        批量删除节点类型。

        参数:
        - ids (list[int]): ID 列表。

        返回:
        - None
        """
        await self.delete(ids=ids)

    async def list_active_options_crud(self) -> Sequence[WorkflowNodeTypeModel]:
        """
        画布用：仅启用的类型，按 sort_order、id 排序。

        返回:
        - Sequence[WorkflowNodeTypeModel]: 启用中的节点类型列表。
        """
        return await self.get_obj_list_crud(
            search={"is_active": (QueueEnum.eq.value, True)},
            order_by=[{"sort_order": "asc"}, {"id": "asc"}],
        )
