"""
费用报销 - 控制器
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

from .schema import ExpenseCreateSchema, ExpenseOutSchema, ExpenseQuerySchema, ExpenseUpdateSchema
from .service import ExpenseService

ExpenseRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/expense",
    tags=["招生宣传活动 - 费用报销"],
)


@ExpenseRouter.get(
    "/detail/{id}",
    summary="获取费用报销详情",
    description="获取费用报销详情",
    response_model=ResponseSchema[ExpenseOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="费用报销ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:expense:detail"]))],
) -> JSONResponse:
    """
    获取费用报销详情

    参数:
    - id (int): 费用报销ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含费用报销详情的JSON响应
    """
    result_dict = await ExpenseService.detail_service(auth=auth, id=id)
    log.info(f"获取费用报销详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@ExpenseRouter.get(
    "/list",
    summary="查询费用报销列表",
    description="查询费用报销列表",
    response_model=ResponseSchema[list[ExpenseOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ExpenseQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:expense:query"]))],
) -> JSONResponse:
    """
    查询费用报销列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (ExpenseQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含费用报销列表分页信息的JSON响应
    """
    result_dict = await ExpenseService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询费用报销列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@ExpenseRouter.post(
    "/create",
    summary="创建费用报销",
    description="创建费用报销",
    response_model=ResponseSchema[ExpenseOutSchema],
)
async def create_obj_controller(
    data: ExpenseCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:expense:create"]))],
) -> JSONResponse:
    """
    创建费用报销

    参数:
    - data (ExpenseCreateSchema): 费用报销创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建费用报销详情的JSON响应
    """
    result_dict = await ExpenseService.create_service(auth=auth, data=data)
    log.info("创建费用报销成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@ExpenseRouter.put(
    "/update/{id}",
    summary="更新费用报销",
    description="更新费用报销",
    response_model=ResponseSchema[ExpenseOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="费用报销ID")],
    data: ExpenseUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:expense:update"]))],
) -> JSONResponse:
    """
    更新费用报销

    参数:
    - id (int): 费用报销ID
    - data (ExpenseUpdateSchema): 费用报销更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后费用报销详情的JSON响应
    """
    result_dict = await ExpenseService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新费用报销成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@ExpenseRouter.delete(
    "/delete/{id}",
    summary="删除费用报销",
    description="删除费用报销",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="费用报销ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:expense:delete"]))],
) -> JSONResponse:
    """
    删除费用报销

    参数:
    - id (int): 费用报销ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await ExpenseService.delete_service(auth=auth, id=id)
    log.info(f"删除费用报销成功 {id}")
    return SuccessResponse(msg="删除成功")


@ExpenseRouter.delete(
    "/batch-delete",
    summary="批量删除费用报销",
    description="批量删除费用报销",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:expense:delete"]))],
) -> JSONResponse:
    """
    批量删除费用报销

    参数:
    - ids (list[int]): 费用报销ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await ExpenseService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除费用报销成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@ExpenseRouter.post(
    "/approve/{id}",
    summary="审批通过费用报销",
    description="审批通过费用报销",
    response_model=ResponseSchema[ExpenseOutSchema],
)
async def approve_controller(
    id: Annotated[int, Path(description="费用报销ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:expense:approve"]))],
    approval_comment: Annotated[str | None, Query(description="审批意见")] = None,
) -> JSONResponse:
    """
    审批通过费用报销

    参数:
    - id (int): 费用报销ID
    - approval_comment (str | None): 审批意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审批通过的JSON响应
    """
    result_dict = await ExpenseService.approve_service(auth=auth, id=id, approval_comment=approval_comment)
    log.info(f"审批通过费用报销成功 {id}")
    return SuccessResponse(data=result_dict, msg="审批通过")


@ExpenseRouter.post(
    "/reject/{id}",
    summary="审批拒绝费用报销",
    description="审批拒绝费用报销",
    response_model=ResponseSchema[ExpenseOutSchema],
)
async def reject_controller(
    id: Annotated[int, Path(description="费用报销ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:expense:approve"]))],
    approval_comment: Annotated[str, Query(description="审批意见")],
) -> JSONResponse:
    """
    审批拒绝费用报销

    参数:
    - id (int): 费用报销ID
    - approval_comment (str): 审批意见
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 审批拒绝的JSON响应
    """
    result_dict = await ExpenseService.reject_service(auth=auth, id=id, approval_comment=approval_comment)
    log.info(f"审批拒绝费用报销成功 {id}")
    return SuccessResponse(data=result_dict, msg="审批拒绝")


@ExpenseRouter.post(
    "/reimburse/{id}",
    summary="报销费用",
    description="报销费用",
    response_model=ResponseSchema[ExpenseOutSchema],
)
async def reimburse_controller(
    id: Annotated[int, Path(description="费用报销ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:expense:reimburse"]))],
    reimbursement_account: Annotated[str | None, Query(description="报销账户")] = None,
) -> JSONResponse:
    """
    报销费用

    参数:
    - id (int): 费用报销ID
    - reimbursement_account (str | None): 报销账户
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 报销成功的JSON响应
    """
    result_dict = await ExpenseService.reimburse_service(auth=auth, id=id, reimbursement_account=reimbursement_account)
    log.info(f"报销费用成功 {id}")
    return SuccessResponse(data=result_dict, msg="报销成功")
