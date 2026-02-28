from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.request import PaginationService
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    NodeCreateSchema,
    NodeExecuteSchema,
    NodeOutSchema,
    NodeQueryParam,
    NodeUpdateSchema,
)
from .service import NodeService

NodeRouter = APIRouter(route_class=OperationLogRoute, prefix="/node", tags=["节点"])


@NodeRouter.get(
    "/options",
    summary="获取节点类型选项",
    description="获取节点类型选项列表，用于流程编排",
    response_model=ResponseSchema[list[dict]],
)
async def get_node_options_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:query"]))],
) -> JSONResponse:
    """
    获取节点类型选项

    参数:
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含节点类型选项列表的JSON响应
    """
    result = await NodeService.get_node_options_service(auth=auth)
    log.info("获取节点类型选项成功")
    return SuccessResponse(data=result, msg="获取节点类型选项成功")


@NodeRouter.get(
    "/detail/{id}",
    summary="获取节点详情",
    description="获取节点详情",
    response_model=ResponseSchema[NodeOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="节点ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:detail"]))],
) -> JSONResponse:
    """
    获取节点详情

    参数:
    - id (int): 节点ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含节点详情的JSON响应
    """
    result_dict = await NodeService.get_node_detail_service(id=id, auth=auth)
    log.info(f"获取节点详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取节点详情成功")


@NodeRouter.get(
    "/list",
    summary="查询节点",
    description="查询节点",
    response_model=ResponseSchema[list[NodeOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[NodeQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:query"]))],
) -> JSONResponse:
    """
    查询节点

    参数:
    - page (PaginationQueryParam): 分页查询参数模型
    - search (NodeQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含分页后的节点列表的JSON响应
    """
    result_dict_list = await NodeService.get_node_list_service(
        auth=auth, search=search, order_by=page.order_by
    )
    result_dict = await PaginationService.paginate(
        data_list=result_dict_list,
        page_no=page.page_no,
        page_size=page.page_size,
    )
    log.info("查询节点列表成功")
    return SuccessResponse(data=result_dict, msg="查询节点列表成功")


@NodeRouter.post(
    "/create",
    summary="创建节点",
    description="创建节点（仅保存到数据库，不创建调度器任务）",
    response_model=ResponseSchema[NodeOutSchema],
)
async def create_obj_controller(
    data: NodeCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:create"]))],
) -> JSONResponse:
    """
    创建节点

    参数:
    - data (NodeCreateSchema): 创建参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建节点结果的JSON响应
    """
    result_dict = await NodeService.create_node_service(auth=auth, data=data)
    log.info(f"创建节点成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建节点成功")


@NodeRouter.put(
    "/update/{id}",
    summary="修改节点",
    description="修改节点（仅更新数据库，不修改调度器任务）",
    response_model=ResponseSchema[NodeOutSchema],
)
async def update_obj_controller(
    data: NodeUpdateSchema,
    id: Annotated[int, Path(description="节点ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:update"]))],
) -> JSONResponse:
    """
    修改节点

    参数:
    - data (NodeUpdateSchema): 更新参数模型
    - id (int): 节点ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含修改节点结果的JSON响应
    """
    result_dict = await NodeService.update_node_service(auth=auth, id=id, data=data)
    log.info(f"修改节点成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改节点成功")


@NodeRouter.delete(
    "/delete",
    summary="删除节点",
    description="删除节点",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:delete"]))],
) -> JSONResponse:
    """
    删除节点

    参数:
    - ids (list[int]): ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含删除节点结果的JSON响应
    """
    await NodeService.delete_node_service(auth=auth, ids=ids)
    log.info(f"删除节点成功: {ids}")
    return SuccessResponse(msg="删除节点成功")


@NodeRouter.delete(
    "/clear",
    summary="清空节点",
    description="清空所有节点",
    response_model=ResponseSchema[None],
)
async def clear_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:delete"]))],
) -> JSONResponse:
    """
    清空所有节点

    参数:
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含清空节点结果的JSON响应
    """
    await NodeService.clear_node_service(auth=auth)
    log.info("清空节点成功")
    return SuccessResponse(msg="清空节点成功")


@NodeRouter.post(
    "/execute/{id}",
    summary="调试节点",
    description="调试节点（创建调度器任务并执行）",
    response_model=ResponseSchema[dict],
)
async def execute_job_controller(
    id: Annotated[int, Path(description="节点ID")],
    data: NodeExecuteSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_task:node:execute"]))],
) -> JSONResponse:
    """
    调试节点

    参数:
    - id (int): 节点ID
    - data (NodeExecuteSchema): 执行参数模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含调试结果的JSON响应
    """
    result = await NodeService.execute_node_service(auth=auth, id=id, execute_data=data)
    log.info(f"调试节点成功: {id}")
    return SuccessResponse(data=result, msg="调试节点成功")
