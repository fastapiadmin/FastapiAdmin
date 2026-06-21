from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core import cache_util
from app.core.base_schema import AuthSchema, BatchSetAvailable
from app.core.cache_util import cache
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

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
    search: Annotated[MenuQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:query"]))],
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
    id: Annotated[int, Path(description="菜单ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:detail"]))],
) -> JSONResponse:
    result_dict = await MenuService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="查询菜单详情成功")


@MenuRouter.post(
    "/create",
    summary="创建菜单",
    response_model=ResponseSchema[MenuOutSchema],
)
async def create_obj_controller(
    data: MenuCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:create"]))],
) -> JSONResponse:
    result_dict = await MenuService(auth).create(data=data)
    await cache_util.clear(namespace=_MENU_NS)
    return SuccessResponse(data=result_dict, msg="创建菜单成功")


@MenuRouter.put(
    "/update/{id}",
    summary="修改菜单",
    response_model=ResponseSchema[MenuOutSchema],
)
async def update_obj_controller(
    data: MenuUpdateSchema,
    id: Annotated[int, Path(description="菜单ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:update"]))],
) -> JSONResponse:
    result_dict = await MenuService(auth).update(id=id, data=data)
    await cache_util.clear(namespace=_MENU_NS)
    return SuccessResponse(data=result_dict, msg="修改菜单成功")


@MenuRouter.delete(
    "/delete",
    summary="删除菜单",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:delete"]))],
) -> JSONResponse:
    await MenuService(auth).delete(ids=ids)
    await cache_util.clear(namespace=_MENU_NS)
    return SuccessResponse(msg="删除菜单成功")


@MenuRouter.patch(
    "/status/batch",
    summary="批量修改菜单状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:menu:patch"]))],
) -> JSONResponse:
    await MenuService(auth).set_available(data=data)
    await cache_util.clear(namespace=_MENU_NS)
    return SuccessResponse(msg="批量修改菜单状态成功")
