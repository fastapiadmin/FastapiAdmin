# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence, Union, Any

from app.core.base_crud import CRUDBase

from app.api.v1.module_system.auth.schema import AuthSchema
from .model import TenantModel
from .schema import TenantCreateSchema, TenantUpdateSchema, TenantOutSchema


class TenantCRUD(CRUDBase[TenantModel, TenantCreateSchema, TenantUpdateSchema]):
    """租户数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化CRUD数据层
        
        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=TenantModel, auth=auth)
    
    async def get_by_id_crud(self, id: int, preload: Optional[List[Union[str, Any]]] = None) -> Optional[TenantModel]:
        """
        详情
        
        参数:
        - id (int): 租户ID
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Optional[TenantModel]: 租户模型实例或None
        """
        return await self.get(id=id, preload=preload)
    
    async def list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, preload: Optional[List[Union[str, Any]]] = None) -> Sequence[TenantModel]:
        """
        列表查询
        
        参数:
        - search (Optional[Dict]): 查询参数
        - order_by (Optional[List[Dict[str, str]]]): 排序参数
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[TenantModel]: 租户模型实例序列
        """
        return await self.list(search=search, order_by=order_by, preload=preload)
    
    async def create_crud(self, data: TenantCreateSchema) -> Optional[TenantModel]:
        """
        创建
        
        参数:
        - data (TenantCreateSchema): 租户创建模型
        
        返回:
        - Optional[TenantModel]: 租户模型实例或None
        """
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: TenantUpdateSchema) -> Optional[TenantModel]:
        """
        更新
        
        参数:
        - id (int): 租户ID
        - data (TenantUpdateSchema): 租户更新模型
        
        返回:
        - Optional[TenantModel]: 租户模型实例或None
        """
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, ids: List[int]) -> None:
        """
        批量删除
        
        参数:
        - ids (List[int]): 租户ID列表
        
        返回:
        - None
        """
        return await self.delete(ids=ids)
    
    async def set_available_crud(self, ids: List[int], status: str) -> None:
        """
        批量设置可用状态
        
        参数:
        - ids (List[int]): 租户ID列表
        - status (bool): 可用状态
        
        返回:
        - None
        """
        return await self.set(ids=ids, status=status)
    
    async def page_crud(self, offset: int, limit: int, order_by: Optional[List[Dict[str, str]]] = None, search: Optional[Dict] = None, preload: Optional[List[Union[str, Any]]] = None) -> Dict:
        """
        分页查询
        
        参数:
        - offset (int): 偏移量
        - limit (int): 每页数量
        - order_by (Optional[List[Dict[str, str]]]): 排序参数
        - search (Optional[Dict]): 查询参数
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Dict: 分页数据
        """
        order_by_list = order_by or [{'id': 'asc'}]
        search_dict = search or {}
        
        return await self.page(
            offset=offset,
            limit=limit,
            order_by=order_by_list,
            search=search_dict,
            out_schema=TenantOutSchema,
            preload=preload
        )
