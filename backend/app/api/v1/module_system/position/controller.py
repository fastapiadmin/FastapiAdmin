from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core import cache_util
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.cache_util import cache
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
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[PositionQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:query"]))],
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
    id: Annotated[int, Path(description="岗位ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:detail"]))],
) -> JSONResponse:
    result_dict = await PositionService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取岗位详情成功")

@PositionRouter.post(
    "/create",
    summary="创建岗位",
    response_model=ResponseSchema[PositionOutSchema],
)
async def create_obj_controller(
    data: PositionCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:create"]))],
) -> JSONResponse:
    result_dict = await PositionService(auth).create(data=data)
    await cache_util.clear(namespace=_POS_NS)
    return SuccessResponse(data=result_dict, msg="创建岗位成功")

@PositionRouter.put(
    "/update/{id}",
    summary="修改岗位",
    response_model=ResponseSchema[PositionOutSchema],
)
async def update_obj_controller(
    data: PositionUpdateSchema,
    id: Annotated[int, Path(description="岗位ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:update"]))],
) -> JSONResponse:
    result_dict = await PositionService(auth).update(id=id, data=data)
    await cache_util.clear(namespace=_POS_NS)
    return SuccessResponse(data=result_dict, msg="修改岗位成功")

@PositionRouter.delete(
    "/delete",
    summary="删除岗位",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:delete"]))],
) -> JSONResponse:
    await PositionService(auth).delete(ids=ids)
    await cache_util.clear(namespace=_POS_NS)
    return SuccessResponse(msg="删除岗位成功")

@PositionRouter.patch(
    "/status/batch",
    summary="批量修改岗位状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:patch"]))],
) -> JSONResponse:
    await PositionService(auth).set_available(data=data)
    await cache_util.clear(namespace=_POS_NS)
    return SuccessResponse(msg="批量修改岗位状态成功")

@PositionRouter.get(
    "/export",
    summary="导出岗位",
    response_model=ResponseSchema[None],
)
async def export_obj_list_controller(
    search: Annotated[PositionQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:position:export"]))],
) -> StreamingResponse:
    position_query_result = await PositionService(auth).get_list(search=search)
    position_export_result = PositionService.export_list(position_list=position_query_result)

    return StreamResponse(
        data=bytes2file_response(position_export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=position.xlsx"},
    )
