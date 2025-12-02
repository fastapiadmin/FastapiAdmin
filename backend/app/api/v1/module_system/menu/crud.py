# -*- coding: utf-8 -*-

from typing import Sequence

from app.core.base_crud import CRUDBase

from ..auth.schema import AuthSchema
from .model import MenuModel
from .schema import MenuCreateSchema, MenuUpdateSchema


class MenuCRUD(CRUDBase[MenuModel, MenuCreateSchema, MenuUpdateSchema]):
    """菜单模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化菜单CRUD"""
        self.auth = auth
        super().__init__(model=MenuModel, auth=auth)

    async def get_by_id_crud(self, id: int, preload: list[str] | None = None) -> MenuModel | None:
        """
        根据 id 获取菜单信息。
        
        参数:
        - id (int): 菜单 ID。
        - preload (list[str] | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - MenuModel | None: 菜单信息，未找到返回 None。
        """
        obj = await self.get(id=id, preload=preload)
        if not obj:
            return None
        return obj

    async def get_list_crud(self, search: dict | None = None, order_by: list[dict] | None = None, preload: list[str] | None = None) -> Sequence[MenuModel]:
        """
        获取菜单列表。
        
        参数:
        - search (dict | None): 搜索条件。
        - order_by (list[dict] | None): 排序字段列表。
        - preload (list[str] | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[MenuModel]: 菜单列表。
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def get_tree_list_crud(self, search: dict | None = None, order_by: list[dict] | None = None, preload: list[str] | None = None) -> Sequence[MenuModel]:
        """
        获取菜单树形列表。
        
        参数:
        - search (dict | None): 搜索条件。
        - order_by (list[dict] | None): 排序字段列表。
        - preload (list[str] | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[MenuModel]: 菜单树形列表。
        """
        return await self.tree_list(search=search, order_by=order_by, children_attr='children', preload=preload)

    async def set_available_crud(self, ids: list[int], status: str) -> None:
        """
        批量设置菜单可用状态。
        
        参数:
        - ids (list[int]): 菜单 ID 列表。
        - status (str): 可用状态。
        
        返回:
        - None
        """
        await self.set(ids=ids, status=status)