from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .schema import (
    WorkflowCreateSchema,
    WorkflowExecuteResultSchema,
    WorkflowExecuteSchema,
    WorkflowOutSchema,
    WorkflowQueryParam,
    WorkflowUpdateSchema,
)
from .service import WorkflowService

WorkflowRouter = APIRouter(route_class=OperationLogRoute, prefix="/workflow/definition", tags=["任务调度", "工作流"])


@WorkflowRouter.get(
    "/detail/{id}",
    summary="工作流详情",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def get_workflow_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:detail"]))],
    id: Annotated[int, Path(description="工作流ID")],
) -> JSONResponse:
    result_dict = await WorkflowService(auth).get_workflow_detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取工作流详情成功")


@WorkflowRouter.get(
    "/list",
    summary="工作流列表",
    response_model=ResponseSchema[PageResultSchema[WorkflowOutSchema]],
)
async def get_workflow_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[WorkflowQueryParam, Query(description="查询参数")],
) -> JSONResponse:
    result_dict = await WorkflowService(auth).get_workflow_page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询工作流列表成功")


@WorkflowRouter.post(
    "/create",
    summary="创建工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def create_workflow_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:create"]))],
    data: Annotated[WorkflowCreateSchema, Body(description="创建工作流参数")],
) -> JSONResponse:
    result_dict = await WorkflowService(auth).create_workflow(data=data)
    return SuccessResponse(data=result_dict, msg="创建工作流成功")


@WorkflowRouter.put(
    "/update/{id}",
    summary="更新工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def update_workflow_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:update"]))],
    id: Annotated[int, Path(description="工作流ID")],
    data: Annotated[WorkflowUpdateSchema, Body(description="更新工作流参数")],
) -> JSONResponse:
    result_dict = await WorkflowService(auth).update_workflow(id=id, data=data)
    return SuccessResponse(data=result_dict, msg="更新工作流成功")


@WorkflowRouter.delete(
    "/delete",
    summary="删除工作流",
    response_model=ResponseSchema[None],
)
async def delete_workflow_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    await WorkflowService(auth).delete_workflow(ids=ids)
    return SuccessResponse(msg="删除工作流成功")


@WorkflowRouter.post(
    "/publish/{id}",
    summary="发布工作流",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def publish_workflow_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:update"]))],
    id: Annotated[int, Path(description="工作流ID")],
) -> JSONResponse:
    result_dict = await WorkflowService(auth).publish_workflow(id=id)
    return SuccessResponse(data=result_dict, msg="发布工作流成功")


@WorkflowRouter.post(
    "/execute",
    summary="执行工作流",
    response_model=ResponseSchema[WorkflowExecuteResultSchema],
)
async def execute_workflow_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:execute"]))],
    body: Annotated[WorkflowExecuteSchema, Body(description="执行工作流参数")],
) -> JSONResponse:
    result_dict = await WorkflowService(auth).execute_workflow(body=body)
    return SuccessResponse(data=result_dict, msg="执行工作流完成")
