# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence, Union, Any

from app.core.base_crud import CRUDBase

from app.api.v1.module_system.auth.schema import AuthSchema
from .model import ApplicationModel
from .schema import ApplicationCreateSchema, ApplicationUpdateSchema


class ApplicationCRUD(CRUDBase[ApplicationModel, ApplicationCreateSchema, ApplicationUpdateSchema]):
    """应用系统数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化应用CRUD
        
        参数:
        - auth (AuthSchema): 认证信息模型
        """
        self.auth = auth
        super().__init__(model=ApplicationModel, auth=auth)

    async def get_by_id_crud(self, id: int, preload: Optional[List[Union[str, Any]]] = None) -> Optional[ApplicationModel]:
        """
        根据id获取应用详情
        
        参数:
        - id (int): 应用ID
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Optional[ApplicationModel]: 应用详情,如果不存在则为None
        """
        return await self.get(id=id, preload=preload)
    
    async def list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, preload: Optional[List[Union[str, Any]]] = None) -> Sequence[ApplicationModel]:
        """
        列表查询应用
        
        参数:
        - search (Optional[Dict]): 查询参数,默认None
        - order_by (Optional[List[Dict[str, str]]]): 排序参数,默认None
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[ApplicationModel]: 应用列表
        """
        return await self.list(search=search, order_by=order_by, preload=preload)
    
    async def create_crud(self, data: ApplicationCreateSchema) -> Optional[ApplicationModel]:
        """
        创建应用
        
        参数:
        - data (ApplicationCreateSchema): 应用创建模型
        
        返回:
        - Optional[ApplicationModel]: 创建的应用详情,如果创建失败则为None
        """
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: ApplicationUpdateSchema) -> Optional[ApplicationModel]:
        """
        更新应用
        
        参数:
        - id (int): 应用ID
        - data (ApplicationUpdateSchema): 应用更新模型
        
        返回:
        - Optional[ApplicationModel]: 更新后的应用详情,如果更新失败则为None
        """
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, ids: List[int]) -> None:
        """
        批量删除应用
        
        参数:
        - ids (List[int]): 应用ID列表
        """
        return await self.delete(ids=ids)
    
    async def set_available_crud(self, ids: List[int], status: str) -> None:
        """
        批量设置可用状态
        
        参数:
        - ids (List[int]): 应用ID列表
        - status (bool): 可用状态,True为可用,False为不可用
        """
        return await self.set(ids=ids, status=status)