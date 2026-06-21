from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse, StreamingResponse
from redis.asyncio.client import Redis

from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core import cache_util
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.cache_util import cache
from app.core.dependencies import AuthPermission, redis_getter
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import (
    DictDataCreateSchema,
    DictDataOutSchema,
    DictDataQueryParam,
    DictDataUpdateSchema,
    DictTypeCreateSchema,
    DictTypeOutSchema,
    DictTypeQueryParam,
    DictTypeUpdateSchema,
)
from .service import DictDataService, DictTypeService

DictRouter = APIRouter(route_class=OperationLogRoute, prefix="/dict", tags=["系统管理", "字典管理"])

_DICT_TYPE_NS = "dict_type"

@DictRouter.get(
    "/type/detail/{id}",
    summary="获取字典类型详情",
    response_model=ResponseSchema[DictTypeOutSchema],
)
async def get_type_detail_controller(
    id: Annotated[int, Path(description="字典类型ID", ge=1)],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_type:detail"]))],
) -> JSONResponse:
    result_dict = await DictTypeService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取字典类型详情成功")

@DictRouter.get(
    "/type/list",
    summary="查询字典类型",
    response_model=ResponseSchema[PageResultSchema[DictTypeOutSchema]],
)
async def get_type_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[DictTypeQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_type:query"]))],
) -> JSONResponse:
    result_dict = await DictTypeService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询字典类型列表成功")

@DictRouter.get(
    "/type/optionselect",
    summary="获取全部字典类型",
    response_model=ResponseSchema[list[DictTypeOutSchema]],
)
@cache(expire=300, namespace=_DICT_TYPE_NS)
async def get_type_optionselect_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_type:query"]))],
) -> JSONResponse:
    result_dict_list = await DictTypeService(auth).get_list()
    return SuccessResponse(data=result_dict_list, msg="获取字典类型列表成功")

@DictRouter.post(
    "/type/create",
    summary="创建字典类型",
    response_model=ResponseSchema[DictTypeOutSchema],
)
async def create_type_controller(
    data: DictTypeCreateSchema,
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_type:create"]))],
) -> JSONResponse:
    result_dict = await DictTypeService(auth).create(redis=redis, data=data)
    await cache_util.clear(namespace=_DICT_TYPE_NS)
    return SuccessResponse(data=result_dict, msg="创建字典类型成功")

@DictRouter.put(
    "/type/update/{id}",
    summary="修改字典类型",
    response_model=ResponseSchema[DictTypeOutSchema],
)
async def update_type_controller(
    data: DictTypeUpdateSchema,
    redis: Annotated[Redis, Depends(redis_getter)],
    id: Annotated[int, Path(description="字典类型ID", ge=1)],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_type:update"]))],
) -> JSONResponse:
    result_dict = await DictTypeService(auth).update(redis=redis, id=id, data=data)
    await cache_util.clear(namespace=_DICT_TYPE_NS)
    return SuccessResponse(data=result_dict, msg="修改字典类型成功")

@DictRouter.delete(
    "/type/delete",
    summary="删除字典类型",
    response_model=ResponseSchema[None],
)
async def delete_type_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_type:delete"]))],
) -> JSONResponse:
    await DictTypeService(auth).delete(redis=redis, ids=ids)
    await cache_util.clear(namespace=_DICT_TYPE_NS)
    return SuccessResponse(msg="删除字典类型成功")

@DictRouter.patch(
    "/type/status/batch",
    summary="批量修改字典类型状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_dict_type_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_type:patch"]))],
) -> JSONResponse:
    await DictTypeService(auth).set_available(data=data)
    await cache_util.clear(namespace=_DICT_TYPE_NS)
    return SuccessResponse(msg="批量修改字典类型状态成功")

@DictRouter.post(
    "/type/export",
    summary="导出字典类型",
    response_model=ResponseSchema[None],
)
async def export_type_list_controller(
    search: Annotated[DictTypeQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_type:export"]))],
) -> StreamingResponse:
    # 获取全量数据并转为dict列表
    result_dict_list = await DictTypeService(auth).get_list(search=search)
    export_data = [item.model_dump() for item in result_dict_list]
    export_result = DictTypeService.export(data_list=export_data)

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=dict_type.xlsx"},
    )

@DictRouter.get(
    "/data/detail/{id}",
    summary="获取字典数据详情",
    response_model=ResponseSchema[DictDataOutSchema],
)
async def get_data_detail_controller(
    id: Annotated[int, Path(description="字典数据ID", ge=1)],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_data:detail"]))],
) -> JSONResponse:
    result_dict = await DictDataService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取字典数据详情成功")

@DictRouter.get(
    "/data/list",
    summary="查询字典数据",
    response_model=ResponseSchema[PageResultSchema[DictDataOutSchema]],
)
async def get_data_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[DictDataQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_data:query"]))],
) -> JSONResponse:
    order_by = [{"order": "asc"}]
    if page.order_by:
        order_by = page.order_by
    result_dict = await DictDataService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询字典数据列表成功")

@DictRouter.post(
    "/data/create",
    summary="创建字典数据",
    response_model=ResponseSchema[DictDataOutSchema],
)
async def create_data_controller(
    data: DictDataCreateSchema,
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_data:create"]))],
) -> JSONResponse:
    result_dict = await DictDataService(auth).create(redis=redis, data=data)
    return SuccessResponse(data=result_dict, msg="创建字典数据成功")

@DictRouter.put(
    "/data/update/{id}",
    summary="修改字典数据",
    response_model=ResponseSchema[DictDataOutSchema],
)
async def update_data_controller(
    data: DictDataUpdateSchema,
    redis: Annotated[Redis, Depends(redis_getter)],
    id: Annotated[int, Path(description="字典数据ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_data:update"]))],
) -> JSONResponse:
    result_dict = await DictDataService(auth).update(redis=redis, id=id, data=data)
    return SuccessResponse(data=result_dict, msg="修改字典数据成功")

@DictRouter.delete(
    "/data/delete",
    summary="删除字典数据",
    response_model=ResponseSchema[None],
)
async def delete_data_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_data:delete"]))],
) -> JSONResponse:
    await DictDataService(auth).delete(redis=redis, ids=ids)
    return SuccessResponse(msg="删除字典数据成功")

@DictRouter.patch(
    "/data/status/batch",
    summary="批量修改字典数据状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_dict_data_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_data:patch"]))],
) -> JSONResponse:
    await DictDataService(auth).set_available(data=data)
    return SuccessResponse(msg="批量修改字典数据状态成功")

@DictRouter.post(
    "/data/export",
    summary="导出字典数据",
    response_model=ResponseSchema[None],
)
async def export_data_list_controller(
    search: Annotated[DictDataQueryParam, Depends()],
    page: Annotated[PaginationQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dict_data:export"]))],
) -> StreamingResponse:
    result_dict_list = await DictDataService(auth).get_list(search=search, order_by=page.order_by)
    export_data = [item.model_dump() for item in result_dict_list]
    export_result = DictDataService.export(data_list=export_data)

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=dice_data.xlsx"},
    )

@DictRouter.get(
    "/data/info/{dict_type}",
    summary="根据字典类型获取数据",
    response_model=ResponseSchema[list[DictDataOutSchema]],
)
async def get_init_dict_data_controller(dict_type: str, redis: Annotated[Redis, Depends(redis_getter)]) -> JSONResponse:
    dict_data_query_result = await DictDataService.get_init_cache(redis=redis, dict_type=dict_type, tenant_id=1)

    return SuccessResponse(data=dict_data_query_result, msg="获取初始化字典数据成功")
