from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core import cache_util
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, BatchSetAvailable, PageResultSchema
from app.core.cache_util import cache
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .schema import (
    PackageCreateSchema,
    PackageMenuSetSchema,
    PackageOutSchema,
    PackagePluginSetSchema,
    PackageQueryParam,
    PackageUpdateSchema,
)
from .service import PackageService

PackageRouter = APIRouter(route_class=OperationLogRoute, prefix="/package", tags=["平台管理", "套餐管理"])

_PKG_NS = "package"

@PackageRouter.get(
    "/detail/{id}",
    summary="获取套餐详情",
    response_model=ResponseSchema[PackageOutSchema],
)
@cache(expire=300, namespace=_PKG_NS)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="套餐ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:query"]))],
) -> JSONResponse:
    result_dict = await PackageService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="获取套餐详情成功")

@PackageRouter.get(
    "/list",
    summary="获取套餐列表",
    response_model=ResponseSchema[PageResultSchema[PackageOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[PackageQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:query"]))],
) -> JSONResponse:
    result_dict = await PackageService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询成功")

@PackageRouter.post(
    "/create",
    summary="创建套餐",
    response_model=ResponseSchema[PackageOutSchema],
)
async def create_obj_controller(
    data: Annotated[PackageCreateSchema, Body(description="套餐信息")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:create"]))],
) -> JSONResponse:
    result_dict = await PackageService(auth).create(data=data)
    await cache_util.clear(namespace=_PKG_NS)
    return SuccessResponse(data=result_dict, msg="创建成功")

@PackageRouter.put(
    "/update/{id}",
    summary="更新套餐",
    response_model=ResponseSchema[PackageOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="套餐ID")],
    data: Annotated[PackageUpdateSchema, Body(description="套餐信息")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:update"]))],
) -> JSONResponse:
    result_dict = await PackageService(auth).update(id=id, data=data)
    await cache_util.clear(namespace=_PKG_NS)
    return SuccessResponse(data=result_dict, msg="更新成功")

@PackageRouter.delete(
    "/delete",
    summary="删除套餐",
    response_model=ResponseSchema,
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:delete"]))],
) -> JSONResponse:
    await PackageService(auth).delete(ids=ids)
    await cache_util.clear(namespace=_PKG_NS)
    return SuccessResponse(msg="删除成功")

@PackageRouter.patch(
    "/status/batch",
    summary="批量修改状态",
    response_model=ResponseSchema,
)
async def set_available_controller(
    data: Annotated[BatchSetAvailable, Body(description="状态设置")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:update"]))],
) -> JSONResponse:
    for id in data.ids:
        await PackageService(auth).update(id=id, data=PackageUpdateSchema(status=data.status))
    await cache_util.clear(namespace=_PKG_NS)
    return SuccessResponse(msg="状态设置成功")

@PackageRouter.get(
    "/menus/{package_id}",
    summary="获取套餐菜单",
    response_model=ResponseSchema[list[int]],
)
async def get_menus_controller(
    package_id: Annotated[int, Path(description="套餐ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:query"]))],
) -> JSONResponse:
    result = await PackageService(auth).get_menus(package_id=package_id)
    return SuccessResponse(data=result, msg="获取成功")

@PackageRouter.post(
    "/menus/{package_id}/set",
    summary="设置套餐菜单",
    response_model=ResponseSchema,
)
async def set_menus_controller(
    package_id: Annotated[int, Path(description="套餐ID")],
    data: Annotated[PackageMenuSetSchema, Body(description="菜单列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:update"]))],
) -> JSONResponse:
    await PackageService(auth).set_menus(package_id=package_id, data=data)
    return SuccessResponse(msg="设置成功")

@PackageRouter.get(
    "/plugins/{package_id}",
    summary="获取套餐插件",
    response_model=ResponseSchema[list[int]],
)
async def get_plugins_controller(
    package_id: Annotated[int, Path(description="套餐ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:query"]))],
) -> JSONResponse:
    result = await PackageService(auth).get_plugins(package_id=package_id)
    return SuccessResponse(data=result, msg="获取成功")

@PackageRouter.post(
    "/plugins/{package_id}/set",
    summary="设置套餐插件",
    response_model=ResponseSchema,
)
async def set_plugins_controller(
    package_id: Annotated[int, Path(description="套餐ID")],
    data: Annotated[PackagePluginSetSchema, Body(description="插件列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:update"]))],
) -> JSONResponse:
    await PackageService(auth).set_plugins(package_id=package_id, data=data)
    return SuccessResponse(msg="设置成功")
