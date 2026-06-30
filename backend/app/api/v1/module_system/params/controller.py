from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse, StreamingResponse
from redis.asyncio.client import Redis

from app.common.response import ResponseSchema, StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.dependencies import AuthPermission, redis_getter
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from .schema import ParamsCreateSchema, ParamsOutSchema, ParamsQueryParam, ParamsUpdateSchema
from .service import ParamsService

ParamsRouter = APIRouter(route_class=OperationLogRoute, prefix="/param", tags=["系统管理", "参数管理"])

@ParamsRouter.get(
    "/detail/{id}",
    summary="获取参数详情",
    response_model=ResponseSchema[ParamsOutSchema],
)
async def get_param_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:param:detail"]))],
    id: Annotated[int, Path(description="参数ID")],
) -> JSONResponse:
    result_dict = await ParamsService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取参数详情成功")

@ParamsRouter.get(
    "/key/{config_key}",
    summary="根据配置键获取参数详情",
    response_model=ResponseSchema[ParamsOutSchema],
)
async def get_param_by_key_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:param:query"]))],
    config_key: Annotated[str, Path(description="配置键")],
) -> JSONResponse:
    result_dict = await ParamsService(auth).get_by_key(config_key=config_key)
    return SuccessResponse(data=result_dict, msg="根据配置键获取参数详情成功")

@ParamsRouter.get(
    "/value/{config_key}",
    summary="根据配置键获取参数值",
    response_model=ResponseSchema[ParamsOutSchema],
)
async def get_config_value_by_key_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:param:query"]))],
    config_key: Annotated[str, Path(description="配置键")],
) -> JSONResponse:
    result_value = await ParamsService(auth).get_config_value_by_key(config_key=config_key)
    return SuccessResponse(data=result_value, msg="根据配置键获取参数值成功")

@ParamsRouter.get(
    "/list",
    summary="获取参数列表",
    response_model=ResponseSchema[PageResultSchema[ParamsOutSchema]],
)
async def get_param_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:param:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[ParamsQueryParam, Query(description="参数查询参数")],
) -> JSONResponse:
    result_dict = await ParamsService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询参数列表成功")

@ParamsRouter.post(
    "/create",
    summary="创建参数",
    response_model=ResponseSchema[ParamsOutSchema],
)
async def create_param_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:param:create"]))],
    data: Annotated[ParamsCreateSchema, Body(description="参数创建参数")],
) -> JSONResponse:
    result_dict = await ParamsService(auth).create(redis=redis, data=data)
    return SuccessResponse(data=result_dict, msg="创建参数成功")

@ParamsRouter.put(
    "/update/{id}",
    summary="修改参数",
    response_model=ResponseSchema[ParamsOutSchema],
)
async def update_param_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:param:update"]))],
    id: Annotated[int, Path(description="参数ID")],
    data: Annotated[ParamsUpdateSchema, Body(description="参数修改参数")],
) -> JSONResponse:
    result_dict = await ParamsService(auth).update(redis=redis, id=id, data=data)
    return SuccessResponse(data=result_dict, msg="更新参数成功")

@ParamsRouter.delete(
    "/delete",
    summary="删除参数",
    response_model=ResponseSchema[ParamsOutSchema],
)
async def delete_param_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:param:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    await ParamsService(auth).delete(redis=redis, ids=ids)
    return SuccessResponse(msg="删除参数成功")

@ParamsRouter.patch(
    "/status/batch",
    summary="批量设置参数状态",
    response_model=ResponseSchema,
)
async def batch_set_status_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:param:patch"]))],
    ids: Annotated[list[int], Body(description="参数ID列表")],
    status: Annotated[int, Body(description="状态值")],
) -> JSONResponse:
    await ParamsService(auth).batch_set_status(ids=ids, status=status)
    return SuccessResponse(msg="批量设置参数状态成功")

@ParamsRouter.get(
    "/export",
    summary="导出参数",
    response_model=ResponseSchema[None],
)
async def export_param_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:param:export"]))],
    search: Annotated[ParamsQueryParam, Query(description="参数查询参数")],
) -> StreamingResponse:
    result_dict_list = await ParamsService(auth).get_list(search=search)
    export_data = [item.model_dump() for item in result_dict_list]
    export_result = ParamsService.export(data_list=export_data)

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=params.xlsx"},
    )

@ParamsRouter.get(
    "/info",
    summary="获取初始化缓存参数",
    response_model=ResponseSchema[list[ParamsOutSchema]],
)
async def get_init_config_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    result_dict = await ParamsService.get_init_cache(redis=redis, tenant_id=1)
    return SuccessResponse(data=result_dict, msg="获取初始化缓存参数成功")
