from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    ChatMessageCreateSchema,
    ChatMessageOutSchema,
    ChatMessageQueryParam,
    ChatMessageUpdateSchema,
)
from .service import ChatMessageService

ChatMessageRouter = APIRouter(route_class=OperationLogRoute, prefix="/chat_message", tags=["AI模块"])


@ChatMessageRouter.get(
    "/detail/{id}",
    summary="获取聊天消息详情",
    description="获取聊天消息详情",
    response_model=ResponseSchema[ChatMessageOutSchema],
)
async def get_message_detail_controller(
    id: Annotated[int, Path(description="消息ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_message:detail"]))],
) -> JSONResponse:
    """
    获取聊天消息详情

    参数:
    - id (int): 消息ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含消息详情的JSON响应
    """
    result_dict = await ChatMessageService.detail_service(id=id, auth=auth)
    log.info(f"获取聊天消息详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取聊天消息详情成功")


@ChatMessageRouter.get(
    "/list",
    summary="查询聊天消息列表",
    description="查询聊天消息列表",
    response_model=ResponseSchema[list[ChatMessageOutSchema]],
)
async def get_message_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ChatMessageQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_message:query"]))],
) -> JSONResponse:
    """
    查询聊天消息列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (ChatMessageQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含消息列表分页信息的JSON响应
    """
    result_dict = await ChatMessageService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询聊天消息列表成功")
    return SuccessResponse(data=result_dict, msg="查询聊天消息列表成功")


@ChatMessageRouter.get(
    "/session/{session_id}",
    summary="按会话ID获取聊天消息",
    description="按会话ID获取聊天消息",
    response_model=ResponseSchema[list[ChatMessageOutSchema]],
)
async def get_message_by_session_id_controller(
    session_id: Annotated[int, Path(description="会话ID")],
    page: Annotated[PaginationQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_message:query"]))],
) -> JSONResponse:
    """
    按会话ID获取聊天消息

    参数:
    - session_id (int): 会话ID
    - page (PaginationQueryParam): 分页查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含消息列表分页信息的JSON响应
    """
    result_dict = await ChatMessageService.get_by_session_id_service(
        auth=auth,
        session_id=session_id,
        page_no=page.page_no,
        page_size=page.page_size,
    )
    log.info(f"按会话ID获取聊天消息成功: {session_id}")
    return SuccessResponse(data=result_dict, msg="按会话ID获取聊天消息成功")


@ChatMessageRouter.post(
    "/create",
    summary="创建聊天消息",
    description="创建聊天消息",
    response_model=ResponseSchema[ChatMessageOutSchema],
)
async def create_message_controller(
    data: ChatMessageCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_message:create"]))],
) -> JSONResponse:
    """
    创建聊天消息

    参数:
    - data (ChatMessageCreateSchema): 消息创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建消息详情的JSON响应
    """
    result_dict = await ChatMessageService.create_service(auth=auth, data=data)
    content = result_dict.get('content', '')[:50] if result_dict.get('content') else ''
    log.info(f"创建聊天消息成功: {content}...")
    return SuccessResponse(data=result_dict, msg="创建聊天消息成功")


@ChatMessageRouter.put(
    "/update/{id}",
    summary="修改聊天消息",
    description="修改聊天消息",
    response_model=ResponseSchema[ChatMessageOutSchema],
)
async def update_message_controller(
    data: ChatMessageUpdateSchema,
    id: Annotated[int, Path(description="消息ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_message:update"]))],
) -> JSONResponse:
    """
    修改聊天消息

    参数:
    - data (ChatMessageUpdateSchema): 消息更新模型
    - id (int): 消息ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含修改消息详情的JSON响应
    """
    result_dict = await ChatMessageService.update_service(auth=auth, id=id, data=data)
    content = result_dict.get('content', '')[:50] if result_dict.get('content') else ''
    log.info(f"修改聊天消息成功: {content}...")
    return SuccessResponse(data=result_dict, msg="修改聊天消息成功")


@ChatMessageRouter.delete(
    "/delete",
    summary="删除聊天消息",
    description="删除聊天消息",
    response_model=ResponseSchema[None],
)
async def delete_message_controller(
    ids: Annotated[list[int], Body(description="消息ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_message:delete"]))],
) -> JSONResponse:
    """
    删除聊天消息

    参数:
    - ids (list[int]): 消息ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除消息详情的JSON响应
    """
    await ChatMessageService.delete_service(auth=auth, ids=ids)
    log.info(f"删除聊天消息成功: {ids}")
    return SuccessResponse(msg="删除聊天消息成功")
