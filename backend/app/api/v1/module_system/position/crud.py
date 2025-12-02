# -*- coding: utf-8 -*-

from typing import Sequence, Any

from app.core.base_crud import CRUDBase
from ..auth.schema import AuthSchema
from .model import PositionModel
from .schema import PositionCreateSchema, PositionUpdateSchema


class PositionCRUD(CRUDBase[PositionModel, PositionCreateSchema, PositionUpdateSchema]):
    """岗位模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化岗位CRUD
        
        参数:
        - auth (AuthSchema): 认证信息模型
        """
        self.auth = auth
        super().__init__(model=PositionModel, auth=auth)

    async def get_by_id_crud(self, id: int, preload: list[str] | None = None) -> PositionModel | None:
        """
        根据 id 获取岗位信息。
        
        参数:
        - id (int): 岗位 ID。
        - preload (list[str] | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - PositionModel | None: 岗位信息，未找到返回 None。
        """
        return await self.get(id=id, preload=preload)

    async def get_list_crud(self, search: dict | None = None, order_by: list[dict[str, Any]] | None = None, preload: list[str] | None = None) -> Sequence[PositionModel]:
        """
        获取岗位列表。
        
        参数:
        - search (dict | None): 搜索条件。
        - order_by (list[dict[str, Any]] | None): 排序字段列表。
        - preload (list[str] | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[PositionModel]: 岗位列表。
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def set_available_crud(self, ids: list[int], status: str) -> None:
        """
        批量设置岗位可用状态。
        
        参数:
        - ids (list[int]): 岗位 ID 列表。
        - status (bool): 可用状态。
        
        返回:
        - None
        """
        await self.set(ids=ids, status=status)

    async def get_name_crud(self, ids: list[int]) -> list[str]:
        """
        根据 id 列表获取岗位名称。
        
        参数:
        - ids (list[int]): 岗位 ID 列表。
        
        返回:
        - list[str]: 岗位名称列表。
        """
        position_names = []
        for id in ids:
            obj = await self.get(id=id)
            if obj:
                position_names.append(obj.name)
        return position_names