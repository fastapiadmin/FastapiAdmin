from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.dependencies import AuthPermission, db_getter
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.router_class import OperationLogRoute

from .schema import (
    OrderCreateSchema,
    OrderOutSchema,
    OrderQueryParam,
    OrderStatusMessage,
    PaymentCreateOut,
    PaymentRecordOutSchema,
    PaymentStatusOut,
    RefundApplySchema,
    RefundOutSchema,
    RefundReviewSchema,
)
from .service import OrderService, PaymentService, RefundService

OrderRouter = APIRouter(route_class=OperationLogRoute, prefix="/order", tags=["平台管理", "订单管理"])
PaymentRouter = APIRouter(route_class=OperationLogRoute, prefix="/payment", tags=["平台管理", "支付管理"])
RefundRouter = APIRouter(route_class=OperationLogRoute, prefix="/refund", tags=["平台管理", "退款管理"])
TenantOrderRouter = APIRouter(route_class=OperationLogRoute, prefix="/order", tags=["平台管理", "租户订单"])

@OrderRouter.post(
    "/create",
    summary="创建订单",
    response_model=ResponseSchema[OrderOutSchema],
)
async def order_create_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:order:create"]))],
    data: Annotated[OrderCreateSchema, Body(description="订单创建参数")],
) -> JSONResponse:
    result = await OrderService.create_order(auth=auth, data=data)
    return SuccessResponse(data=result, msg="订单创建成功")

@OrderRouter.get(
    "/detail/{order_id}",
    summary="订单详情",
    response_model=ResponseSchema[OrderOutSchema],
)
async def order_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:order:query"]))],
    order_id: Annotated[int, Path(description="订单ID", ge=1)],
) -> JSONResponse:
    order = await OrderService.get_detail(auth=auth, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return SuccessResponse(data=order)

@OrderRouter.get(
    "/list",
    summary="订单列表",
    response_model=ResponseSchema[PageResultSchema[OrderOutSchema]],
)
async def order_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:order:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[OrderQueryParam, Query(description="查询参数")],
) -> JSONResponse:
    items, total = await OrderService.get_list(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        order_by=page.order_by,
        search=search,
    )
    offset = (page.page_no - 1) * page.page_size
    result = PageResultSchema(
        page_no=page.page_no,
        page_size=page.page_size,
        total=total,
        has_next=offset + page.page_size < total,
        items=items,
    )
    return SuccessResponse(data=result)

@OrderRouter.post(
    "/cancel/{order_id}",
    summary="取消订单",
    response_model=ResponseSchema[OrderStatusMessage],
)
async def order_cancel_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:order:update"]))],
    order_id: Annotated[int, Path(description="订单ID", ge=1)],
) -> JSONResponse:
    result = await OrderService.cancel_order(auth=auth, order_id=order_id)
    return SuccessResponse(data=result, msg=result["message"])

@PaymentRouter.post(
    "/pay/{order_id}",
    summary="创建支付（获取支付 URL/二维码）",
    response_model=ResponseSchema[PaymentCreateOut],
)
async def payment_create_controller(
    request: Request,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:order:update"]))],
    order_id: Annotated[int, Path(description="订单ID", ge=1)],
    method: Annotated[str, Query(description="支付渠道: alipay / wxpay(留空=自动)")] = "",
) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")
    result = await PaymentService.create_payment(auth=auth, order_id=order_id, method=method, notify_base_url=base_url)
    return SuccessResponse(data=result, msg="支付信息已生成")

@PaymentRouter.get(
    "/status/{order_id}",
    summary="查询支付状态（供前端轮询）",
    response_model=ResponseSchema[PaymentStatusOut],
)
async def payment_status_controller(
    db: Annotated[AsyncSession, Depends(db_getter)],
    order_id: Annotated[int, Path(description="订单ID", ge=1)],
) -> JSONResponse:
    auth = AuthSchema(db=db, check_data_scope=False)
    result = await OrderService.check_payment_status(auth=auth, order_id=order_id)
    return SuccessResponse(data=result)

@PaymentRouter.post(
    "/callback/{method}",
    summary="支付回调（统一入口）",
    response_model=ResponseSchema[dict],
)
async def payment_callback_controller(
    db: Annotated[AsyncSession, Depends(db_getter)],
    method: Annotated[str, Path(description="支付渠道: alipay / wxpay / mock")],
    data: Annotated[dict, Body(description="支付回调数据")],
) -> JSONResponse:
    try:
        auth = AuthSchema(db=db, check_data_scope=False)
        result = await PaymentService.handle_callback(auth=auth, method=method, callback_data=data)
        logger.info(f"支付回调处理成功: {result}")
        return SuccessResponse(data=result)
    except CustomException as e:
        logger.warning(f"支付回调处理失败: {e}")
        return SuccessResponse(data={"message": str(e)}, code=400)

@PaymentRouter.post(
    "/mock/callback",
    summary="Mock 支付回调（开发环境触发模拟支付）",
    response_model=ResponseSchema[dict],
)
async def payment_mock_callback_controller(
    db: Annotated[AsyncSession, Depends(db_getter)],
    order_id: Annotated[int, Body(description="订单ID", ge=1)],
) -> JSONResponse:
    from app.utils.payment import get_mock_gateway

    from .crud import OrderCRUD

    auth = AuthSchema(db=db, check_data_scope=False)
    order = await OrderCRUD(auth).get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    mock_gw = get_mock_gateway()
    callback_data = mock_gw.get_mock_callback_data(order.id, order.order_no)
    result = await PaymentService.handle_callback(auth=auth, method="mock", callback_data=callback_data)
    logger.info(f"Mock 支付回调触发: order_id={order_id}")
    return SuccessResponse(data=result, msg="模拟支付成功")

@PaymentRouter.get(
    "/record/list",
    summary="支付记录列表",
    response_model=ResponseSchema[PageResultSchema[PaymentRecordOutSchema]],
)
async def payment_record_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:order:query"]))],
    page: Annotated[int, Query(description="页码", ge="页码，从1开始")] = 1,
    page_size: Annotated[int, Query(description="每页数量", ge="每页数量，范围1-100，默认1", le="每页数量，范围1-100，默认100")] = 20,
) -> JSONResponse:
    offset = (page - 1) * page_size
    items, total = await PaymentService.get_records(auth=auth, offset=offset, limit=page_size)
    result = PageResultSchema(
        page_no=page,
        page_size=page_size,
        total=total,
        has_next=offset + page_size < total,
        items=items,
    )
    return SuccessResponse(data=result)

@RefundRouter.get(
    "/list",
    summary="退款审核列表",
    response_model=ResponseSchema[PageResultSchema[RefundOutSchema]],
)
async def refund_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:order:query"]))],
    status: Annotated[int | None, Query(description="状态筛选")] = None,
    page: Annotated[int, Query(description="页码", ge="页码，从1开始")] = 1,
    page_size: Annotated[int, Query(description="每页数量", ge="每页数量，范围1-100，默认1", le="每页数量，范围1-100，默认100")] = 20,
) -> JSONResponse:
    offset = (page - 1) * page_size
    items, total = await RefundService.get_list(auth=auth, status=status, offset=offset, limit=page_size)
    result = PageResultSchema(
        page_no=page,
        page_size=page_size,
        total=total,
        has_next=offset + page_size < total,
        items=items,
    )
    return SuccessResponse(data=result)

@RefundRouter.put(
    "/approve/{refund_id}",
    summary="批准退款",
    response_model=ResponseSchema[OrderStatusMessage],
)
async def refund_approve_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:order:update"]))],
    refund_id: Annotated[int, Path(description="退款ID", ge=1)],
) -> JSONResponse:
    result = await RefundService.approve(
        auth=auth,
        refund_id=refund_id,
        reviewer_id=auth.user.id if auth.user else 0,
        operator_name=auth.user.name if auth.user else "",
    )
    return SuccessResponse(data=result, msg=result["message"])

@RefundRouter.put(
    "/reject/{refund_id}",
    summary="驳回退款",
    response_model=ResponseSchema[OrderStatusMessage],
)
async def refund_reject_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:order:update"]))],
    refund_id: Annotated[int, Path(description="退款ID", ge=1)],
    data: Annotated[RefundReviewSchema, Body(description="退款驳回数据")],
) -> JSONResponse:
    result = await RefundService.reject(
        auth=auth,
        refund_id=refund_id,
        reviewer_id=auth.user.id if auth.user else 0,
        data=data,
        operator_name=auth.user.name if auth.user else "",
    )
    return SuccessResponse(data=result, msg=result["message"])

@TenantOrderRouter.post(
    "/create",
    summary="租户端创建订单",
    response_model=ResponseSchema[OrderOutSchema],
)
async def tenant_order_create_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["tenant:order:create"]))],
    data: Annotated[OrderCreateSchema, Body(description="订单创建数据")],
) -> JSONResponse:
    if data.tenant_id != auth.tenant_id:
        raise HTTPException(status_code=403, detail="无权操作")
    result = await OrderService.create_order(auth=auth, data=data)
    return SuccessResponse(data=result, msg="订单创建成功")

@TenantOrderRouter.post(
    "/refund/apply/{order_id}",
    summary="申请退款",
    response_model=ResponseSchema[RefundOutSchema],
)
async def tenant_refund_apply_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["tenant:order:refund"]))],
    order_id: Annotated[int, Path(description="订单ID", ge=1)],
    data: Annotated[RefundApplySchema, Body(description="退款申请数据")],
) -> JSONResponse:
    result = await RefundService.apply(auth=auth, data=data, order_id=order_id)
    return SuccessResponse(data=result, msg="退款申请已提交")
