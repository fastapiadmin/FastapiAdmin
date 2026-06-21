from collections.abc import Sequence
from typing import Any

from app.core.base_crud import CRUDBase
from app.core.base_schema import AuthSchema

from .model import WorkflowModel
from .schema import WorkflowCreateSchema, WorkflowUpdateSchema


class WorkflowCRUD(CRUDBase[WorkflowModel, WorkflowCreateSchema, WorkflowUpdateSchema]):
    """工作流数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化工作流 CRUD。

        参数:
        - auth (AuthSchema): 认证信息。

        返回:
        - None
        """
        super().__init__(model=WorkflowModel, auth=auth)

    async def get_obj_by_id_crud(self, id: int, preload: list[str | Any] | None = None) -> WorkflowModel | None:
        """
        按主键查询工作流。

        参数:
        - id (int): 工作流 ID。
        - preload (list[str | Any] | None): 预加载关系。

        返回:
        - WorkflowModel | None: 实体或 None。
        """
        return await self.get(id=id, preload=preload)

    async def get_obj_list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
        preload: list[str | Any] | None = None,
    ) -> Sequence[WorkflowModel]:
        """
        条件列表查询工作流。

        参数:
        - search (dict | None): 查询条件。
        - order_by (list[dict[str, str]] | None): 排序。
        - preload (list[str | Any] | None): 预加载关系。

        返回:
        - Sequence[WorkflowModel]: 工作流列表。
        """
        return await self.get_list(search=search, order_by=order_by, preload=preload)

    async def create_obj_crud(self, data: WorkflowCreateSchema) -> WorkflowModel | None:
        """
        创建工作流。

        参数:
        - data (WorkflowCreateSchema): 创建模型。

        返回:
        - WorkflowModel | None: 新建实体或 None。
        """
        return await self.create(data=data)

    async def update_obj_crud(self, id: int, data: WorkflowUpdateSchema) -> WorkflowModel | None:
        """
        更新工作流。

        参数:
        - id (int): 工作流 ID。
        - data (WorkflowUpdateSchema): 更新模型。

        返回:
        - WorkflowModel | None: 更新后实体或 None。
        """
        return await self.update(id=id, data=data)

    async def delete_obj_crud(self, ids: list[int]) -> None:
        """
        批量删除工作流。

        参数:
        - ids (list[int]): ID 列表。

        返回:
        - None
        """
        await self.delete(ids=ids)
