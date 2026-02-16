from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    NodeCreateSchema,
    NodeOutSchema,
    NodeQueryParam,
    NodeUpdateSchema,
)
from .service import NodeService

NodeRouter = APIRouter(route_class=OperationLogRoute, prefix="/node", tags=["节点管理"])


@NodeRouter.get(
    "/detail/{id}",
    summary="获取节点详情",
    description="获取节点详情",
    response_model=ResponseSchema[NodeOutSchema],
)
async def get_node_type_detail_controller(
    id: Annotated[int, Path(description="节点类型ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:detail"]))],
) -> JSONResponse:
    """
    获取节点类型详情

    参数:
    - id (int): 节点类型ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含节点类型详情的JSON响应
    """
    result_dict = await NodeService.detail_service(auth=auth, id=id)
    log.info(f"获取节点详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取节点详情成功")


@NodeRouter.get(
    "/list",
    summary="查询节点列表",
    description="查询节点列表",
    response_model=ResponseSchema[list[NodeOutSchema]],
)
async def get_node_type_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[NodeQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:query"]))],
) -> JSONResponse:
    """
    查询节点列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (NodeQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含节点列表分页信息的JSON响应
    """
    result_dict = await NodeService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search.__dict__ if search else None,
        order_by=page.order_by,
    )
    log.info("查询节点列表成功")
    return SuccessResponse(data=result_dict, msg="查询节点列表成功")


@NodeRouter.get(
    "/options",
    summary="获取节点选项",
    description="获取节点选项",
    response_model=ResponseSchema[list[NodeOutSchema]],
)
async def get_node_options_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:query"]))],
) -> JSONResponse:
    """
    获取节点选项

    参数:
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含节点选项的JSON响应
    """
    result_list = await NodeService.list_service(auth=auth)
    log.info("获取节点选项成功")
    return SuccessResponse(data=result_list, msg="获取节点选项成功")


@NodeRouter.post(
    "/create",
    summary="创建节点",
    description="创建节点",
    response_model=ResponseSchema[NodeOutSchema],
)
async def create_node_controller(
    data: NodeCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:create"]))],
) -> JSONResponse:
    """
    创建节点

    参数:
    - data (NodeCreateSchema): 节点创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建节点详情的JSON响应
    """
    result_dict = await NodeService.create_service(auth=auth, data=data)
    log.info(f"创建节点成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="创建节点成功")


@NodeRouter.put(
    "/update/{id}",
    summary="修改节点",
    description="修改节点",
    response_model=ResponseSchema[NodeOutSchema],
)
async def update_node_controller(
    data: NodeUpdateSchema,
    id: Annotated[int, Path(description="节点ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:update"]))],
) -> JSONResponse:
    """
    修改节点

    参数:
    - data (NodeUpdateSchema): 节点更新模型
    - id (int): 节点ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含修改节点详情的JSON响应
    """
    result_dict = await NodeService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改节点成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="修改节点成功")


@NodeRouter.delete(
    "/delete",
    summary="删除节点",
    description="删除节点",
    response_model=ResponseSchema[None],
)
async def delete_node_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:delete"]))],
) -> JSONResponse:
    """
    删除节点

    参数:
    - ids (list[int]): 节点ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除节点详情的JSON响应
    """
    await NodeService.delete_service(auth=auth, ids=ids)
    log.info(f"删除节点成功: {ids}")
    return SuccessResponse(msg="删除节点成功")
