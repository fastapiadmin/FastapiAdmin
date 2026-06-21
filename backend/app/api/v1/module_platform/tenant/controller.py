from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse
from redis.asyncio.client import Redis

from app.common.response import ResponseSchema, SuccessResponse
from app.core import cache_util
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.cache_util import cache
from app.core.dependencies import AuthPermission, redis_getter
from app.core.router_class import OperationLogRoute

from .schema import (
    PackageChangePreviewOut,
    TenantConfigItem,
    TenantConfigOutSchema,
    TenantCreateSchema,
    TenantOutSchema,
    TenantQueryParam,
    TenantRenewSchema,
    TenantUpdateSchema,
    TenantUserAddSchema,
    TenantUserOutSchema,
)
from .service import TenantService

TenantRouter = APIRouter(route_class=OperationLogRoute, prefix="/tenant", tags=["平台管理", "租户管理"])

_TENANT_NS = "tenant"

@TenantRouter.get(
    "/detail/{id}",
    summary="获取租户详情",
    response_model=ResponseSchema[TenantOutSchema],
)
@cache(expire=120, namespace=_TENANT_NS)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="租户ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:query"]))],
) -> JSONResponse:
    result_dict = await TenantService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取租户详情成功")

@TenantRouter.get(
    "/list",
    summary="查询租户列表",
    response_model=ResponseSchema[PageResultSchema[TenantOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[TenantQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:query"]))],
) -> JSONResponse:
    order_by = [{"id": "asc"}]
    if page.order_by:
        order_by = page.order_by
    result_dict = await TenantService(auth).page(
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询租户列表成功")

@TenantRouter.post(
    "/create",
    summary="创建租户",
    response_model=ResponseSchema[TenantOutSchema],
)
async def create_obj_controller(
    data: TenantCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:create"]))],
) -> JSONResponse:
    result_dict = await TenantService(auth).create(data=data)
    await cache_util.clear(namespace=_TENANT_NS)
    return SuccessResponse(data=result_dict, msg="创建租户成功")

@TenantRouter.put(
    "/update/{id}",
    summary="修改租户",
    response_model=ResponseSchema[TenantOutSchema],
)
async def update_obj_controller(
    data: TenantUpdateSchema,
    id: Annotated[int, Path(description="租户ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:update"]))],
) -> JSONResponse:
    result_dict = await TenantService(auth).update(id=id, data=data)
    await cache_util.clear(namespace=_TENANT_NS)
    return SuccessResponse(data=result_dict, msg="修改租户成功")

@TenantRouter.delete(
    "/delete",
    summary="删除租户",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(..., description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:delete"]))],
) -> JSONResponse:
    await TenantService(auth).delete(ids=ids)
    await cache_util.clear(namespace=_TENANT_NS)
    return SuccessResponse(msg="删除租户成功")

@TenantRouter.patch(
    "/status/batch",
    summary="批量修改租户状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:patch"]))],
) -> JSONResponse:
    await TenantService(auth).set_available(data=data)
    await cache_util.clear(namespace=_TENANT_NS)
    return SuccessResponse(msg="批量修改租户状态成功")

@TenantRouter.put(
    "/status/{id}",
    summary="启/禁用租户",
    response_model=ResponseSchema[None],
)
async def toggle_tenant_status_controller(
    id: Annotated[int, Path(description="租户ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:patch"]))],
) -> JSONResponse:
    await TenantService(auth).toggle_status(id=id)
    await cache_util.clear(namespace=_TENANT_NS)
    return SuccessResponse(msg="修改租户状态成功")

@TenantRouter.get(
    "/{id}/users",
    summary="获取租户用户列表",
    response_model=ResponseSchema[list[TenantUserOutSchema]],
)
@cache(expire=120, namespace=_TENANT_NS)
async def get_tenant_users_controller(
    id: Annotated[int, Path(description="租户ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:query"]))],
) -> JSONResponse:
    result = await TenantService(auth).get_tenant_users(tenant_id=id)
    return SuccessResponse(data=result, msg="获取租户用户列表成功")

@TenantRouter.post(
    "/{id}/users",
    summary="向租户添加用户",
    response_model=ResponseSchema[None],
)
async def add_tenant_user_controller(
    id: Annotated[int, Path(description="租户ID")],
    data: TenantUserAddSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:create"]))],
) -> JSONResponse:
    await TenantService(auth).add_tenant_user(tenant_id=id, data=data)
    await cache_util.clear(namespace=_TENANT_NS)
    return SuccessResponse(msg="添加用户成功")

@TenantRouter.delete(
    "/{id}/users/{uid}",
    summary="从租户移除用户",
    response_model=ResponseSchema[None],
)
async def remove_tenant_user_controller(
    id: Annotated[int, Path(description="租户ID")],
    uid: Annotated[int, Path(description="用户ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:delete"]))],
) -> JSONResponse:
    await TenantService(auth).remove_tenant_user(tenant_id=id, user_id=uid)
    await cache_util.clear(namespace=_TENANT_NS)
    return SuccessResponse(msg="移除用户成功")

@TenantRouter.get(
    "/{id}/config",
    summary="获取租户配置",
    response_model=ResponseSchema[list[TenantConfigOutSchema]],
)
async def get_tenant_config_controller(
    id: Annotated[int, Path(description="租户ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:query"]))],
) -> JSONResponse:
    result = await TenantService(auth).get_config_items(tenant_id=id)
    return SuccessResponse(data=result, msg="获取租户配置成功")

@TenantRouter.get(
    "/{id}/config/info",
    summary="获取租户配置（公开-缓存）",
    response_model=ResponseSchema[list[TenantConfigOutSchema]],
)
async def get_tenant_config_info_controller(
    id: Annotated[int, Path(description="租户ID")],
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    result = await TenantService.get_config_cache_items(redis=redis, tenant_id=id)
    return SuccessResponse(data=result, msg="获取租户配置成功")

@TenantRouter.put(
    "/{id}/config",
    summary="更新租户配置",
    response_model=ResponseSchema[list[TenantConfigOutSchema]],
)
async def update_tenant_config_controller(
    id: Annotated[int, Path(description="租户ID")],
    data: Annotated[list[TenantConfigItem], Body(..., description="配置项列表")],
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:update"]))],
) -> JSONResponse:
    result = await TenantService(auth).update_config(redis=redis, tenant_id=id, config=data)
    await cache_util.clear(namespace=_TENANT_NS)
    return SuccessResponse(data=result, msg="更新租户配置成功")

@TenantRouter.put(
    "/renew/{id}",
    summary="租户续期",
    response_model=ResponseSchema[TenantOutSchema],
)
async def renew_tenant_controller(
    id: Annotated[int, Path(description="租户ID")],
    data: TenantRenewSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:update"]))],
) -> JSONResponse:
    result = await TenantService(auth).renew(tenant_id=id, end_time=data.end_time)
    await cache_util.clear(namespace=_TENANT_NS)
    return SuccessResponse(data=result, msg="租户续期成功")

@TenantRouter.get(
    "/{id}/package-change-preview",
    summary="套餐变更影响预览",
    response_model=ResponseSchema[PackageChangePreviewOut],
)
async def package_change_preview_controller(
    id: Annotated[int, Path(description="租户ID")],
    new_package_id: Annotated[int, Query(..., description="目标套餐ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:query"]))],
) -> JSONResponse:
    result = await TenantService(auth).package_change_preview(tenant_id=id, new_package_id=new_package_id)
    return SuccessResponse(data=result, msg="套餐变更预览成功")
