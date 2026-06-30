from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import AuthSchema, PageResultSchema
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
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
    search: Annotated[PluginQueryParam, Query(description="查询参数")],
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
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:query"]))],
    id: Annotated[int, Path(description="插件ID", ge=1)],
) -> JSONResponse:
    return SuccessResponse(data=await PluginService(auth).detail(id=id), msg="查询成功")


@PluginRouter.post(
    "/create",
    summary="创建插件",
    response_model=ResponseSchema[PluginOutSchema],
)
async def plugin_create_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:create"]))],
    data: Annotated[PluginCreateSchema, Body(description="插件创建参数")],
) -> JSONResponse:
    r = await PluginService(auth).create(data=data)
    await FastAPICache.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(data=r, msg="创建成功")


@PluginRouter.put(
    "/update/{id}",
    summary="更新插件",
    response_model=ResponseSchema[PluginOutSchema],
)
async def plugin_update_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:update"]))],
    id: Annotated[int, Path(description="插件ID", ge=1)],
    data: Annotated[PluginUpdateSchema, Body(description="插件更新参数")],
) -> JSONResponse:
    r = await PluginService(auth).update(id=id, data=data)
    await FastAPICache.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(data=r, msg="更新成功")


@PluginRouter.delete(
    "/delete",
    summary="删除插件",
    response_model=ResponseSchema[None],
)
async def plugin_delete_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:delete"]))],
    ids: Annotated[list[int], Body(description="插件ID列表")],
) -> JSONResponse:
    await PluginService(auth).delete(ids=ids)
    await FastAPICache.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(msg="删除成功")


@PluginRouter.get(
    "/marketplace",
    summary="插件市场",
    response_model=ResponseSchema[PageResultSchema[PluginOutSchema]],
)
@cache(expire=600, namespace=_PLUGIN_NS)
async def plugin_marketplace_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:query"]))],
    page: Annotated[PaginationQueryParam, Query(description="分页参数")],
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
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:install"]))],
    data: Annotated[PluginInstallSchema, Body(description="插件安装参数")],
) -> JSONResponse:
    await PluginService(auth).install(plugin_id=data.plugin_id)
    await FastAPICache.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(msg="安装成功")


@PluginRouter.post(
    "/uninstall",
    summary="卸载插件",
    response_model=ResponseSchema[None],
)
async def plugin_uninstall_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:uninstall"]))],
    data: Annotated[PluginInstallSchema, Body(description="插件卸载参数")],
) -> JSONResponse:
    await PluginService(auth).uninstall(plugin_id=data.plugin_id)
    await FastAPICache.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(msg="卸载成功")


@PluginRouter.post(
    "/toggle",
    summary="启用/禁用插件",
    response_model=ResponseSchema[None],
)
async def plugin_toggle_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_platform:plugin:toggle"]))],
    data: Annotated[PluginInstallSchema, Body(description="插件启用/禁用参数")],
) -> JSONResponse:
    await PluginService(auth).toggle(plugin_id=data.plugin_id)
    await FastAPICache.clear(namespace=_PLUGIN_NS)
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
    dependencies=[Depends(AuthPermission(["module_platform:plugin:reload"]))],
)
async def plugin_reload_controller() -> JSONResponse:
    msg = PluginService.reload()
    await FastAPICache.clear(namespace=_PLUGIN_NS)
    return SuccessResponse(data=msg, msg="重载成功")
