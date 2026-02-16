from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import NodeModel
from .schema import (
    NodeCreateSchema,
    NodeOutSchema,
    NodeUpdateSchema,
)


class NodeCRUD(CRUDBase[NodeModel, NodeCreateSchema, NodeUpdateSchema]):
    """节点数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth
        super().__init__(model=NodeModel, auth=auth)

    async def get_by_id_crud(
        self, id: int, preload: list[str | Any] | None = None
    ) -> NodeModel | None:
        """
        获取节点类型详情

        参数:
        - id (int): 节点类型ID
        - preload (list[str | Any] | None): 预加载关联数据

        返回:
        - NodeTypeModel | None: 节点类型模型实例
        """
        return await self.get(id=id, preload=preload)

    async def get_by_code_crud(self, code: str) -> NodeModel | None:
        """
        根据编码获取节点类型

        参数:
        - code (str): 节点类型编码

        返回:
        - NodeModel | None: 节点模型实例
        """
        return await self.get(code=code)

    async def page_crud(
        self,
        offset: int,
        limit: int,
        order_by: list[dict] | None = None,
        search: dict | None = None,
        preload: list | None = None,
    ) -> dict:
        """
        分页查询节点类型

        参数:
        - offset (int): 偏移量
        - limit (int): 限制数量
        - order_by (list[dict] | None): 排序条件
        - search (dict | None): 查询条件
        - preload (list | None): 预加载关联数据

        返回:
        - dict: 分页查询结果
        """
        order_by_list = order_by or [{"sort_order": "asc"}, {"id": "desc"}]
        search_dict = search or {}

        return await self.page(
            offset=offset,
            limit=limit,
            order_by=order_by_list,
            search=search_dict,
            out_schema=NodeOutSchema,
            preload=preload,
        )

    async def create_crud(self, data: NodeCreateSchema) -> NodeModel | None:
        """
        创建节点类型

        参数:
        - data (NodeCreateSchema): 节点类型创建模型

        返回:
        - NodeModel | None: 节点类型模型实例
        """
        return await self.create(data=data)

    async def update_crud(self, id: int, data: NodeUpdateSchema) -> NodeModel | None:
        """
        更新节点类型

        参数:
        - id (int): 节点类型ID
        - data (NodeUpdateSchema): 节点类型更新模型

        返回:
        - NodeModel | None: 节点类型模型实例
        """
        return await self.update(id=id, data=data)

    async def delete_crud(self, ids: list[int]) -> None:
        """
        删除节点类型

        参数:
        - ids (list[int]): 节点类型ID列表

        返回:
        - None
        """
        await self.delete(ids=ids)
