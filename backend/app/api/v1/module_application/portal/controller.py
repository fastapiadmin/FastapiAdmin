from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchSetAvailable
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    ApplicationCreateSchema,
    ApplicationOutSchema,
    ApplicationQueryParam,
    ApplicationUpdateSchema,
    PluginInfoOut,
)
from .service import ApplicationService

PortalRouter = APIRouter(route_class=OperationLogRoute, prefix="/portal", tags=["应用管理"])


@PortalRouter.get(
    "/detail/{id}",
    summary="获取应用详情",
    description="获取应用详情",
    response_model=ResponseSchema[ApplicationOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="应用ID")],
    auth: Annotated[
        AuthSchema,
        Depends(AuthPermission(["module_application:portal:detail"])),
    ],
) -> JSONResponse:
    """
    获取应用详情

    参数:
    - id (int): 应用ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含应用详情的JSON响应
    """
    result_dict = await ApplicationService.detail_service(id=id, auth=auth)
    log.info(f"获取应用详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取应用详情成功")


@PortalRouter.get(
    "/list",
    summary="查询应用列表",
    description="查询应用列表",
    response_model=ResponseSchema[list[ApplicationOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ApplicationQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:portal:query"]))],
) -> JSONResponse:
    """
    查询应用列表

    参数:
    - page (PaginationQueryParam): 分页参数模型
    - search (ApplicationQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含应用列表的JSON响应
    """
    result_dict = await ApplicationService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询应用列表成功")
    return SuccessResponse(data=result_dict, msg="查询应用列表成功")


@PortalRouter.get(
    "/plugins",
    summary="列出插件元数据",
    description="扫描 app/plugin 下 module_* 目录及可选 plugin.toml，供管理端展示。",
    response_model=ResponseSchema[list[PluginInfoOut]],
)
async def list_plugins_controller(
    auth: Annotated[
        AuthSchema,
        Depends(AuthPermission(["module_application:portal:query"])),
    ],
) -> JSONResponse:
    """
    列出插件与子系统元数据（不涉及动态安装依赖）。

    参数:
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 插件信息列表
    """
    data = await ApplicationService.list_plugins_service()
    log.info("查询插件元数据列表成功")
    return SuccessResponse(data=data, msg="查询插件元数据成功")


@PortalRouter.post(
    "/create",
    summary="创建应用",
    description="创建应用",
    response_model=ResponseSchema[ApplicationOutSchema],
)
async def create_obj_controller(
    data: ApplicationCreateSchema,
    auth: Annotated[
        AuthSchema,
        Depends(AuthPermission(["module_application:portal:create"])),
    ],
) -> JSONResponse:
    """
    创建应用

    参数:
    - data (ApplicationCreateSchema): 应用创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建应用详情的JSON响应
    """
    result_dict = await ApplicationService.create_service(auth=auth, data=data)
    log.info(f"创建应用成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建应用成功")


@PortalRouter.put(
    "/update/{id}",
    summary="修改应用",
    description="修改应用",
    response_model=ResponseSchema[ApplicationOutSchema],
)
async def update_obj_controller(
    data: ApplicationUpdateSchema,
    id: Annotated[int, Path(description="应用ID")],
    auth: Annotated[
        AuthSchema,
        Depends(AuthPermission(["module_application:portal:update"])),
    ],
) -> JSONResponse:
    """
    修改应用

    参数:
    - data (ApplicationUpdateSchema): 应用更新模型
    - id (int): 应用ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含修改应用详情的JSON响应
    """
    result_dict = await ApplicationService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改应用成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改应用成功")


@PortalRouter.delete(
    "/delete",
    summary="删除应用",
    description="删除应用",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[
        AuthSchema,
        Depends(AuthPermission(["module_application:portal:delete"])),
    ],
) -> JSONResponse:
    """
    删除应用

    参数:
    - ids (list[int]): 应用ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除应用详情的JSON响应
    """
    await ApplicationService.delete_service(auth=auth, ids=ids)
    log.info(f"删除应用成功: {ids}")
    return SuccessResponse(msg="删除应用成功")


@PortalRouter.patch(
    "/available/setting",
    summary="批量修改应用状态",
    description="批量修改应用状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_application:portal:patch"]))],
) -> JSONResponse:
    """
    批量修改应用状态

    参数:
    - data (BatchSetAvailable): 批量修改应用状态模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量修改应用状态成功
    """
    await ApplicationService.set_available_service(auth=auth, data=data)
    log.info(f"批量修改应用状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改应用状态成功")
