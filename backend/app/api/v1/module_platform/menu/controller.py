from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_schema import AuthSchema, BatchSetAvailable
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from .schema import MenuCreateSchema, MenuOutSchema, MenuQueryParam, MenuUpdateSchema
from .service import MenuService

MenuRouter = APIRouter(route_class=OperationLogRoute, prefix="/menu", tags=["平台管理", "菜单管理"])

_MENU_NS = "menu"


@MenuRouter.get(
    "/tree",
    summary="查询菜单树",
    response_model=ResponseSchema[list[MenuOutSchema]],
)
@cache(expire=300, namespace=_MENU_NS)
async def get_menu_tree_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:query"]))],
    search: Annotated[MenuQueryParam, Query(description="菜单查询参数")],
) -> JSONResponse:
    order_by = [{"order": "asc"}]
    result_dict_tree = await MenuService(auth).tree(search=search, order_by=order_by)
    return SuccessResponse(data=result_dict_tree, msg="查询菜单树成功")


@MenuRouter.get(
    "/detail/{id}",
    summary="查询菜单详情",
    response_model=ResponseSchema[MenuOutSchema],
)
async def get_obj_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:detail"]))],
    id: Annotated[int, Path(description="菜单ID", ge=1)],
) -> JSONResponse:
    result_dict = await MenuService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="查询菜单详情成功")


@MenuRouter.post(
    "/create",
    summary="创建菜单",
    response_model=ResponseSchema[MenuOutSchema],
)
async def create_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:create"]))],
    data: Annotated[MenuCreateSchema, Body(description="菜单创建参数")],
) -> JSONResponse:
    result_dict = await MenuService(auth).create(data=data)
    await FastAPICache.clear(namespace=_MENU_NS)
    return SuccessResponse(data=result_dict, msg="创建菜单成功")


@MenuRouter.put(
    "/update/{id}",
    summary="修改菜单",
    response_model=ResponseSchema[MenuOutSchema],
)
async def update_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:update"]))],
    id: Annotated[int, Path(description="菜单ID", ge=1)],
    data: Annotated[MenuUpdateSchema, Body(description="菜单修改参数")],
) -> JSONResponse:
    result_dict = await MenuService(auth).update(id=id, data=data)
    await FastAPICache.clear(namespace=_MENU_NS)
    return SuccessResponse(data=result_dict, msg="修改菜单成功")


@MenuRouter.delete(
    "/delete",
    summary="删除菜单",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:delete"]))],
    ids: Annotated[list[int], Body(description="菜单ID列表")],
) -> JSONResponse:
    await MenuService(auth).delete(ids=ids)
    await FastAPICache.clear(namespace=_MENU_NS)
    return SuccessResponse(msg="删除菜单成功")


@MenuRouter.patch(
    "/status/batch",
    summary="批量修改菜单状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:patch"]))],
    data: Annotated[BatchSetAvailable, Body(description="批量修改菜单状态参数")],
) -> JSONResponse:
    await MenuService(auth).set_available(data=data)
    await FastAPICache.clear(namespace=_MENU_NS)
    return SuccessResponse(msg="批量修改菜单状态成功")
