from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema
from app.core.dependencies import AuthPermission, get_current_user
from app.core.router_class import OperationLogRoute

from .schema import (
    PackageAvailableOut,
    PackagePreviewOut,
    PluginPurchaseCreate,
    SelfOrderCreate,
    SelfOrderDetailOut,
    SelfOrderListOut,
    SelfOrderOut,
    WorkspaceOut,
)
from .service import SelfService

TenantSelfServiceRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/tenant",
    tags=["自助服务"],
)

@TenantSelfServiceRouter.get(
    "/package/available",
    summary="可选套餐列表",
    response_model=ResponseSchema[PackageAvailableOut],
)
async def package_available_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["tenant:package:query"]))],
) -> JSONResponse:
    result = await SelfService.get_available_packages(auth=auth, tenant_id=auth.tenant_id)
    return SuccessResponse(data=result, msg="查询成功")

@TenantSelfServiceRouter.get(
    "/package/preview",
    summary="套餐变更影响预览",
    response_model=ResponseSchema[PackagePreviewOut],
)
async def package_preview_controller(
    target_package_id: Annotated[int, Query(ge=1, description="目标套餐ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["tenant:package:query"]))],
) -> JSONResponse:
    result = await SelfService.preview_package_change(auth=auth, tenant_id=auth.tenant_id, target_package_id=target_package_id)
    return SuccessResponse(data=result, msg="查询成功")

@TenantSelfServiceRouter.post(
    "/order/create",
    summary="创建自助订单",
    response_model=ResponseSchema[SelfOrderOut],
)
async def order_create_controller(
    data: SelfOrderCreate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["tenant:order:create"]))],
) -> JSONResponse:
    result = await SelfService.create_self_order(auth=auth, tenant_id=auth.tenant_id, data=data)
    return SuccessResponse(data=result, msg="订单创建成功")

@TenantSelfServiceRouter.post(
    "/plugin/purchase",
    summary="购买付费插件",
    response_model=ResponseSchema[SelfOrderOut],
)
async def plugin_purchase_controller(
    data: PluginPurchaseCreate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["tenant:order:create"]))],
) -> JSONResponse:
    result = await SelfService.create_plugin_purchase_order(auth=auth, tenant_id=auth.tenant_id, data=data)
    return SuccessResponse(data=result, msg="插件订单创建成功")

@TenantSelfServiceRouter.get(
    "/order/list",
    summary="我的订单列表",
    response_model=ResponseSchema[SelfOrderListOut],
)
async def order_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["tenant:order:query"]))],
) -> JSONResponse:
    result = await SelfService.get_self_order_list(
        auth=auth,
        tenant_id=auth.tenant_id,
        page_no=page.page_no,
        page_size=page.page_size,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result, msg="查询成功")

@TenantSelfServiceRouter.get(
    "/order/detail/{order_id}",
    summary="订单详情",
    response_model=ResponseSchema[SelfOrderDetailOut],
)
async def order_detail_controller(
    order_id: Annotated[int, Path(ge=1, description="订单ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["tenant:order:query"]))],
) -> JSONResponse:
    result = await SelfService.get_self_order_detail(auth=auth, order_id=order_id)
    return SuccessResponse(data=result, msg="查询成功")

@TenantSelfServiceRouter.get(
    "/workspace",
    summary="租户工作台概览",
    response_model=ResponseSchema[WorkspaceOut],
)
async def tenant_workspace_controller(
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    result = await SelfService.get_workspace_data(auth=auth, tenant_id=auth.tenant_id)
    return SuccessResponse(data=result, msg="查询成功")
