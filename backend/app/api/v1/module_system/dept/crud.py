# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence, Union, Any

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

    async def get_by_id_crud(self, id: int, preload: Optional[List[Union[str, Any]]] = None) -> Optional[DeptModel]:
        """
        根据 id 获取部门信息。
        
        参数:
        - id (int): 部门 ID。
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - DeptModel | None: 部门信息，未找到返回 None。
        """
        obj = await self.get(id=id, preload=preload)
        if not obj:
            return None
        return obj

    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, preload: Optional[List[Union[str, Any]]] = None) -> Sequence[DeptModel]:
        """
        获取部门列表。
        
        参数:
        - search (Dict | None): 搜索条件。
        - order_by (List[Dict[str, str]] | None): 排序字段列表。
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[DeptModel]: 部门列表。
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def get_tree_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, preload: Optional[List[Union[str, Any]]] = None) -> Sequence[DeptModel]:
        """
        获取部门树形列表。
        
        参数:
        - search (Dict | None): 搜索条件。
        - order_by (List[Dict[str, str]] | None): 排序字段列表。
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[DeptModel]: 部门树形列表。
        """
        return await self.tree_list(search=search, order_by=order_by, children_attr='children', preload=preload)

    async def set_available_crud(self, ids: List[int], status: str) -> None:
        """
        批量设置部门可用状态。
        
        参数:
        - ids (List[int]): 部门 ID 列表。
        - status (bool): 可用状态。
        
        返回:
        - None
        """
        await self.set(ids=ids, status=status)

    async def get_name_crud(self, id: int) -> Optional[str]:
        """
        根据 id 获取部门名称。
        
        参数:
        - id (int): 部门 ID。
        
        返回:
        - str | None: 部门名称，未找到返回 None。
        """
        obj = await self.get(id=id)
        return obj.name if obj else None