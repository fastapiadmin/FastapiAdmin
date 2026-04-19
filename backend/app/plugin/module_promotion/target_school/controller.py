"""
目标学校管理 - 控制器
"""
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    TargetSchoolCreateSchema,
    TargetSchoolOutSchema,
    TargetSchoolQuerySchema,
    TargetSchoolUpdateSchema,
)
from .service import TargetSchoolService

TargetSchoolRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/target-school",
    tags=["招生宣传活动 - 目标学校管理"],
)


@TargetSchoolRouter.get(
    "/detail/{id}",
    summary="获取目标学校详情",
    description="获取目标学校详情",
    response_model=ResponseSchema[TargetSchoolOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="目标学校ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:target_school:detail"]))],
) -> JSONResponse:
    """
    获取目标学校详情

    参数:
    - id (int): 目标学校ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含目标学校详情的JSON响应
    """
    result_dict = await TargetSchoolService.detail_service(auth=auth, id=id)
    log.info(f"获取目标学校详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@TargetSchoolRouter.get(
    "/list",
    summary="查询目标学校列表",
    description="查询目标学校列表",
    response_model=ResponseSchema[list[TargetSchoolOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[TargetSchoolQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:target_school:query"]))],
) -> JSONResponse:
    """
    查询目标学校列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (TargetSchoolQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含目标学校列表分页信息的JSON响应
    """
    result_dict = await TargetSchoolService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询目标学校列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@TargetSchoolRouter.post(
    "/create",
    summary="创建目标学校",
    description="创建目标学校",
    response_model=ResponseSchema[TargetSchoolOutSchema],
)
async def create_obj_controller(
    data: TargetSchoolCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:target_school:create"]))],
) -> JSONResponse:
    """
    创建目标学校

    参数:
    - data (TargetSchoolCreateSchema): 目标学校创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建目标学校详情的JSON响应
    """
    result_dict = await TargetSchoolService.create_service(auth=auth, data=data)
    log.info(f"创建目标学校成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@TargetSchoolRouter.put(
    "/update/{id}",
    summary="更新目标学校",
    description="更新目标学校",
    response_model=ResponseSchema[TargetSchoolOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="目标学校ID")],
    data: TargetSchoolUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:target_school:update"]))],
) -> JSONResponse:
    """
    更新目标学校

    参数:
    - id (int): 目标学校ID
    - data (TargetSchoolUpdateSchema): 目标学校更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后目标学校详情的JSON响应
    """
    result_dict = await TargetSchoolService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新目标学校成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@TargetSchoolRouter.delete(
    "/delete/{id}",
    summary="删除目标学校",
    description="删除目标学校",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="目标学校ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:target_school:delete"]))],
) -> JSONResponse:
    """
    删除目标学校

    参数:
    - id (int): 目标学校ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await TargetSchoolService.delete_service(auth=auth, id=id)
    log.info(f"删除目标学校成功 {id}")
    return SuccessResponse(msg="删除成功")


@TargetSchoolRouter.delete(
    "/batch-delete",
    summary="批量删除目标学校",
    description="批量删除目标学校",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:target_school:delete"]))],
) -> JSONResponse:
    """
    批量删除目标学校

    参数:
    - ids (list[int]): 目标学校ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await TargetSchoolService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除目标学校成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@TargetSchoolRouter.post(
    "/follow/{id}",
    summary="跟进目标学校",
    description="跟进目标学校",
    response_model=ResponseSchema[TargetSchoolOutSchema],
)
async def follow_controller(
    id: Annotated[int, Path(description="目标学校ID")],
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:target_school:follow"]))],
) -> JSONResponse:
    """
    跟进目标学校

    参数:
    - id (int): 目标学校ID
    - data (dict): 跟进数据
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 跟进成功的JSON响应
    """
    result_dict = await TargetSchoolService.follow_service(auth=auth, id=id, data=data)
    log.info(f"跟进目标学校成功 {id}")
    return SuccessResponse(data=result_dict, msg="跟进成功")


@TargetSchoolRouter.get(
    "/team/{team_id}",
    summary="获取招生组下所有目标学校",
    description="获取招生组下所有目标学校",
    response_model=ResponseSchema[list[TargetSchoolOutSchema]],
)
async def get_by_team_controller(
    team_id: Annotated[int, Path(description="招生组ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:target_school:query"]))],
) -> JSONResponse:
    """
    获取招生组下所有目标学校

    参数:
    - team_id (int): 招生组ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含目标学校列表的JSON响应
    """
    result_list = await TargetSchoolService.get_by_team_service(auth=auth, team_id=team_id)
    log.info(f"获取招生组目标学校列表成功")
    return SuccessResponse(data=result_list, msg="获取列表成功")


@TargetSchoolRouter.get(
    "/personnel/{personnel_id}",
    summary="获取负责人下所有目标学校",
    description="获取负责人下所有目标学校",
    response_model=ResponseSchema[list[TargetSchoolOutSchema]],
)
async def get_by_personnel_controller(
    personnel_id: Annotated[int, Path(description="负责人ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:target_school:query"]))],
) -> JSONResponse:
    """
    获取负责人下所有目标学校

    参数:
    - personnel_id (int): 负责人ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含目标学校列表的JSON响应
    """
    result_list = await TargetSchoolService.get_by_personnel_service(auth=auth, personnel_id=personnel_id)
    log.info(f"获取负责人目标学校列表成功")
    return SuccessResponse(data=result_list, msg="获取列表成功")