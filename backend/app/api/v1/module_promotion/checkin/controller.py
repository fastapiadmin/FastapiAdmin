"""
活动打卡 - 控制器
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

from .schema import CheckinCreateSchema, CheckinOutSchema, CheckinQuerySchema, CheckinUpdateSchema
from .service import CheckinService

CheckinRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/checkin",
    tags=["招生宣传活动 - 活动打卡"],
)


@CheckinRouter.get(
    "/detail/{id}",
    summary="获取活动打卡详情",
    description="获取活动打卡详情",
    response_model=ResponseSchema[CheckinOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="活动打卡ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:checkin:detail"]))],
) -> JSONResponse:
    """
    获取活动打卡详情

    参数:
    - id (int): 活动打卡ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含活动打卡详情的JSON响应
    """
    result_dict = await CheckinService.detail_service(auth=auth, id=id)
    log.info(f"获取活动打卡详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@CheckinRouter.get(
    "/list",
    summary="查询活动打卡列表",
    description="查询活动打卡列表",
    response_model=ResponseSchema[list[CheckinOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[CheckinQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:checkin:query"]))],
) -> JSONResponse:
    """
    查询活动打卡列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (CheckinQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含活动打卡列表分页信息的JSON响应
    """
    result_dict = await CheckinService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询活动打卡列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@CheckinRouter.post(
    "/create",
    summary="创建活动打卡",
    description="创建活动打卡",
    response_model=ResponseSchema[CheckinOutSchema],
)
async def create_obj_controller(
    data: CheckinCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:checkin:create"]))],
) -> JSONResponse:
    """
    创建活动打卡

    参数:
    - data (CheckinCreateSchema): 活动打卡创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建活动打卡详情的JSON响应
    """
    result_dict = await CheckinService.create_service(auth=auth, data=data)
    log.info("创建活动打卡成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@CheckinRouter.put(
    "/update/{id}",
    summary="更新活动打卡",
    description="更新活动打卡",
    response_model=ResponseSchema[CheckinOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="活动打卡ID")],
    data: CheckinUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:checkin:update"]))],
) -> JSONResponse:
    """
    更新活动打卡

    参数:
    - id (int): 活动打卡ID
    - data (CheckinUpdateSchema): 活动打卡更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后活动打卡详情的JSON响应
    """
    result_dict = await CheckinService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新活动打卡成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@CheckinRouter.delete(
    "/delete/{id}",
    summary="删除活动打卡",
    description="删除活动打卡",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="活动打卡ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:checkin:delete"]))],
) -> JSONResponse:
    """
    删除活动打卡

    参数:
    - id (int): 活动打卡ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await CheckinService.delete_service(auth=auth, id=id)
    log.info(f"删除活动打卡成功 {id}")
    return SuccessResponse(msg="删除成功")


@CheckinRouter.delete(
    "/batch-delete",
    summary="批量删除活动打卡",
    description="批量删除活动打卡",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:checkin:delete"]))],
) -> JSONResponse:
    """
    批量删除活动打卡

    参数:
    - ids (list[int]): 活动打卡ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await CheckinService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除活动打卡成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@CheckinRouter.post(
    "/validate/{id}",
    summary="验证打卡",
    description="验证打卡",
    response_model=ResponseSchema[CheckinOutSchema],
)
async def validate_controller(
    id: Annotated[int, Path(description="活动打卡ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:checkin:validate"]))],
) -> JSONResponse:
    """
    验证打卡

    参数:
    - id (int): 活动打卡ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 验证成功的JSON响应
    """
    result_dict = await CheckinService.validate_service(auth=auth, id=id)
    log.info(f"验证打卡成功 {id}")
    return SuccessResponse(data=result_dict, msg="验证成功")


@CheckinRouter.post(
    "/invalidate/{id}",
    summary="无效打卡",
    description="无效打卡",
    response_model=ResponseSchema[CheckinOutSchema],
)
async def invalidate_controller(
    id: Annotated[int, Path(description="活动打卡ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:checkin:validate"]))],
    reason: Annotated[str, Query(..., description="无效原因")],
) -> JSONResponse:
    """
    无效打卡

    参数:
    - id (int): 活动打卡ID
    - reason (str): 无效原因
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 无效成功的JSON响应
    """
    result_dict = await CheckinService.invalidate_service(auth=auth, id=id, reason=reason)
    log.info(f"无效打卡成功 {id}")
    return SuccessResponse(data=result_dict, msg="无效成功")


@CheckinRouter.post(
    "/gps-validate/{id}",
    summary="GPS位置验证",
    description="验证打卡位置是否在允许范围内",
    response_model=ResponseSchema[CheckinOutSchema],
)
async def gps_validate_controller(
    id: Annotated[int, Path(description="活动打卡ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:checkin:validate"]))],
) -> JSONResponse:
    """
    GPS位置验证

    参数:
    - id (int): 活动打卡ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含GPS验证结果的JSON响应
    """
    result_dict = await CheckinService.gps_validate_service(auth=auth, id=id)
    gps_msg = result_dict.pop("gps_validation_message", "验证完成")
    log.info(f"GPS验证成功 {id}: {gps_msg}")
    return SuccessResponse(data=result_dict, msg=gps_msg)
