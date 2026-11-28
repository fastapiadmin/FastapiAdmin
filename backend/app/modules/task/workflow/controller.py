from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, Security, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_schema import AuthSchema, PageResultSchema, PaginationQueryParam
from app.core.dependencies import AuthPermission, db_getter
from app.core.router_class import OperationLogRoute

from .schema import (
    WorkflowActionSchema,
    WorkflowCreateSchema,
    WorkflowInstanceOutSchema,
    WorkflowOutSchema,
    WorkflowQueryParam,
    WorkflowRunSchema,
    WorkflowTaskOutSchema,
    WorkflowUpdateSchema,
)
from .service import WorkflowService

WorkflowRouter = APIRouter(route_class=OperationLogRoute, prefix="/workflow", tags=["流程编排"])


@WorkflowRouter.get("/page", summary="分页查询流程", response_model=ResponseSchema[PageResultSchema[WorkflowOutSchema]])
async def get_workflow_page_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:query"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[WorkflowQueryParam, Query()],
) -> JSONResponse:
    result = await WorkflowService(auth, db).page(page.page_no, page.page_size, search)
    return SuccessResponse(data=result, msg="查询流程分页成功")


@WorkflowRouter.get("/detail/{id}", summary="查询流程详情", response_model=ResponseSchema[WorkflowOutSchema])
async def get_workflow_detail_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:query"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(ge=1)],
) -> JSONResponse:
    result = await WorkflowService(auth, db).detail(id)
    return SuccessResponse(data=result, msg="查询流程详情成功")


@WorkflowRouter.post("/create", status_code=status.HTTP_201_CREATED, summary="创建流程", response_model=ResponseSchema[WorkflowOutSchema])
async def create_workflow_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:create"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    data: Annotated[WorkflowCreateSchema, Body()],
) -> JSONResponse:
    result = await WorkflowService(auth, db).create(data)
    return SuccessResponse(data=result, msg="创建流程成功")


@WorkflowRouter.put("/update/{id}", summary="修改流程", response_model=ResponseSchema[WorkflowOutSchema])
async def update_workflow_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:update"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(ge=1)],
    data: Annotated[WorkflowUpdateSchema, Body()],
) -> JSONResponse:
    result = await WorkflowService(auth, db).update(id, data)
    return SuccessResponse(data=result, msg="修改流程成功")


@WorkflowRouter.delete("/delete", summary="删除流程", response_model=ResponseSchema[None])
async def delete_workflow_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:delete"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    ids: Annotated[list[int], Body()],
) -> JSONResponse:
    await WorkflowService(auth, db).delete(ids)
    return SuccessResponse(msg="删除流程成功")


@WorkflowRouter.post("/execute/{id}", summary="发起流程", response_model=ResponseSchema[WorkflowInstanceOutSchema])
async def execute_workflow_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:execute"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(ge=1)],
    data: Annotated[WorkflowRunSchema, Body()],
) -> JSONResponse:
    result = await WorkflowService(auth, db).execute(id, data)
    return SuccessResponse(data=result, msg="流程已发起")


@WorkflowRouter.get("/instances/page", summary="流程实例分页", response_model=ResponseSchema[PageResultSchema[WorkflowInstanceOutSchema]])
async def get_instance_page_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:query"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    page: Annotated[PaginationQueryParam, Depends()],
    workflow_id: Annotated[int | None, Query(ge=1)] = None,
    status: Annotated[str | None, Query()] = None,
) -> JSONResponse:
    result = await WorkflowService(auth, db).instances(page.page_no, page.page_size, workflow_id, status)
    return SuccessResponse(data=result, msg="查询流程实例成功")


@WorkflowRouter.get("/instances/{id}", summary="流程实例详情", response_model=ResponseSchema[WorkflowInstanceOutSchema])
async def get_instance_detail_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:query"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(ge=1)],
) -> JSONResponse:
    result = await WorkflowService(auth, db).instance_detail(id)
    return SuccessResponse(data=result, msg="查询流程实例成功")


@WorkflowRouter.get("/tasks/pending", summary="我的待审批任务", response_model=ResponseSchema[list[WorkflowTaskOutSchema]])
async def get_pending_tasks_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:query"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
) -> JSONResponse:
    result = await WorkflowService(auth, db).pending_tasks()
    return SuccessResponse(data=result, msg="查询待审批任务成功")


@WorkflowRouter.post("/tasks/{id}/action", summary="审批任务", response_model=ResponseSchema[WorkflowTaskOutSchema])
async def act_task_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_task:workflow:execute"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(ge=1)],
    data: Annotated[WorkflowActionSchema, Body()],
) -> JSONResponse:
    result = await WorkflowService(auth, db).act(id, data)
    return SuccessResponse(data=result, msg="审批完成")
