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
    ChatSessionCreateSchema,
    ChatSessionOutSchema,
    ChatSessionQueryParam,
    ChatSessionUpdateSchema,
)
from .service import ChatSessionService

ChatSessionRouter = APIRouter(route_class=OperationLogRoute, prefix="/chat_session", tags=["AI模块"])


@ChatSessionRouter.get(
    "/detail/{id}",
    summary="获取聊天会话详情",
    description="获取聊天会话详情",
    response_model=ResponseSchema[ChatSessionOutSchema],
)
async def get_session_detail_controller(
    id: Annotated[int, Path(description="会话ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_session:detail"]))],
) -> JSONResponse:
    """
    获取聊天会话详情

    参数:
    - id (str): 会话ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含会话详情的JSON响应
    """
    result_dict = await ChatSessionService.detail_service(id=id, auth=auth)
    log.info(f"获取聊天会话详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取聊天会话详情成功")


@ChatSessionRouter.get(
    "/list",
    summary="查询聊天会话列表",
    description="查询聊天会话列表",
    response_model=ResponseSchema[list[ChatSessionOutSchema]],
)
async def get_session_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ChatSessionQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_session:query"]))],
) -> JSONResponse:
    """
    查询聊天会话列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (ChatSessionQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含会话列表分页信息的JSON响应
    """
    result_dict = await ChatSessionService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询聊天会话列表成功")
    return SuccessResponse(data=result_dict, msg="查询聊天会话列表成功")


@ChatSessionRouter.post(
    "/create",
    summary="创建聊天会话",
    description="创建聊天会话",
    response_model=ResponseSchema[ChatSessionOutSchema],
)
async def create_session_controller(
    data: ChatSessionCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_session:create"]))],
) -> JSONResponse:
    """
    创建聊天会话

    参数:
    - data (ChatSessionCreateSchema): 会话创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建会话详情的JSON响应
    """
    result_dict = await ChatSessionService.create_service(auth=auth, data=data)
    log.info(f"创建聊天会话成功: {result_dict.get('title')}")
    return SuccessResponse(data=result_dict, msg="创建聊天会话成功")


@ChatSessionRouter.put(
    "/update/{id}",
    summary="修改聊天会话",
    description="修改聊天会话",
    response_model=ResponseSchema[ChatSessionOutSchema],
)
async def update_session_controller(
    data: ChatSessionUpdateSchema,
    id: Annotated[int, Path(description="会话ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_session:update"]))],
) -> JSONResponse:
    """
    修改聊天会话

    参数:
    - data (ChatSessionUpdateSchema): 会话更新模型
    - id (int): 会话ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含修改会话详情的JSON响应
    """
    result_dict = await ChatSessionService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改聊天会话成功: {result_dict.get('title')}")
    return SuccessResponse(data=result_dict, msg="修改聊天会话成功")


@ChatSessionRouter.delete(
    "/delete",
    summary="删除聊天会话",
    description="删除聊天会话",
    response_model=ResponseSchema[None],
)
async def delete_session_controller(
    ids: Annotated[list[int], Body(description="会话ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ai:chat_session:delete"]))],
) -> JSONResponse:
    """
    删除聊天会话

    参数:
    - ids (list[int]): 会话ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除会话详情的JSON响应
    """
    await ChatSessionService.delete_service(auth=auth, ids=ids)
    log.info(f"删除聊天会话成功: {ids}")
    return SuccessResponse(msg="删除聊天会话成功")
