# -*- coding: utf-8 -*-

from typing import Sequence, Any

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

    async def get_by_id_crud(self, id: int, preload: list[str | Any] | None = None) -> ApplicationModel | None:
        """
        根据id获取应用详情
        
        参数:
        - id (int): 应用ID
        - preload (list[str | Any] | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - ApplicationModel | None: 应用详情,如果不存在则为None
        """
        return await self.get(id=id, preload=preload)
    
    async def list_crud(self, search: dict[str, Any] | None = None, order_by: list[dict[str, str]] | None = None, preload: list[str | Any] | None = None) -> Sequence[ApplicationModel]:
        """
        列表查询应用
        
        参数:
        - search (dict[str, Any] | None): 查询参数,默认None
        - order_by (list[dict[str, str]] | None): 排序参数,默认None
        - preload (list[str | Any] | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[ApplicationModel]: 应用列表
        """
        return await self.list(search=search, order_by=order_by, preload=preload)
    
    async def create_crud(self, data: ApplicationCreateSchema) -> ApplicationModel | None:
        """
        创建应用
        
        参数:
        - data (ApplicationCreateSchema): 应用创建模型
        
        返回:
        - ApplicationModel | None: 创建的应用详情,如果创建失败则为None
        """
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: ApplicationUpdateSchema) -> ApplicationModel | None:
        """
        更新应用
        
        参数:
        - id (int): 应用ID
        - data (ApplicationUpdateSchema): 应用更新模型
        
        返回:
        - ApplicationModel | None: 更新后的应用详情,如果更新失败则为None
        """
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, ids: list[int]) -> None:
        """
        批量删除应用
        
        参数:
        - ids (list[int]): 应用ID列表
        """
        return await self.delete(ids=ids)
    
    async def set_available_crud(self, ids: list[int], status: str) -> None:
        """
        批量设置可用状态
        
        参数:
        - ids (list[int]): 应用ID列表
        - status (str): 可用状态,True为可用,False为不可用
        """
        return await self.set(ids=ids, status=status)