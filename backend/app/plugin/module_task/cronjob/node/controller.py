from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .schema import (
    NodeCreateSchema,
    NodeExecuteSchema,
    NodeOutSchema,
    NodeQueryParam,
    NodeUpdateSchema,
)
from .service import NodeService

NodeRouter = APIRouter(route_class=OperationLogRoute, prefix="/cronjob/node", tags=["任务调度", "节点管理"])


@NodeRouter.get(
    "/options",
    summary="获取定时任务节点列表",
    response_model=ResponseSchema[list[dict]],
)
async def get_node_options_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:node:query"]))],
) -> JSONResponse:
    service = NodeService(auth)
    result = await service.options()
    return SuccessResponse(data=result, msg="获取定时任务节点选项成功")


@NodeRouter.get(
    "/detail/{id}",
    summary="获取节点详情",
    response_model=ResponseSchema[NodeOutSchema],
)
async def get_obj_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:node:detail"]))],
    id: Annotated[int, Path(description="节点ID")],
) -> JSONResponse:
    service = NodeService(auth)
    result_dict = await service.detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取节点详情成功")


@NodeRouter.get(
    "/list",
    summary="查询节点",
    response_model=ResponseSchema[PageResultSchema[NodeOutSchema]],
)
async def get_obj_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:node:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[NodeQueryParam, Query(description="查询参数")],
) -> JSONResponse:
    service = NodeService(auth)
    result_dict = await service.page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询节点列表成功")


@NodeRouter.post(
    "/create",
    summary="创建节点",
    response_model=ResponseSchema[NodeOutSchema],
)
async def create_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:node:create"]))],
    data: Annotated[NodeCreateSchema, Body(description="创建节点参数")],
) -> JSONResponse:
    service = NodeService(auth)
    result_dict = await service.create(data=data)
    return SuccessResponse(data=result_dict, msg="创建节点成功")


@NodeRouter.put(
    "/update/{id}",
    summary="修改节点",
    response_model=ResponseSchema[NodeOutSchema],
)
async def update_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:node:update"]))],
    id: Annotated[int, Path(description="节点ID")],
    data: Annotated[NodeUpdateSchema, Body(description="修改节点参数")],
) -> JSONResponse:
    service = NodeService(auth)
    result_dict = await service.update(id=id, data=data)
    return SuccessResponse(data=result_dict, msg="修改节点成功")


@NodeRouter.delete(
    "/delete",
    summary="删除节点",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:node:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    service = NodeService(auth)
    await service.delete(ids=ids)
    return SuccessResponse(msg="删除节点成功")


@NodeRouter.delete(
    "/clear",
    summary="清空节点",
    response_model=ResponseSchema[None],
)
async def clear_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:node:delete"]))],
) -> JSONResponse:
    service = NodeService(auth)
    await service.clear()
    return SuccessResponse(msg="清空节点成功")


@NodeRouter.post(
    "/execute/{id}",
    summary="调试节点",
    response_model=ResponseSchema[dict],
)
async def execute_job_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:node:execute"]))],
    id: Annotated[int, Path(description="节点ID")],
    data: Annotated[NodeExecuteSchema, Body(description="调试节点参数")],
) -> JSONResponse:
    service = NodeService(auth)
    result = await service.execute(id=id, execute_data=data)
    return SuccessResponse(data=result, msg="调试节点成功")


@NodeRouter.patch(
    "/status/batch",
    summary="批量设置节点状态",
    response_model=ResponseSchema[None],
)
async def batch_set_status_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:cronjob:node:update"]))],
    ids: Annotated[list[int], Body(description="节点ID列表")],
    status: Annotated[int, Body(description="状态值")],
) -> JSONResponse:
    service = NodeService(auth)
    await service.batch_set_status(ids=ids, status=status)
    return SuccessResponse(msg="批量设置节点状态成功")
