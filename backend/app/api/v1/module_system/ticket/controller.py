from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path, Body
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .schema import (
    TicketBatchSchema,
    TicketCreateSchema,
    TicketOutSchema,
    TicketQueryParam,
    TicketUpdateSchema,
)
from .service import TicketService

TicketRouter = APIRouter(route_class=OperationLogRoute, prefix="/ticket", tags=["系统管理", "工单管理"])

@TicketRouter.get("/list", summary="工单列表", response_model=ResponseSchema[PageResultSchema[TicketOutSchema]])
async def ticket_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:ticket:list"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[TicketQueryParam, Query(description="工单查询参数")],
) -> JSONResponse:
    result = await TicketService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result, msg="查询成功")

@TicketRouter.get("/detail/{id}", summary="获取工单详情", response_model=ResponseSchema[TicketOutSchema])
async def ticket_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:ticket:detail"]))],
    id: Annotated[int, Path(description="工单ID")],
) -> JSONResponse:
    result = await TicketService(auth).detail(id=id)
    return SuccessResponse(data=result, msg="查询成功")

@TicketRouter.post("/create", summary="创建工单", response_model=ResponseSchema[TicketOutSchema])
async def ticket_create_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:ticket:create"]))],
    data: Annotated[TicketCreateSchema, Body(description="工单创建参数")],
) -> JSONResponse:
    result = await TicketService(auth).create(data=data)
    return SuccessResponse(data=result, msg="创建成功")

@TicketRouter.put("/update/{id}", summary="更新工单", response_model=ResponseSchema[TicketOutSchema])
async def ticket_update_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:ticket:update"]))],
    id: Annotated[int, Path(description="工单ID")],
    data: Annotated[TicketUpdateSchema, Body(description="工单更新参数")],
) -> JSONResponse:
    result = await TicketService(auth).update(id=id, data=data)
    return SuccessResponse(data=result, msg="更新成功")

@TicketRouter.put("/batch", summary="批量更新工单", response_model=ResponseSchema)
async def ticket_batch_update_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:ticket:update"]))],
    data: Annotated[TicketBatchSchema, Body(description="工单批量更新参数")],
) -> JSONResponse:
    await TicketService(auth).batch(data=data)
    return SuccessResponse(msg="批量操作成功")

@TicketRouter.delete("/delete", summary="删除工单", response_model=ResponseSchema[None])
async def ticket_delete_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:ticket:delete"]))],
    ids: Annotated[list[int], Body(description="工单ID列表")],
) -> JSONResponse:
    await TicketService(auth).delete(ids=ids)
    return SuccessResponse(msg="删除成功")
