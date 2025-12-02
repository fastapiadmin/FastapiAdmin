# -*- coding: utf-8 -*-

from typing import Any, AsyncGenerator

from app.core.exceptions import CustomException
from app.api.v1.module_system.auth.schema import AuthSchema
from .tools.ai_util import AIClient
from .schema import McpCreateSchema, McpUpdateSchema, McpOutSchema, ChatQuerySchema, McpQueryParam
from .crud import McpCRUD


class McpService:
    """MCP服务层"""

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict[str, Any]:
        """
        获取MCP服务器详情
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): MCP服务器ID
        
        返回:
        - dict[str, Any]: MCP服务器详情字典
        """
        obj = await McpCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='MCP 服务器不存在')
        return McpOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_service(cls, auth: AuthSchema, search: McpQueryParam | None = None, order_by: list[dict[str, str]] | None = None) -> list[dict[str, Any]]:
        """
        列表查询MCP服务器
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - search (McpQueryParam | None): 查询参数模型
        - order_by (list[dict[str, str]] | None): 排序参数列表
        
        返回:
        - list[dict[str, Any]]: MCP服务器详情字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await McpCRUD(auth).get_list_crud(search=search_dict, order_by=order_by)
        return [McpOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_service(cls, auth: AuthSchema, data: McpCreateSchema) -> dict[str, Any]:
        """
        创建MCP服务器
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (McpCreateSchema): 创建MCP服务器模型
        
        返回:
        - dict[str, Any]: 创建的MCP服务器详情字典
        """
        obj = await McpCRUD(auth).get_by_name_crud(name=data.name)
        if obj:
            raise CustomException(msg='创建失败，MCP 服务器已存在')
        obj = await McpCRUD(auth).create_crud(data=data)
        return McpOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: McpUpdateSchema) -> dict[str, Any]:
        """
        更新MCP服务器
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): MCP服务器ID
        - data (McpUpdateSchema): 更新MCP服务器模型
        
        返回:
        - dict[str, Any]: 更新的MCP服务器详情字典
        """
        obj = await McpCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        exist_obj = await McpCRUD(auth).get_by_name_crud(name=data.name)
        if exist_obj and exist_obj.id != id:
            raise CustomException(msg='更新失败，MCP 服务器名称重复')
        obj = await McpCRUD(auth).update_crud(id=id, data=data)
        return McpOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除MCP服务器
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): MCP服务器ID列表
        
        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await McpCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg='删除失败，该数据不存在')
        await McpCRUD(auth).delete_crud(ids=ids)
    
    @classmethod
    async def chat_query(cls, query: ChatQuerySchema) -> AsyncGenerator[str, Any]:
        """
        处理聊天查询
        
        参数:
        - query (ChatQuerySchema): 聊天查询模型
        
        返回:
        - AsyncGenerator[str, None]: 异步生成器,每次返回一个聊天响应
        """
        # 创建MCP客户端实例
        mcp_client = AIClient()
        try:
            # 处理消息
            async for response in mcp_client.process(query.message):
                yield response
        finally:
            # 确保关闭客户端连接
            await mcp_client.close()
