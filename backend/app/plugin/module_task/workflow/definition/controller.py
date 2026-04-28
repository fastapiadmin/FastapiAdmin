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
    WorkflowExecuteSchema,
    WorkflowOutSchema,
    WorkflowPublishSchema,
    WorkflowQueryParam,
    WorkflowUpdateSchema,
)
from .service import WorkflowService

WorkflowRouter = APIRouter(
    route_class=OperationLogRoute, prefix="/workflow/definition", tags=["工作流"]
)


@WorkflowRouter.get(
    "/detail/{id}",
    summary="工作流详情",
    description="根据ID获取工作流详情（含画布 nodes/edges）",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def get_workflow_detail_controller(
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:detail"]))
    ],
) -> JSONResponse:
    """
    根据 ID 获取工作流详情（含画布 nodes/edges）。

    参数:
    - id (int): 工作流 ID。
    - auth (AuthSchema): 认证信息。

    返回:
    - JSONResponse: 成功响应，data 为详情字典。
    """
    result_dict = await WorkflowService.get_workflow_detail_service(auth=auth, id=id)
    log.info(f"获取工作流详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取工作流详情成功")


@WorkflowRouter.get(
    "/list",
    summary="工作流列表",
    description="分页查询工作流列表",
    response_model=ResponseSchema[list[WorkflowOutSchema]],
)
async def get_workflow_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[WorkflowQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:query"]))],
) -> JSONResponse:
    """
    分页查询工作流列表。

    参数:
    - page (PaginationQueryParam): 分页与排序参数。
    - search (WorkflowQueryParam): 查询条件。
    - auth (AuthSchema): 认证信息。

    返回:
    - JSONResponse: 成功响应，data 为分页结果。
    """
    result_dict = await WorkflowService.get_workflow_page_service(
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
    description="创建草稿工作流，保存 Vue Flow 画布",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def create_workflow_controller(
    data: WorkflowCreateSchema,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:create"]))
    ],
) -> JSONResponse:
    """
    创建草稿工作流。

    参数:
    - data (WorkflowCreateSchema): 创建体。
    - auth (AuthSchema): 认证信息。

    返回:
    - JSONResponse: 成功响应，data 为新建工作流。
    """
    result_dict = await WorkflowService.create_workflow_service(auth=auth, data=data)
    log.info("创建工作流成功")
    return SuccessResponse(data=result_dict, msg="创建工作流成功")


@WorkflowRouter.put(
    "/update/{id}",
    summary="更新工作流",
    description="更新工作流及画布",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def update_workflow_controller(
    id: Annotated[int, Path(description="工作流ID")],
    data: WorkflowUpdateSchema,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:update"]))
    ],
) -> JSONResponse:
    """
    更新工作流及画布。

    参数:
    - id (int): 工作流 ID。
    - data (WorkflowUpdateSchema): 更新体。
    - auth (AuthSchema): 认证信息。

    返回:
    - JSONResponse: 成功响应，data 为更新后的工作流。
    """
    result_dict = await WorkflowService.update_workflow_service(auth=auth, id=id, data=data)
    log.info(f"更新工作流成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新工作流成功")


@WorkflowRouter.delete(
    "/delete",
    summary="删除工作流",
    description="批量删除工作流",
    response_model=ResponseSchema[None],
)
async def delete_workflow_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:delete"]))
    ],
) -> JSONResponse:
    """
    批量删除工作流。

    参数:
    - ids (list[int]): 工作流 ID 列表。
    - auth (AuthSchema): 认证信息。

    返回:
    - JSONResponse: 成功提示响应。
    """
    await WorkflowService.delete_workflow_service(auth=auth, ids=ids)
    log.info(f"删除工作流成功 {ids}")
    return SuccessResponse(msg="删除工作流成功")


@WorkflowRouter.post(
    "/publish/{id}",
    summary="发布工作流",
    description="校验 DAG 无环后标记为已发布，方可执行",
    response_model=ResponseSchema[WorkflowOutSchema],
)
async def publish_workflow_controller(
    id: Annotated[int, Path(description="工作流ID")],
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:update"]))
    ],
    body: Annotated[WorkflowPublishSchema | None, Body()] = None,
) -> JSONResponse:
    """
    校验 DAG 无环后发布工作流。

    参数:
    - id (int): 工作流 ID。
    - auth (AuthSchema): 认证信息。
    - body (WorkflowPublishSchema | None): 可选发布附加参数。

    返回:
    - JSONResponse: 成功响应，data 为发布后工作流。
    """
    result_dict = await WorkflowService.publish_workflow_service(auth=auth, id=id, body=body)
    log.info(f"发布工作流成功 {id}")
    return SuccessResponse(data=result_dict, msg="发布工作流成功")


@WorkflowRouter.post(
    "/execute",
    summary="执行工作流",
    description="使用 Prefect 按拓扑顺序执行已发布工作流",
    response_model=ResponseSchema[dict],
)
async def execute_workflow_controller(
    body: WorkflowExecuteSchema,
    auth: Annotated[
        AuthSchema, Depends(AuthPermission(["module_task:workflow:definition:execute"]))
    ],
) -> JSONResponse:
    """
    使用 Prefect 按拓扑顺序执行已发布工作流。

    参数:
    - body (WorkflowExecuteSchema): 工作流 ID 与变量等。
    - auth (AuthSchema): 认证信息。

    返回:
    - JSONResponse: 成功响应，data 为执行结果摘要。
    """
    result_dict = await WorkflowService.execute_workflow_service(auth=auth, body=body)
    log.info(f"执行工作流完成 workflow_id={body.workflow_id}")
    return SuccessResponse(data=result_dict, msg="执行工作流完成")
