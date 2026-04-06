from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchSetAvailable
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import TenantCreateSchema, TenantOutSchema, TenantQueryParam, TenantUpdateSchema
from .service import TenantService

TenantRouter = APIRouter(route_class=OperationLogRoute, prefix="/tenant", tags=["租户管理"])


@TenantRouter.get(
    "/detail/{id}",
    summary="获取租户详情",
    description="获取租户详情",
    response_model=ResponseSchema[TenantOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="租户ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:query"]))],
) -> JSONResponse:
    result_dict = await TenantService.detail_service(id=id, auth=auth)
    log.info(f"获取租户详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取租户详情成功")


@TenantRouter.get(
    "/list",
    summary="查询租户列表",
    description="查询租户列表（分页）",
    response_model=ResponseSchema[dict],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[TenantQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:query"]))],
) -> JSONResponse:
    order_by = [{"id": "asc"}]
    if page.order_by:
        order_by = page.order_by
    result_dict = await TenantService.page_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=order_by,
    )
    log.info("查询租户列表成功")
    return SuccessResponse(data=result_dict, msg="查询租户列表成功")


@TenantRouter.post(
    "/create",
    summary="创建租户",
    description="创建租户",
    response_model=ResponseSchema[TenantOutSchema],
)
async def create_obj_controller(
    data: TenantCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:create"]))],
) -> JSONResponse:
    result_dict = await TenantService.create_service(auth=auth, data=data)
    log.info(f"创建租户成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="创建租户成功")


@TenantRouter.put(
    "/update/{id}",
    summary="修改租户",
    description="修改租户",
    response_model=ResponseSchema[TenantOutSchema],
)
async def update_obj_controller(
    data: TenantUpdateSchema,
    id: Annotated[int, Path(description="租户ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:update"]))],
) -> JSONResponse:
    result_dict = await TenantService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改租户成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="修改租户成功")


@TenantRouter.delete(
    "/delete",
    summary="删除租户",
    description="删除租户",
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(..., description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:delete"]))],
) -> JSONResponse:
    await TenantService.delete_service(auth=auth, ids=ids)
    log.info(f"删除租户成功: {ids}")
    return SuccessResponse(msg="删除租户成功")


@TenantRouter.patch(
    "/available/setting",
    summary="批量修改租户状态",
    description="批量修改租户状态",
)
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:tenant:patch"]))],
) -> JSONResponse:
    await TenantService.set_available_service(auth=auth, data=data)
    log.info(f"批量修改租户状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改租户状态成功")
