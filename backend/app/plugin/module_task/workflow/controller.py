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
    WorkflowCreateSchema,
    WorkflowExecuteResultSchema,
    WorkflowExecuteSchema,
    WorkflowOutSchema,
    WorkflowPublishSchema,
    WorkflowQueryParam,
    WorkflowUpdateSchema,
)
from .service import WorkflowService

WorkflowRouter = APIRouter(route_class=OperationLogRoute, prefix="/workflow", tags=["工作流模块"])


@WorkflowRouter.get(
    "/detail/{id}",
    summary="获取工作流详情",
    description="获取工作流详情",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:detail"]))],
) -> JSONResponse:
    """
    获取工作流详情

    参数:
    - id (int): 工作流ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含工作流详情的JSON响应
    """
    result_dict = await WorkflowService.detail_service(id=id, auth=auth)
    log.info(f"获取工作流详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取工作流详情成功")


@WorkflowRouter.get(
    "/list",
    summary="查询工作流列表",
    description="查询工作流列表",
    response_model=ResponseSchema[list[WorkflowOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[WorkflowQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:query"]))],
) -> JSONResponse:
    """
    查询工作流列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (WorkflowQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含工作流列表分页信息的JSON响应
    """
    result_dict = await WorkflowService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询工作流列表成功")
    return SuccessResponse(data=result_dict, msg="查询工作流列表成功")


@WorkflowRouter.post(
    "/create",
    summary="创建工作流",
    description="创建工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def create_obj_controller(
    data: WorkflowCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:create"]))],
) -> JSONResponse:
    """
    创建工作流

    参数:
    - data (WorkflowCreateSchema): 工作流创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建工作流详情的JSON响应
    """
    result_dict = await WorkflowService.create_service(auth=auth, data=data)
    log.info(f"创建工作流成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="创建工作流成功")


@WorkflowRouter.put(
    "/update/{id}",
    summary="修改工作流",
    description="修改工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def update_obj_controller(
    data: WorkflowUpdateSchema,
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:update"]))],
) -> JSONResponse:
    """
    修改工作流

    参数:
    - data (WorkflowUpdateSchema): 工作流更新模型
    - id (int): 工作流ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含修改工作流详情的JSON响应
    """
    result_dict = await WorkflowService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改工作流成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="修改工作流成功")


@WorkflowRouter.delete(
    "/delete",
    summary="删除工作流",
    description="删除工作流",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:delete"]))],
) -> JSONResponse:
    """
    删除工作流

    参数:
    - ids (list[int]): 工作流ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除工作流详情的JSON响应
    """
    await WorkflowService.delete_service(auth=auth, ids=ids)
    log.info(f"删除工作流成功: {ids}")
    return SuccessResponse(msg="删除工作流成功")


@WorkflowRouter.post(
    "/publish/{id}",
    summary="发布工作流",
    description="发布工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def publish_obj_controller(
    id: Annotated[int, Path(description="工作流ID")],
    data: WorkflowPublishSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:publish"]))],
) -> JSONResponse:
    """
    发布工作流

    参数:
    - id (int): 工作流ID
    - data (WorkflowPublishSchema): 发布模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含发布工作流详情的JSON响应
    """
    result_dict = await WorkflowService.publish_service(auth=auth, id=id, data=data)
    log.info(f"发布工作流成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="发布工作流成功")


@WorkflowRouter.post(
    "/execute",
    summary="执行工作流",
    description="执行工作流",
    response_model=ResponseSchema[WorkflowExecuteResultSchema],
)
async def execute_obj_controller(
    data: WorkflowExecuteSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:execute"]))],
) -> JSONResponse:
    """
    执行工作流

    参数:
    - data (WorkflowExecuteSchema): 执行模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含执行结果的JSON响应
    """
    result_dict = await WorkflowService.execute_service(auth=auth, data=data)
    log.info(f"执行工作流成功: {result_dict.get('workflow_id')}")
    return SuccessResponse(data=result_dict, msg="执行工作流成功")
