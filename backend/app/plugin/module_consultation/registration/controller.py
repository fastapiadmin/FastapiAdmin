"""
咨询会报名管理 - 控制器
"""
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
    RegistrationApproveSchema,
    RegistrationCreateSchema,
    RegistrationOutSchema,
    RegistrationPaySchema,
    RegistrationQuerySchema,
    RegistrationRejectSchema,
    RegistrationUpdateSchema,
)
from .service import RegistrationService

RegistrationRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/registration",
    tags=["招生咨询会 - 报名管理"],
)


@RegistrationRouter.get(
    "/detail/{id}",
    summary="获取报名详情",
    description="获取报名详情",
    response_model=ResponseSchema[RegistrationOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="报名ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:detail"]))],
) -> JSONResponse:
    """获取报名详情"""
    result_dict = await RegistrationService.detail_service(auth=auth, id=id)
    log.info(f"获取报名详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@RegistrationRouter.get(
    "/list",
    summary="查询报名列表",
    description="查询报名列表",
    response_model=ResponseSchema[list[RegistrationOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[RegistrationQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:query"]))],
) -> JSONResponse:
    """查询报名列表"""
    result_dict = await RegistrationService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询报名列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@RegistrationRouter.post(
    "/create",
    summary="创建报名",
    description="创建报名",
    response_model=ResponseSchema[RegistrationOutSchema],
)
async def create_obj_controller(
    data: RegistrationCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:create"]))],
) -> JSONResponse:
    """创建报名"""
    result_dict = await RegistrationService.create_service(auth=auth, data=data)
    log.info(f"创建报名成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@RegistrationRouter.put(
    "/update/{id}",
    summary="更新报名",
    description="更新报名",
    response_model=ResponseSchema[RegistrationOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="报名ID")],
    data: RegistrationUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:update"]))],
) -> JSONResponse:
    """更新报名"""
    result_dict = await RegistrationService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新报名成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@RegistrationRouter.delete(
    "/delete/{id}",
    summary="删除报名",
    description="删除报名",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="报名ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:delete"]))],
) -> JSONResponse:
    """删除报名"""
    await RegistrationService.delete_service(auth=auth, id=id)
    log.info(f"删除报名成功 {id}")
    return SuccessResponse(msg="删除成功")


@RegistrationRouter.delete(
    "/batch-delete",
    summary="批量删除报名",
    description="批量删除报名",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:delete"]))],
) -> JSONResponse:
    """批量删除报名"""
    await RegistrationService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除报名成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@RegistrationRouter.post(
    "/approve/{id}",
    summary="审核通过",
    description="审核通过报名",
    response_model=ResponseSchema[RegistrationOutSchema],
)
async def approve_controller(
    id: Annotated[int, Path(description="报名ID")],
    data: RegistrationApproveSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:approve"]))],
) -> JSONResponse:
    """审核通过"""
    result_dict = await RegistrationService.approve_service(auth=auth, id=id, data=data)
    log.info(f"审核通过报名 {id}")
    return SuccessResponse(data=result_dict, msg="审核通过")


@RegistrationRouter.post(
    "/reject/{id}",
    summary="审核拒绝",
    description="审核拒绝报名",
    response_model=ResponseSchema[RegistrationOutSchema],
)
async def reject_controller(
    id: Annotated[int, Path(description="报名ID")],
    data: RegistrationRejectSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:approve"]))],
) -> JSONResponse:
    """审核拒绝"""
    result_dict = await RegistrationService.reject_service(auth=auth, id=id, data=data)
    log.info(f"审核拒绝报名 {id}")
    return SuccessResponse(data=result_dict, msg="审核拒绝")


@RegistrationRouter.post(
    "/cancel/{id}",
    summary="取消报名",
    description="取消报名",
    response_model=ResponseSchema[RegistrationOutSchema],
)
async def cancel_controller(
    id: Annotated[int, Path(description="报名ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:update"]))],
    reason: Annotated[str | None, Body(description="取消原因")] = None,
) -> JSONResponse:
    """取消报名"""
    result_dict = await RegistrationService.cancel_service(auth=auth, id=id, reason=reason)
    log.info(f"取消报名 {id}")
    return SuccessResponse(data=result_dict, msg="取消成功")


@RegistrationRouter.post(
    "/confirm-payment/{id}",
    summary="确认支付",
    description="确认报名支付",
    response_model=ResponseSchema[RegistrationOutSchema],
)
async def confirm_payment_controller(
    id: Annotated[int, Path(description="报名ID")],
    data: RegistrationPaySchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:update"]))],
) -> JSONResponse:
    """确认支付"""
    result_dict = await RegistrationService.confirm_payment_service(auth=auth, id=id, data=data)
    log.info(f"确认支付报名 {id}")
    return SuccessResponse(data=result_dict, msg="确认成功")


@RegistrationRouter.get(
    "/statistics/status",
    summary="按状态统计",
    description="按状态统计报名数量",
)
async def statistics_by_status_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:query"]))],
) -> JSONResponse:
    """按状态统计"""
    result_dict = await RegistrationService.statistics_by_status_service(auth=auth)
    log.info("按状态统计报名成功")
    return SuccessResponse(data=result_dict, msg="统计成功")


@RegistrationRouter.get(
    "/statistics/consultation/{consultation_id}",
    summary="咨询会统计",
    description="统计某咨询会的报名情况",
)
async def statistics_by_consultation_controller(
    consultation_id: Annotated[int, Path(description="咨询会ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:registration:query"]))],
) -> JSONResponse:
    """咨询会统计"""
    result_dict = await RegistrationService.statistics_by_consultation_service(
        auth=auth, consultation_id=consultation_id
    )
    log.info(f"统计咨询会 {consultation_id} 报名情况成功")
    return SuccessResponse(data=result_dict, msg="统计成功")
