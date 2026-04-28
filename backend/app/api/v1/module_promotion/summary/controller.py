"""
总结上传 - 控制器
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

from .schema import SummaryCreateSchema, SummaryOutSchema, SummaryQuerySchema, SummaryUpdateSchema
from .service import SummaryService

SummaryRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/summary",
    tags=["招生宣传活动 - 总结上传"],
)


@SummaryRouter.get(
    "/detail/{id}",
    summary="获取总结详情",
    description="获取总结详情",
    response_model=ResponseSchema[SummaryOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="总结ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:summary:detail"]))],
) -> JSONResponse:
    """
    获取总结详情

    参数:
    - id (int): 总结ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含总结详情的JSON响应
    """
    result_dict = await SummaryService.detail_service(auth=auth, id=id)
    log.info(f"获取总结详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@SummaryRouter.get(
    "/list",
    summary="查询总结列表",
    description="查询总结列表",
    response_model=ResponseSchema[list[SummaryOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[SummaryQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:summary:query"]))],
) -> JSONResponse:
    """
    查询总结列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (SummaryQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含总结列表分页信息的JSON响应
    """
    result_dict = await SummaryService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询总结列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@SummaryRouter.post(
    "/create",
    summary="创建总结",
    description="创建总结",
    response_model=ResponseSchema[SummaryOutSchema],
)
async def create_obj_controller(
    data: SummaryCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:summary:create"]))],
) -> JSONResponse:
    """
    创建总结

    参数:
    - data (SummaryCreateSchema): 总结创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建总结详情的JSON响应
    """
    result_dict = await SummaryService.create_service(auth=auth, data=data)
    log.info("创建总结成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@SummaryRouter.put(
    "/update/{id}",
    summary="更新总结",
    description="更新总结",
    response_model=ResponseSchema[SummaryOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="总结ID")],
    data: SummaryUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:summary:update"]))],
) -> JSONResponse:
    """
    更新总结

    参数:
    - id (int): 总结ID
    - data (SummaryUpdateSchema): 总结更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后总结详情的JSON响应
    """
    result_dict = await SummaryService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新总结成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@SummaryRouter.delete(
    "/delete/{id}",
    summary="删除总结",
    description="删除总结",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="总结ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:summary:delete"]))],
) -> JSONResponse:
    """
    删除总结

    参数:
    - id (int): 总结ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await SummaryService.delete_service(auth=auth, id=id)
    log.info(f"删除总结成功 {id}")
    return SuccessResponse(msg="删除成功")


@SummaryRouter.delete(
    "/batch-delete",
    summary="批量删除总结",
    description="批量删除总结",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:summary:delete"]))],
) -> JSONResponse:
    """
    批量删除总结

    参数:
    - ids (list[int]): 总结ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await SummaryService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除总结成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@SummaryRouter.post(
    "/submit/{id}",
    summary="提交总结",
    description="提交总结",
    response_model=ResponseSchema[SummaryOutSchema],
)
async def submit_controller(
    id: Annotated[int, Path(description="总结ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:summary:update"]))],
) -> JSONResponse:
    """
    提交总结

    参数:
    - id (int): 总结ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 提交成功的JSON响应
    """
    result_dict = await SummaryService.submit_service(auth=auth, id=id)
    log.info(f"提交总结成功 {id}")
    return SuccessResponse(data=result_dict, msg="提交成功")


@SummaryRouter.post(
    "/approve/{id}",
    summary="审批通过总结",
    description="审批通过总结",
    response_model=ResponseSchema[SummaryOutSchema],
)
async def approve_controller(
    id: Annotated[int, Path(description="总结ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:summary:approve"]))],
    approval_comment: Annotated[str | None, Query(description="审批意见")] = None,
) -> JSONResponse:
    """
    审批通过总结

    参数:
    - id (int): 总结ID
    - approval_comment (str | None): 审批意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审批通过的JSON响应
    """
    result_dict = await SummaryService.approve_service(
        auth=auth, id=id, approval_comment=approval_comment
    )
    log.info(f"审批通过总结成功 {id}")
    return SuccessResponse(data=result_dict, msg="审批通过")


@SummaryRouter.post(
    "/reject/{id}",
    summary="审批拒绝总结",
    description="审批拒绝总结",
    response_model=ResponseSchema[SummaryOutSchema],
)
async def reject_controller(
    id: Annotated[int, Path(description="总结ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:summary:approve"]))],
    approval_comment: Annotated[str, Query(description="审批意见")],
) -> JSONResponse:
    """
    审批拒绝总结

    参数:
    - id (int): 总结ID
    - approval_comment (str): 审批意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审批拒绝的JSON响应
    """
    result_dict = await SummaryService.reject_service(
        auth=auth, id=id, approval_comment=approval_comment
    )
    log.info(f"审批拒绝总结成功 {id}")
    return SuccessResponse(data=result_dict, msg="审批拒绝")
