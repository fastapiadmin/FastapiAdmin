# -*- coding: utf-8 -*-

from typing import Sequence

from app.core.base_crud import CRUDBase

from ..auth.schema import AuthSchema
from .model import DeptModel
from .schema import DeptCreateSchema, DeptUpdateSchema


class DeptCRUD(CRUDBase[DeptModel, DeptCreateSchema, DeptUpdateSchema]):
    """部门模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化部门CRUD"""
        self.auth = auth
        super().__init__(model=DeptModel, auth=auth)

    async def get_by_id_crud(self, id: int, preload: list | None = None) -> DeptModel | None:
        """
        根据 id 获取部门信息。
        
        参数:
        - id (int): 部门 ID。
        - preload (list | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - DeptModel | None: 部门信息，未找到返回 None。
        """
        obj = await self.get(id=id, preload=preload)
        if not obj:
            return None
        return obj

    async def get_list_crud(self, search: dict | None = None, order_by: list[dict] | None = None, preload: list | None = None) -> Sequence[DeptModel]:
        """
        获取部门列表。
        
        参数:
        - search (dict | None): 搜索条件。
        - order_by (list[dict] | None): 排序字段列表。
        - preload (list | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[DeptModel]: 部门列表。
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def get_tree_list_crud(self, search: dict | None = None, order_by: list[dict] | None = None, preload: list | None = None) -> Sequence[DeptModel]:
        """
        获取部门树形列表。
        
        参数:
        - search (dict | None): 搜索条件。
        - order_by (list[dict] | None): 排序字段列表。
        - preload (list | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[DeptModel]: 部门树形列表。
        """
        return await self.tree_list(search=search, order_by=order_by, children_attr='children', preload=preload)

    async def set_available_crud(self, ids: list[int], status: str) -> None:
        """
        批量设置部门可用状态。
        
        参数:
        - ids (list[int]): 部门 ID 列表。
        - status (str): 可用状态。
        
        返回:
        - None
        """
        await self.set(ids=ids, status=status)

    async def get_name_crud(self, id: int) -> str | None:
        """
        根据 id 获取部门名称。
        
        参数:
        - id (int): 部门 ID。
        
        返回:
        - str | None: 部门名称，未找到返回 None。
        """
        obj = await self.get(id=id)
        return obj.name if obj else None