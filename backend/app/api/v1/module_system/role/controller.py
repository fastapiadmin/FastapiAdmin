from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core import cache_util
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.cache_util import cache
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
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[RoleQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:query"]))],
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
    id: Annotated[int, Path(description="角色ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:detail"]))],
) -> JSONResponse:
    result_dict = await RoleService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取角色详情成功")

@RoleRouter.post(
    "/create",
    summary="创建角色",
    response_model=ResponseSchema[RoleOutSchema],
)
async def create_role_controller(
    data: RoleCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:create"]))],
) -> JSONResponse:
    result_dict = await RoleService(auth).create(data=data)
    await cache_util.clear(namespace=_ROLE_NS)
    return SuccessResponse(data=result_dict, msg="创建角色成功")

@RoleRouter.put(
    "/update/{id}",
    summary="修改角色",
    response_model=ResponseSchema[RoleOutSchema],
)
async def update_role_controller(
    data: RoleUpdateSchema,
    id: Annotated[int, Path(description="角色ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:update"]))],
) -> JSONResponse:
    result_dict = await RoleService(auth).update(id=id, data=data)
    await cache_util.clear(namespace=_ROLE_NS)
    return SuccessResponse(data=result_dict, msg="修改角色成功")

@RoleRouter.delete(
    "/delete",
    summary="删除角色",
    response_model=ResponseSchema[None],
)
async def delete_role_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:delete"]))],
) -> JSONResponse:
    await RoleService(auth).delete(ids=ids)
    await cache_util.clear(namespace=_ROLE_NS)
    return SuccessResponse(msg="删除角色成功")

@RoleRouter.patch(
    "/status/batch",
    summary="批量修改角色状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_role_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:patch"]))],
) -> JSONResponse:
    await RoleService(auth).set_available(data=data)
    await cache_util.clear(namespace=_ROLE_NS)
    return SuccessResponse(msg="批量修改角色状态成功")

@RoleRouter.put(
    "/permission",
    summary="角色授权",
    response_model=ResponseSchema[None],
)
async def set_role_permission_controller(
    data: RolePermissionSettingSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:permission"]))],
) -> JSONResponse:
    await RoleService(auth).set_permission(data=data)
    await cache_util.clear(namespace=_ROLE_NS)
    return SuccessResponse(msg="授权角色成功")

@RoleRouter.get(
    "/export",
    summary="导出角色",
    response_model=ResponseSchema[None],
)
async def export_role_list_controller(
    search: Annotated[RoleQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:export"]))],
) -> StreamingResponse:
    role_query_result = await RoleService(auth).get_list(search=search)
    role_export_result = RoleService.export_list(role_list=role_query_result)

    return StreamResponse(
        data=bytes2file_response(role_export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=role.xlsx"},
    )
