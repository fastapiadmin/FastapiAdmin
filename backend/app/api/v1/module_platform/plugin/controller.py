from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core import cache_util
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.cache_util import cache
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

from .schema import (
    PluginCreateSchema,
    PluginInstallSchema,
    PluginOutSchema,
    PluginQueryParam,
    PluginUpdateSchema,
)
from .service import PluginService

PluginRouter = APIRouter(route_class=OperationLogRoute, prefix="/plugin", tags=["平台管理", "插件管理"])

_PLUGIN_NS = "plugin"


@PluginRouter.get(
    "/list",
    summary="插件列表",
    response_model=ResponseSchema[PageResultSchema[PluginOutSchema]],
)
@cache(expire=300, namespace=_PLUGIN_NS)
async def plugin_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[PluginQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:query"]))],
) -> JSONResponse:
    r = await PluginService(auth).page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=r, msg="查询成功")


@PluginRouter.get(
    "/detail/{id}",
    summary="插件详情",
    response_model=ResponseSchema[PluginOutSchema],
)
async def plugin_detail_controller(
    id: Annotated[int, Path()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:query"]))],
) -> JSONResponse:
    return SuccessResponse(data=await PluginService(auth).detail(id=id), msg="查询成功")


@PluginRouter.post(
    "/create",
    summary="创建插件",
    response_model=ResponseSchema[PluginOutSchema],
)
async def plugin_create_controller(
    data: PluginCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:create"]))],
) -> JSONResponse:
    r = await PluginService(auth).create(data=data)
    await cache_util.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(data=r, msg="创建成功")


@PluginRouter.put(
    "/update/{id}",
    summary="更新插件",
    response_model=ResponseSchema[PluginOutSchema],
)
async def plugin_update_controller(
    id: Annotated[int, Path()],
    data: PluginUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:update"]))],
) -> JSONResponse:
    r = await PluginService(auth).update(id=id, data=data)
    await cache_util.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(data=r, msg="更新成功")


@PluginRouter.delete(
    "/delete",
    summary="删除插件",
    response_model=ResponseSchema[None],
)
async def plugin_delete_controller(
    ids: Annotated[list[int], Body()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:delete"]))],
) -> JSONResponse:
    await PluginService(auth).delete(ids=ids)
    await cache_util.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(msg="删除成功")


@PluginRouter.get(
    "/marketplace",
    summary="插件市场",
    response_model=ResponseSchema[PageResultSchema[PluginOutSchema]],
)
@cache(expire=600, namespace=_PLUGIN_NS)
async def plugin_marketplace_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:query"]))],
    page: Annotated[PaginationQueryParam, Depends()],
    category: Annotated[str | None, Query(description="分类筛选")] = None,
) -> JSONResponse:
    r = await PluginService(auth).marketplace(page_no=page.page_no, page_size=page.page_size, category=category)
    return SuccessResponse(data=r, msg="查询成功")


@PluginRouter.post(
    "/install",
    summary="安装插件",
    response_model=ResponseSchema[None],
)
async def plugin_install_controller(
    data: PluginInstallSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:install"]))],
) -> JSONResponse:
    await PluginService(auth).install(plugin_id=data.plugin_id)
    await cache_util.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(msg="安装成功")


@PluginRouter.post(
    "/uninstall",
    summary="卸载插件",
    response_model=ResponseSchema[None],
)
async def plugin_uninstall_controller(
    data: PluginInstallSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:uninstall"]))],
) -> JSONResponse:
    await PluginService(auth).uninstall(plugin_id=data.plugin_id)
    await cache_util.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(msg="卸载成功")


@PluginRouter.post(
    "/toggle",
    summary="启用/禁用插件",
    response_model=ResponseSchema[None],
)
async def plugin_toggle_controller(
    data: PluginInstallSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:toggle"]))],
) -> JSONResponse:
    await PluginService(auth).toggle(plugin_id=data.plugin_id)
    await cache_util.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(msg="操作成功")


@PluginRouter.get(
    "/my",
    summary="我的插件",
    response_model=ResponseSchema[list[PluginOutSchema]],
)
@cache(expire=120, namespace=_PLUGIN_NS)
async def plugin_my_list_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:query"]))],
) -> JSONResponse:
    return SuccessResponse(data=await PluginService(auth).my_plugins(), msg="查询成功")


@PluginRouter.post(
    "/reload",
    summary="热重载插件路由",
    response_model=ResponseSchema[str],
)
async def plugin_reload_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:reload"]))],
) -> JSONResponse:
    msg = PluginService.reload()
    await cache_util.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(data=msg, msg="重载成功")
