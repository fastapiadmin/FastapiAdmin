from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchDelete, PageResultSchema
from app.core.dependencies import AuthPermission, get_current_user
from app.core.router_class import OperationLogRoute

from .schema import (
    LoginLogCreateSchema,
    LoginLogDetailOutSchema,
    LoginLogOutSchema,
    LoginLogQueryParam,
    OperationLogCreateSchema,
    OperationLogDetailOutSchema,
    OperationLogOutSchema,
    OperationLogQueryParam,
)
from .service import LoginLogService, OperationLogService

LogRouter = APIRouter(route_class=OperationLogRoute, prefix="/log", tags=["系统管理", "日志管理"])


@LogRouter.get(
    "/login/detail/{id}",
    summary="获取登录日志详情",
    response_model=ResponseSchema[LoginLogDetailOutSchema],
)
async def get_log_detail_controller(
    id: Annotated[int, Path(description="登录日志ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:login_log:query"]))],
) -> JSONResponse:
    result_dict = await LoginLogService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取登录日志详情成功")


@LogRouter.get(
    "/login/list",
    summary="查询登录日志列表",
    response_model=ResponseSchema[PageResultSchema[LoginLogOutSchema]],
)
async def get_log_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[LoginLogQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:login_log:query"]))],
) -> JSONResponse:
    result_dict = await LoginLogService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询登录日志列表成功")


@LogRouter.post(
    "/login/create",
    summary="创建登录日志",
    response_model=ResponseSchema[LoginLogDetailOutSchema],
)
async def create_log_controller(
    data: LoginLogCreateSchema,
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    result_dict = await LoginLogService(auth).create(data=data)
    return SuccessResponse(data=result_dict, msg="创建登录日志成功")


@LogRouter.delete(
    "/login/delete",
    summary="删除登录日志",
    response_model=ResponseSchema,
)
async def delete_log_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:login_log:delete"]))],
) -> JSONResponse:
    await LoginLogService(auth).delete(ids=ids)
    return SuccessResponse(msg="删除登录日志成功")


@LogRouter.get(
    "/operation/detail/{id}",
    summary="获取操作日志详情",
    response_model=ResponseSchema[OperationLogDetailOutSchema],
    dependencies=[Depends(AuthPermission(["module_system:log:query"]))],
)
async def get_operation_log_detail_controller(
    *,
    id: Annotated[int, Path(gt=0)],
    auth: Annotated[AuthSchema, Depends(get_current_user)],
):
    result_dict = await OperationLogService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取操作日志详情成功")


@LogRouter.get(
    "/operation/list",
    summary="获取操作日志列表",
    response_model=ResponseSchema[PageResultSchema[OperationLogOutSchema]],
    dependencies=[Depends(AuthPermission(["module_system:log:query"]))],
)
async def list(
    *,
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[OperationLogQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(get_current_user)],
):
    result_dict = await OperationLogService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询操作日志列表成功")


@LogRouter.post(
    "/operation/create",
    summary="创建操作日志",
    response_model=ResponseSchema[OperationLogDetailOutSchema],
)
async def create_operation_log_controller(
    *,
    data: OperationLogCreateSchema,
    auth: Annotated[AuthSchema, Depends(get_current_user)],
):
    result_dict = await OperationLogService(auth).create(data=data)
    return SuccessResponse(data=result_dict, msg="创建操作日志成功")


@LogRouter.delete(
    "/operation/delete",
    summary="删除操作日志",
    response_model=ResponseSchema,
    dependencies=[Depends(AuthPermission(["module_system:log:delete"]))],
)
async def delete(
    *,
    data: BatchDelete,
    auth: Annotated[AuthSchema, Depends(get_current_user)],
):
    await OperationLogService(auth).delete(ids=data.ids)
    return SuccessResponse(msg="删除操作日志成功")
