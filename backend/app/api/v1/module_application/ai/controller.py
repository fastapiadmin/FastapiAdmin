# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Path, Body, WebSocket
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import StreamResponse, SuccessResponse
from app.common.request import PaginationService
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.router_class import OperationLogRoute
from .service import McpService
from .schema import McpCreateSchema, McpUpdateSchema, ChatQuerySchema, McpQueryParam


AIRouter = APIRouter(route_class=OperationLogRoute, prefix="/ai", tags=["MCP智能助手"])


@AIRouter.post("/chat", summary="智能对话", description="与MCP智能助手进行对话")
async def chat_controller(
    query: ChatQuerySchema,
    auth: AuthSchema = Depends(AuthPermission(["module_application:ai:chat"]))
) -> StreamingResponse:
    """
    智能对话接口
    
    参数:
    - query (ChatQuerySchema): 聊天查询模型
    
    返回:
    - StreamingResponse: 流式响应,每次返回一个聊天响应
    """
    user_name = auth.user.name if auth.user else "未知用户"
    log.info(f"用户 {user_name} 发起智能对话: {query.message[:50]}...")
    
    async def generate_response():
        try:
            async for chunk in McpService.chat_query(query=query):
                # 确保返回的是字节串
                if chunk:
                    yield chunk.encode('utf-8') if isinstance(chunk, str) else chunk
        except Exception as e:
            log.error(f"流式响应出错: {str(e)}")
            yield f"抱歉，处理您的请求时出现了错误: {str(e)}".encode('utf-8')
    
    return StreamResponse(generate_response(), media_type="text/plain; charset=utf-8")


@AIRouter.get("/detail/{id}", summary="获取 MCP 服务器详情", description="获取 MCP 服务器详情")
async def detail_controller(
    id: int = Path(..., description="MCP ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_application:ai:query"]))
) -> JSONResponse:
    """
    获取 MCP 服务器详情接口
    
    参数:
    - id (int): MCP 服务器ID
    
    返回:
    - JSONResponse: 包含 MCP 服务器详情的 JSON 响应
    """
    result_dict = await McpService.detail_service(auth=auth, id=id)
    log.info(f"获取 MCP 服务器详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取 MCP 服务器详情成功")


@AIRouter.get("/list", summary="查询 MCP 服务器列表", description="查询 MCP 服务器列表")
async def list_controller(
    page: PaginationQueryParam = Depends(),
    search: McpQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_application:ai:query"]))
) -> JSONResponse:
    """
    查询 MCP 服务器列表接口
    
    参数:
    - page (PaginationQueryParam): 分页查询参数模型
    - search (McpQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含 MCP 服务器列表的 JSON 响应
    """
    result_dict_list = await McpService.list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.paginate(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    log.info(f"查询 MCP 服务器列表成功")
    return SuccessResponse(data=result_dict, msg="查询 MCP 服务器列表成功")


@AIRouter.post("/create", summary="创建 MCP 服务器", description="创建 MCP 服务器")
async def create_controller(
    data: McpCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_application:ai:create"]))
) -> JSONResponse:
    """
    创建 MCP 服务器接口
    
    参数:
    - data (McpCreateSchema): 创建 MCP 服务器模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含创建 MCP 服务器结果的 JSON 响应
    """
    result_dict = await McpService.create_service(auth=auth, data=data)
    log.info(f"创建 MCP 服务器成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建 MCP 服务器成功")


@AIRouter.put("/update/{id}", summary="修改 MCP 服务器", description="修改 MCP 服务器")
async def update_controller(
    data: McpUpdateSchema,
    id: int = Path(..., description="MCP ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_application:ai:update"]))
) -> JSONResponse:
    """
    修改 MCP 服务器接口
    
    参数:
    - data (McpUpdateSchema): 修改 MCP 服务器模型
    - id (int): MCP 服务器ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含修改 MCP 服务器结果的 JSON 响应
    """
    result_dict = await McpService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改 MCP 服务器成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改 MCP 服务器成功")


@AIRouter.delete("/delete", summary="删除 MCP 服务器", description="删除 MCP 服务器")
async def delete_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_application:ai:delete"]))
) -> JSONResponse:
    """
    删除 MCP 服务器接口
    
    参数:
    - ids (list[int]): MCP 服务器ID列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含删除 MCP 服务器结果的 JSON 响应
    """
    await McpService.delete_service(auth=auth, ids=ids)
    log.info(f"删除 MCP 服务器成功: {ids}")
    return SuccessResponse(msg="删除 MCP 服务器成功")
