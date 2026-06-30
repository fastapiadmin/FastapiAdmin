from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import (
    PositionCreateSchema,
    PositionOutSchema,
    PositionQueryParam,
    PositionUpdateSchema,
)
from .service import PositionService

PositionRouter = APIRouter(route_class=OperationLogRoute, prefix="/position", tags=["系统管理", "岗位管理"])

_POS_NS = "position"

@PositionRouter.get(
    "/list",
    summary="查询岗位",
    response_model=ResponseSchema[PageResultSchema[PositionOutSchema]],
)
@cache(expire=300, namespace=_POS_NS)
async def get_obj_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[PositionQueryParam, Query(description="岗位查询参数")],
) -> JSONResponse:
    order_by = [{"order": "asc"}]
    if page.order_by:
        order_by = page.order_by
    result_dict = await PositionService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询岗位列表成功")

@PositionRouter.get(
    "/detail/{id}",
    summary="查询岗位详情",
    response_model=ResponseSchema[PositionOutSchema],
)
async def get_obj_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:detail"]))],
    id: Annotated[int, Path(description="岗位ID")],
) -> JSONResponse:
    result_dict = await PositionService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取岗位详情成功")

@PositionRouter.post(
    "/create",
    summary="创建岗位",
    response_model=ResponseSchema[PositionOutSchema],
)
async def create_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:create"]))],
    data: Annotated[PositionCreateSchema, Body(description="岗位创建参数")],
) -> JSONResponse:
    result_dict = await PositionService(auth).create(data=data)
    await FastAPICache.clear(namespace=_POS_NS)
    return SuccessResponse(data=result_dict, msg="创建岗位成功")

@PositionRouter.put(
    "/update/{id}",
    summary="修改岗位",
    response_model=ResponseSchema[PositionOutSchema],
)
async def update_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:update"]))],
    id: Annotated[int, Path(description="岗位ID")],
    data: Annotated[PositionUpdateSchema, Body(description="岗位修改参数")],
) -> JSONResponse:
    result_dict = await PositionService(auth).update(id=id, data=data)
    await FastAPICache.clear(namespace=_POS_NS)
    return SuccessResponse(data=result_dict, msg="修改岗位成功")

@PositionRouter.delete(
    "/delete",
    summary="删除岗位",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    await PositionService(auth).delete(ids=ids)
    await FastAPICache.clear(namespace=_POS_NS)
    return SuccessResponse(msg="删除岗位成功")

@PositionRouter.patch(
    "/status/batch",
    summary="批量修改岗位状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:patch"]))],
    data: Annotated[BatchSetAvailable, Body(description="批量修改岗位状态参数")],
) -> JSONResponse:
    await PositionService(auth).set_available(data=data)
    await FastAPICache.clear(namespace=_POS_NS)
    return SuccessResponse(msg="批量修改岗位状态成功")

@PositionRouter.get(
    "/export",
    summary="导出岗位",
    response_model=ResponseSchema[None],
)
async def export_obj_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:export"]))],
    search: Annotated[PositionQueryParam, Query(description="岗位查询参数")],
) -> StreamingResponse:
    position_query_result = await PositionService(auth).get_list(search=search)
    position_export_result = PositionService.export_list(position_list=position_query_result)

    return StreamResponse(
        data=bytes2file_response(position_export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=position.xlsx"},
    )
