"""
表彰评优 - 控制器
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
    EvaluationCreateSchema,
    EvaluationOutSchema,
    EvaluationQuerySchema,
    EvaluationUpdateSchema,
)
from .service import EvaluationService

EvaluationRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/evaluation",
    tags=["招生宣传活动 - 表彰评优"],
)


@EvaluationRouter.get(
    "/detail/{id}",
    summary="获取表彰评优详情",
    description="获取表彰评优详情",
    response_model=ResponseSchema[EvaluationOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="表彰评优ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:detail"]))],
) -> JSONResponse:
    """
    获取表彰评优详情

    参数:
    - id (int): 表彰评优ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含表彰评优详情的JSON响应
    """
    result_dict = await EvaluationService.detail_service(auth=auth, id=id)
    log.info(f"获取表彰评优详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@EvaluationRouter.get(
    "/list",
    summary="查询表彰评优列表",
    description="查询表彰评优列表",
    response_model=ResponseSchema[list[EvaluationOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[EvaluationQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:query"]))],
) -> JSONResponse:
    """
    查询表彰评优列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (EvaluationQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含表彰评优列表分页信息的JSON响应
    """
    result_dict = await EvaluationService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询表彰评优列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@EvaluationRouter.post(
    "/create",
    summary="创建表彰评优",
    description="创建表彰评优",
    response_model=ResponseSchema[EvaluationOutSchema],
)
async def create_obj_controller(
    data: EvaluationCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:create"]))],
) -> JSONResponse:
    """
    创建表彰评优

    参数:
    - data (EvaluationCreateSchema): 表彰评优创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建表彰评优详情的JSON响应
    """
    result_dict = await EvaluationService.create_service(auth=auth, data=data)
    log.info("创建表彰评优成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@EvaluationRouter.put(
    "/update/{id}",
    summary="更新表彰评优",
    description="更新表彰评优",
    response_model=ResponseSchema[EvaluationOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="表彰评优ID")],
    data: EvaluationUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:update"]))],
) -> JSONResponse:
    """
    更新表彰评优

    参数:
    - id (int): 表彰评优ID
    - data (EvaluationUpdateSchema): 表彰评优更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后表彰评优详情的JSON响应
    """
    result_dict = await EvaluationService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新表彰评优成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@EvaluationRouter.delete(
    "/delete/{id}",
    summary="删除表彰评优",
    description="删除表彰评优",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="表彰评优ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:delete"]))],
) -> JSONResponse:
    """
    删除表彰评优

    参数:
    - id (int): 表彰评优ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await EvaluationService.delete_service(auth=auth, id=id)
    log.info(f"删除表彰评优成功 {id}")
    return SuccessResponse(msg="删除成功")


@EvaluationRouter.delete(
    "/batch-delete",
    summary="批量删除表彰评优",
    description="批量删除表彰评优",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:delete"]))],
) -> JSONResponse:
    """
    批量删除表彰评优

    参数:
    - ids (list[int]): 表彰评优ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await EvaluationService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除表彰评优成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@EvaluationRouter.post(
    "/submit/{id}",
    summary="提交表彰评优",
    description="提交表彰评优",
    response_model=ResponseSchema[EvaluationOutSchema],
)
async def submit_controller(
    id: Annotated[int, Path(description="表彰评优ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:update"]))],
) -> JSONResponse:
    """
    提交表彰评优

    参数:
    - id (int): 表彰评优ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 提交成功的JSON响应
    """
    result_dict = await EvaluationService.submit_service(auth=auth, id=id)
    log.info(f"提交表彰评优成功 {id}")
    return SuccessResponse(data=result_dict, msg="提交成功")


@EvaluationRouter.post(
    "/review/{id}",
    summary="审核表彰评优",
    description="审核表彰评优",
    response_model=ResponseSchema[EvaluationOutSchema],
)
async def review_controller(
    id: Annotated[int, Path(description="表彰评优ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:review"]))],
    review_comment: Annotated[str | None, Query(description="审核意见")] = None,
) -> JSONResponse:
    """
    审核表彰评优

    参数:
    - id (int): 表彰评优ID
    - review_comment (str | None): 审核意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审核成功的JSON响应
    """
    result_dict = await EvaluationService.review_service(
        auth=auth, id=id, review_comment=review_comment
    )
    log.info(f"审核表彰评优成功 {id}")
    return SuccessResponse(data=result_dict, msg="审核成功")


@EvaluationRouter.post(
    "/approve/{id}",
    summary="批准表彰评优",
    description="批准表彰评优",
    response_model=ResponseSchema[EvaluationOutSchema],
)
async def approve_controller(
    id: Annotated[int, Path(description="表彰评优ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:approve"]))],
    approval_comment: Annotated[str | None, Query(description="批准意见")] = None,
    reward_type: Annotated[str | None, Query(description="奖励类型")] = None,
    reward_amount: Annotated[float | None, Query(ge=0, description="奖励金额")] = None,
) -> JSONResponse:
    """
    批准表彰评优

    参数:
    - id (int): 表彰评优ID
    - approval_comment (str | None): 批准意见
    - reward_type (str | None): 奖励类型
    - reward_amount (float | None): 奖励金额
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批准成功的JSON响应
    """
    result_dict = await EvaluationService.approve_service(
        auth=auth,
        id=id,
        approval_comment=approval_comment,
        reward_type=reward_type,
        reward_amount=reward_amount,
    )
    log.info(f"批准表彰评优成功 {id}")
    return SuccessResponse(data=result_dict, msg="批准成功")


@EvaluationRouter.post(
    "/reject/{id}",
    summary="拒绝表彰评优",
    description="拒绝表彰评优",
    response_model=ResponseSchema[EvaluationOutSchema],
)
async def reject_controller(
    id: Annotated[int, Path(description="表彰评优ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:evaluation:approve"]))],
    approval_comment: Annotated[str, Query(description="拒绝意见")],
) -> JSONResponse:
    """
    拒绝表彰评优

    参数:
    - id (int): 表彰评优ID
    - approval_comment (str): 拒绝意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 拒绝成功的JSON响应
    """
    result_dict = await EvaluationService.reject_service(
        auth=auth, id=id, approval_comment=approval_comment
    )
    log.info(f"拒绝表彰评优成功 {id}")
    return SuccessResponse(data=result_dict, msg="拒绝成功")
