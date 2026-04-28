"""
物料管理 - 控制器
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
    MaterialApplyCreateSchema,
    MaterialApplyOutSchema,
    MaterialApplyQuerySchema,
    MaterialCreateSchema,
    MaterialOutSchema,
    MaterialQuerySchema,
    MaterialUpdateSchema,
)
from .service import MaterialApplyService, MaterialService

MaterialRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/material",
    tags=["招生宣传活动 - 物料管理"],
)


@MaterialRouter.get(
    "/detail/{id}",
    summary="获取物料详情",
    description="获取物料详情",
    response_model=ResponseSchema[MaterialOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="物料ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:detail"]))],
) -> JSONResponse:
    """
    获取物料详情

    参数:
    - id (int): 物料ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含物料详情的JSON响应
    """
    result_dict = await MaterialService.detail_service(auth=auth, id=id)
    log.info(f"获取物料详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@MaterialRouter.get(
    "/list",
    summary="查询物料列表",
    description="查询物料列表",
    response_model=ResponseSchema[list[MaterialOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[MaterialQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:query"]))],
) -> JSONResponse:
    """
    查询物料列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (MaterialQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含物料列表分页信息的JSON响应
    """
    result_dict = await MaterialService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询物料列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@MaterialRouter.post(
    "/create",
    summary="创建物料",
    description="创建物料",
    response_model=ResponseSchema[MaterialOutSchema],
)
async def create_obj_controller(
    data: MaterialCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:create"]))],
) -> JSONResponse:
    """
    创建物料

    参数:
    - data (MaterialCreateSchema): 物料创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建物料详情的JSON响应
    """
    result_dict = await MaterialService.create_service(auth=auth, data=data)
    log.info("创建物料成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@MaterialRouter.put(
    "/update/{id}",
    summary="更新物料",
    description="更新物料",
    response_model=ResponseSchema[MaterialOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="物料ID")],
    data: MaterialUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:update"]))],
) -> JSONResponse:
    """
    更新物料

    参数:
    - id (int): 物料ID
    - data (MaterialUpdateSchema): 物料更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后物料详情的JSON响应
    """
    result_dict = await MaterialService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新物料成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@MaterialRouter.delete(
    "/delete/{id}",
    summary="删除物料",
    description="删除物料",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="物料ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:delete"]))],
) -> JSONResponse:
    """
    删除物料

    参数:
    - id (int): 物料ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await MaterialService.delete_service(auth=auth, id=id)
    log.info(f"删除物料成功 {id}")
    return SuccessResponse(msg="删除成功")


@MaterialRouter.delete(
    "/batch-delete",
    summary="批量删除物料",
    description="批量删除物料",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:delete"]))],
) -> JSONResponse:
    """
    批量删除物料

    参数:
    - ids (list[int]): 物料ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await MaterialService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除物料成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@MaterialRouter.post(
    "/replenish/{id}",
    summary="补充库存",
    description="招生办录入全年物料总量",
    response_model=ResponseSchema[MaterialOutSchema],
)
async def replenish_controller(
    id: Annotated[int, Path(description="物料ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:create"]))],
    add_quantity: Annotated[int, Query(description="补充数量")],
) -> JSONResponse:
    """
    补充库存

    参数:
    - id (int): 物料ID
    - add_quantity (int): 补充数量
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 补充库存成功的JSON响应
    """
    result_dict = await MaterialService.replenish_service(
        auth=auth, id=id, add_quantity=add_quantity
    )
    log.info(f"补充库存成功 {id}")
    return SuccessResponse(data=result_dict, msg="补充成功")


@MaterialRouter.post(
    "/apply",
    summary="申领物料",
    description="申领物料",
    response_model=ResponseSchema[MaterialApplyOutSchema],
)
async def apply_controller(
    data: MaterialApplyCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:apply"]))],
) -> JSONResponse:
    """
    申领物料

    参数:
    - data (MaterialApplyCreateSchema): 申领数据
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 申领成功的JSON响应
    """
    result_dict = await MaterialApplyService.create_service(auth=auth, data=data)
    log.info("申领物料成功")
    return SuccessResponse(data=result_dict, msg="申领成功")


@MaterialRouter.get(
    "/apply/list",
    summary="查询物料申请列表",
    description="查询物料申请列表",
    response_model=ResponseSchema[list[MaterialApplyOutSchema]],
)
async def get_apply_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[MaterialApplyQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:query"]))],
) -> JSONResponse:
    """
    查询物料申请列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (MaterialApplyQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含物料申请列表分页信息的JSON响应
    """
    result_dict = await MaterialApplyService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询物料申请列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@MaterialRouter.post(
    "/apply/approve/{id}",
    summary="审批通过物料申请",
    description="审批通过物料申请",
    response_model=ResponseSchema[MaterialApplyOutSchema],
)
async def approve_controller(
    id: Annotated[int, Path(description="物料申请ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:approve"]))],
    approved_quantity: Annotated[int | None, Query(description="批准数量")] = None,
) -> JSONResponse:
    """
    审批通过物料申请

    参数:
    - id (int): 物料申请ID
    - approved_quantity (int | None): 批准数量
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审批通过的JSON响应
    """
    result_dict = await MaterialApplyService.approve_service(
        auth=auth, id=id, approved_quantity=approved_quantity
    )
    log.info(f"审批通过物料申请成功 {id}")
    return SuccessResponse(data=result_dict, msg="审批通过")


@MaterialRouter.post(
    "/apply/reject/{id}",
    summary="审批拒绝物料申请",
    description="审批拒绝物料申请",
    response_model=ResponseSchema[MaterialApplyOutSchema],
)
async def reject_controller(
    id: Annotated[int, Path(description="物料申请ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:approve"]))],
    approval_comment: Annotated[str, Query(description="审批意见")],
) -> JSONResponse:
    """
    审批拒绝物料申请

    参数:
    - id (int): 物料申请ID
    - approval_comment (str): 审批意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审批拒绝的JSON响应
    """
    result_dict = await MaterialApplyService.reject_service(
        auth=auth, id=id, approval_comment=approval_comment
    )
    log.info(f"审批拒绝物料申请成功 {id}")
    return SuccessResponse(data=result_dict, msg="审批拒绝")


@MaterialRouter.post(
    "/apply/issue/{id}",
    summary="发放物料",
    description="发放物料",
    response_model=ResponseSchema[MaterialApplyOutSchema],
)
async def issue_controller(
    id: Annotated[int, Path(description="物料申请ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:material:issue"]))],
    issued_quantity: Annotated[int | None, Query(description="发放数量")] = None,
) -> JSONResponse:
    """
    发放物料

    参数:
    - id (int): 物料申请ID
    - issued_quantity (int | None): 发放数量
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 发放成功的JSON响应
    """
    result_dict = await MaterialApplyService.issue_service(
        auth=auth, id=id, issued_quantity=issued_quantity
    )
    log.info(f"发放物料成功 {id}")
    return SuccessResponse(data=result_dict, msg="发放成功")
