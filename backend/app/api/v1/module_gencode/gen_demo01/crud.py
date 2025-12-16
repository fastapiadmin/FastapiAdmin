# -*- coding: utf-8 -*-

from typing import Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import GenDemo01Model
from .schema import GenDemo01CreateSchema, GenDemo01UpdateSchema, GenDemo01OutSchema


class GenDemo01CRUD(CRUDBase[GenDemo01Model, GenDemo01CreateSchema, GenDemo01UpdateSchema]):
    """示例数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化CRUD数据层
        
        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=GenDemo01Model, auth=auth)

    async def get_by_id_gen_demo01_crud(self, id: int, preload: list | None = None) -> GenDemo01Model | None:
        """
        详情
        
        参数:
        - id (int): 对象ID
        - preload (list | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - GenDemo01Model | None: 模型实例或None
        """
        return await self.get(id=id, preload=preload)
    
    async def list_gen_demo01_crud(self, search: dict | None = None, order_by: list[dict] | None = None, preload: list | None = None) -> Sequence[GenDemo01Model]:
        """
        列表查询
        
        参数:
        - search (dict | None): 查询参数
        - order_by (list[dict] | None): 排序参数，未提供时使用模型默认项
        - preload (list | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[GenDemo01Model]: 模型实例序列
        """
        return await self.list(search=search, order_by=order_by, preload=preload)
    
    async def create_gen_demo01_crud(self, data: GenDemo01CreateSchema) -> GenDemo01Model | None:
        """
        创建
        
        参数:
        - data (GenDemo01CreateSchema): 创建模型
        
        返回:
        - GenDemo01Model | None: 模型实例或None
        """
        return await self.create(data=data)
    
    async def update_gen_demo01_crud(self, id: int, data: GenDemo01UpdateSchema) -> GenDemo01Model | None:
        """
        更新
        
        参数:
        - id (int): 对象ID
        - data (GenDemo01UpdateSchema): 更新模型
        
        返回:
        - GenDemo01Model | None: 模型实例或None
        """
        return await self.update(id=id, data=data)
    
    async def delete_gen_demo01_crud(self, ids: list[int]) -> None:
        """
        批量删除
        
        参数:
        - ids (list[int]): 对象ID列表
        
        返回:
        - None
        """
        return await self.delete(ids=ids)
    
    async def set_available_gen_demo01_crud(self, ids: list[int], status: str) -> None:
        """
        批量设置可用状态
        
        参数:
        - ids (list[int]): 对象ID列表
        - status (str): 可用状态
        
        返回:
        - None
        """
        return await self.set(ids=ids, status=status)
    
    async def page_gen_demo01_crud(self, offset: int, limit: int, order_by: list[dict] | None = None, search: dict | None = None, preload: list | None = None) -> dict:
        """
        分页查询
        
        参数:
        - offset (int): 偏移量
        - limit (int): 每页数量
        - order_by (list[dict] | None): 排序参数，未提供时使用模型默认项
        - search (dict | None): 查询参数，未提供时查询所有
        - preload (list | None): 预加载关系，未提供时使用模型默认项
        
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
            out_schema=GenDemo01OutSchema,
            preload=preload
        )