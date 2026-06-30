from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import (
    RoleCreateSchema,
    RoleOutSchema,
    RolePermissionSettingSchema,
    RoleQueryParam,
    RoleUpdateSchema,
)
from .service import RoleService

RoleRouter = APIRouter(route_class=OperationLogRoute, prefix="/role", tags=["系统管理", "角色管理"])

_ROLE_NS = "role"

@RoleRouter.get(
    "/list",
    summary="查询角色",
    response_model=ResponseSchema[PageResultSchema[RoleOutSchema]],
)
@cache(expire=300, namespace=_ROLE_NS)
async def get_role_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[RoleQueryParam, Query(description="角色查询参数")],
) -> JSONResponse:
    order_by = [{"order": "asc"}]
    if page.order_by:
        order_by = page.order_by
    result_dict = await RoleService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询角色成功")

@RoleRouter.get(
    "/detail/{id}",
    summary="查询角色详情",
    response_model=ResponseSchema[RoleOutSchema],
)
async def get_role_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:detail"]))],
    id: Annotated[int, Path(description="角色ID")],
) -> JSONResponse:
    result_dict = await RoleService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取角色详情成功")

@RoleRouter.post(
    "/create",
    summary="创建角色",
    response_model=ResponseSchema[RoleOutSchema],
)
async def create_role_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:create"]))],
    data: Annotated[RoleCreateSchema, Body(description="角色创建参数")],
) -> JSONResponse:
    result_dict = await RoleService(auth).create(data=data)
    await FastAPICache.clear(namespace=_ROLE_NS)
    return SuccessResponse(data=result_dict, msg="创建角色成功")

@RoleRouter.put(
    "/update/{id}",
    summary="修改角色",
    response_model=ResponseSchema[RoleOutSchema],
)
async def update_role_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:update"]))],
    id: Annotated[int, Path(description="角色ID")],
    data: Annotated[RoleUpdateSchema, Body(description="角色修改参数")],
) -> JSONResponse:
    result_dict = await RoleService(auth).update(id=id, data=data)
    await FastAPICache.clear(namespace=_ROLE_NS)
    return SuccessResponse(data=result_dict, msg="修改角色成功")

@RoleRouter.delete(
    "/delete",
    summary="删除角色",
    response_model=ResponseSchema[None],
)
async def delete_role_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    await RoleService(auth).delete(ids=ids)
    await FastAPICache.clear(namespace=_ROLE_NS)
    return SuccessResponse(msg="删除角色成功")

@RoleRouter.patch(
    "/status/batch",
    summary="批量修改角色状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_role_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:patch"]))],
    data: Annotated[BatchSetAvailable, Body(description="批量修改角色状态参数")],
) -> JSONResponse:
    await RoleService(auth).set_available(data=data)
    await FastAPICache.clear(namespace=_ROLE_NS)
    return SuccessResponse(msg="批量修改角色状态成功")

@RoleRouter.put(
    "/permission",
    summary="角色授权",
    response_model=ResponseSchema[None],
)
async def set_role_permission_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:permission"]))],
    data: Annotated[RolePermissionSettingSchema, Body(description="角色授权参数")],
) -> JSONResponse:
    await RoleService(auth).set_permission(data=data)
    await FastAPICache.clear(namespace=_ROLE_NS)
    return SuccessResponse(msg="授权角色成功")

@RoleRouter.get(
    "/export",
    summary="导出角色",
    response_model=ResponseSchema[None],
)
async def export_role_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:export"]))],
    search: Annotated[RoleQueryParam, Query(description="角色查询参数")],
) -> StreamingResponse:
    role_query_result = await RoleService(auth).get_list(search=search)
    role_export_result = RoleService.export_list(role_list=role_query_result)

    return StreamResponse(
        data=bytes2file_response(role_export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=role.xlsx"},
    )
