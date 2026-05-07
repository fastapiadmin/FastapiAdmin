"""
审批记录 - 控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import ApprovalRecordOutSchema, ApprovalRecordQuerySchema
from .service import ApprovalRecordService

ApprovalRecordRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/approval-record",
    tags=["招生宣传活动 - 审批记录"],
)


@ApprovalRecordRouter.get(
    "/detail/{id}",
    summary="获取审批记录详情",
    description="获取审批记录详情",
    response_model=ResponseSchema[ApprovalRecordOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="审批记录ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:detail"]))
    ],
) -> JSONResponse:
    """获取审批记录详情"""
    result_dict = await ApprovalRecordService.detail_service(auth=auth, id=id)
    log.info(f"获取审批记录详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@ApprovalRecordRouter.get(
    "/list",
    summary="查询审批记录列表",
    description="查询审批记录列表",
    response_model=ResponseSchema[list[ApprovalRecordOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ApprovalRecordQuerySchema, Depends()],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:detail"]))
    ],
) -> JSONResponse:
    """查询审批记录列表"""
    result_dict = await ApprovalRecordService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询审批记录列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@ApprovalRecordRouter.get(
    "/by-apply/{activity_apply_id}",
    summary="获取活动申请的审批记录",
    description="获取活动申请的所有审批记录",
    response_model=ResponseSchema[list[ApprovalRecordOutSchema]],
)
async def get_by_apply_controller(
    activity_apply_id: Annotated[int, Path(description="活动申请ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:detail"]))
    ],
) -> JSONResponse:
    """获取活动申请的所有审批记录"""
    result_list = await ApprovalRecordService.list_by_apply_service(
        auth=auth, activity_apply_id=activity_apply_id
    )
    log.info(f"获取活动申请审批记录成功 {activity_apply_id}")
    return SuccessResponse(data=result_list, msg="获取审批记录成功")
