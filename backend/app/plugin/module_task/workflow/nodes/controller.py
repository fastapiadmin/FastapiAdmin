from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .schema import (
    WorkflowNodeTypeCreateSchema,
    WorkflowNodeTypeOutSchema,
    WorkflowNodeTypeQueryParam,
    WorkflowNodeTypeUpdateSchema,
)
from .service import WorkflowNodeTypeService

WorkflowNodeTypeRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/workflow/node-type",
    tags=["工作流节点类型"],
)


@WorkflowNodeTypeRouter.get(
    "/options",
    summary="节点类型选项",
    response_model=ResponseSchema[list[dict]],
)
async def get_workflow_node_type_options_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:node-type:query"]))],
) -> JSONResponse:
    service = WorkflowNodeTypeService(auth)
    result = await service.get_options()
    return SuccessResponse(data=result, msg="获取节点类型选项成功")


@WorkflowNodeTypeRouter.get(
    "/detail/{id}",
    summary="节点类型详情",
    response_model=ResponseSchema[WorkflowNodeTypeOutSchema],
)
async def get_workflow_node_type_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:node-type:query"]))],
    id: Annotated[int, Path(description="ID")],
) -> JSONResponse:
    service = WorkflowNodeTypeService(auth)
    result_dict = await service.get_detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取节点类型详情成功")


@WorkflowNodeTypeRouter.get(
    "/list",
    summary="节点类型列表",
    response_model=ResponseSchema[PageResultSchema[WorkflowNodeTypeOutSchema]],
)
async def get_workflow_node_type_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:node-type:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[WorkflowNodeTypeQueryParam, Query(description="查询参数")],
) -> JSONResponse:
    order_by = [{"sort_order": "asc"}, {"id": "asc"}]
    if page.order_by:
        order_by = page.order_by
    service = WorkflowNodeTypeService(auth)
    result_dict = await service.get_page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询节点类型列表成功")


@WorkflowNodeTypeRouter.post(
    "/create",
    summary="创建节点类型",
    response_model=ResponseSchema[WorkflowNodeTypeOutSchema],
)
async def create_workflow_node_type_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:node-type:create"]))],
    data: Annotated[WorkflowNodeTypeCreateSchema, Body(description="创建节点类型参数")],
) -> JSONResponse:
    service = WorkflowNodeTypeService(auth)
    result_dict = await service.create(data=data)
    return SuccessResponse(data=result_dict, msg="创建节点类型成功")


@WorkflowNodeTypeRouter.put(
    "/update/{id}",
    summary="更新节点类型",
    response_model=ResponseSchema[WorkflowNodeTypeOutSchema],
)
async def update_workflow_node_type_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:node-type:update"]))],
    id: Annotated[int, Path(description="节点类型ID")],
    data: Annotated[WorkflowNodeTypeUpdateSchema, Body(description="更新节点类型参数")],
) -> JSONResponse:
    service = WorkflowNodeTypeService(auth)
    result_dict = await service.update(id=id, data=data)
    return SuccessResponse(data=result_dict, msg="更新节点类型成功")


@WorkflowNodeTypeRouter.delete(
    "/delete",
    summary="删除节点类型",
    response_model=ResponseSchema[None],
)
async def delete_workflow_node_type_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:node-type:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    service = WorkflowNodeTypeService(auth)
    await service.delete(ids=ids)
    return SuccessResponse(msg="删除节点类型成功")


@WorkflowNodeTypeRouter.get(
    "/select",
    summary="节点类型选择列表",
    response_model=ResponseSchema[list[dict]],
)
async def get_workflow_node_type_select_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:workflow:node-type:query"]))],
) -> JSONResponse:
    service = WorkflowNodeTypeService(auth)
    result = await service.get_select()
    return SuccessResponse(data=result, msg="获取节点类型选择列表成功")
