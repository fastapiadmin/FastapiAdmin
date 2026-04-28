"""
活动申请审批 - 控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    ActivityApplyCreateSchema,
    ActivityApplyOutSchema,
    ActivityApplyQuerySchema,
    ActivityApplyUpdateSchema,
)
from .service import ActivityApplyService

ActivityApplyRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/activity-apply",
    tags=["招生宣传活动 - 活动申请审批"],
)


@ActivityApplyRouter.get(
    "/detail/{id}",
    summary="获取活动申请详情",
    description="获取活动申请详情",
    response_model=ResponseSchema[ActivityApplyOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="活动申请ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:detail"]))
    ],
) -> JSONResponse:
    """
    获取活动申请详情

    参数:
    - id (int): 活动申请ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含活动申请详情的JSON响应
    """
    result_dict = await ActivityApplyService.detail_service(auth=auth, id=id)
    log.info(f"获取活动申请详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@ActivityApplyRouter.get(
    "/list",
    summary="查询活动申请列表",
    description="查询活动申请列表",
    response_model=ResponseSchema[list[ActivityApplyOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ActivityApplyQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:query"]))],
) -> JSONResponse:
    """
    查询活动申请列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (ActivityApplyQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含活动申请列表分页信息的JSON响应
    """
    result_dict = await ActivityApplyService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询活动申请列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@ActivityApplyRouter.post(
    "/create",
    summary="创建活动申请",
    description="创建活动申请",
    response_model=ResponseSchema[ActivityApplyOutSchema],
)
async def create_obj_controller(
    data: ActivityApplyCreateSchema,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:create"]))
    ],
) -> JSONResponse:
    """
    创建活动申请

    参数:
    - data (ActivityApplyCreateSchema): 活动申请创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建活动申请详情的JSON响应
    """
    result_dict = await ActivityApplyService.create_service(auth=auth, data=data)
    log.info("创建活动申请成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@ActivityApplyRouter.put(
    "/update/{id}",
    summary="更新活动申请",
    description="更新活动申请",
    response_model=ResponseSchema[ActivityApplyOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="活动申请ID")],
    data: ActivityApplyUpdateSchema,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:update"]))
    ],
) -> JSONResponse:
    """
    更新活动申请

    参数:
    - id (int): 活动申请ID
    - data (ActivityApplyUpdateSchema): 活动申请更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后活动申请详情的JSON响应
    """
    result_dict = await ActivityApplyService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新活动申请成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@ActivityApplyRouter.delete(
    "/delete/{id}",
    summary="删除活动申请",
    description="删除活动申请",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="活动申请ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:delete"]))
    ],
) -> JSONResponse:
    """
    删除活动申请

    参数:
    - id (int): 活动申请ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await ActivityApplyService.delete_service(auth=auth, id=id)
    log.info(f"删除活动申请成功 {id}")
    return SuccessResponse(msg="删除成功")


@ActivityApplyRouter.delete(
    "/batch-delete",
    summary="批量删除活动申请",
    description="批量删除活动申请",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:delete"]))
    ],
) -> JSONResponse:
    """
    批量删除活动申请

    参数:
    - ids (list[int]): 活动申请ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await ActivityApplyService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除活动申请成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@ActivityApplyRouter.post(
    "/approve/{id}",
    summary="审批通过",
    description="审批通过活动申请",
    response_model=ResponseSchema[ActivityApplyOutSchema],
)
async def approve_controller(
    id: Annotated[int, Path(description="活动申请ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:approve"]))
    ],
    approval_comment: Annotated[str | None, Query(description="审批意见")] = None,
) -> JSONResponse:
    """
    审批通过

    参数:
    - id (int): 活动申请ID
    - approval_comment (str | None): 审批意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审批通过的JSON响应
    """
    result_dict = await ActivityApplyService.approve_service(
        auth=auth, id=id, approval_comment=approval_comment
    )
    log.info(f"审批通过活动申请成功 {id}")
    return SuccessResponse(data=result_dict, msg="审批通过")


@ActivityApplyRouter.post(
    "/reject/{id}",
    summary="审批拒绝",
    description="审批拒绝活动申请",
    response_model=ResponseSchema[ActivityApplyOutSchema],
)
async def reject_controller(
    id: Annotated[int, Path(description="活动申请ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:approve"]))
    ],
    approval_comment: Annotated[str, Query(..., description="审批意见")],
) -> JSONResponse:
    """
    审批拒绝

    参数:
    - id (int): 活动申请ID
    - approval_comment (str): 审批意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审批拒绝的JSON响应
    """
    result_dict = await ActivityApplyService.reject_service(
        auth=auth, id=id, approval_comment=approval_comment
    )
    log.info(f"审批拒绝活动申请成功 {id}")
    return SuccessResponse(data=result_dict, msg="审批拒绝")


@ActivityApplyRouter.post(
    "/cancel/{id}",
    summary="取消活动申请",
    description="取消活动申请",
    response_model=ResponseSchema[ActivityApplyOutSchema],
)
async def cancel_controller(
    id: Annotated[int, Path(description="活动申请ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_promotion:activity_apply:update"]))
    ],
) -> JSONResponse:
    """
    取消活动申请

    参数:
    - id (int): 活动申请ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 取消成功的JSON响应
    """
    result_dict = await ActivityApplyService.cancel_service(auth=auth, id=id)
    log.info(f"取消活动申请成功 {id}")
    return SuccessResponse(data=result_dict, msg="取消成功")
