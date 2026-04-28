"""
组织架构管理 - 控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import TeamCreateSchema, TeamOutSchema, TeamQuerySchema, TeamUpdateSchema
from .service import TeamService

TeamRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/team",
    tags=["招生宣传活动 - 组织架构管理"],
)


@TeamRouter.get(
    "/detail/{id}",
    summary="获取招生组详情",
    description="获取招生组详情",
    response_model=ResponseSchema[TeamOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="招生组ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:team:detail"]))],
) -> JSONResponse:
    """
    获取招生组详情

    参数:
    - id (int): 招生组ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含招生组详情的JSON响应
    """
    result_dict = await TeamService.detail_service(auth=auth, id=id)
    log.info(f"获取招生组详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@TeamRouter.get(
    "/list",
    summary="查询招生组列表",
    description="查询招生组列表",
    response_model=ResponseSchema[list[TeamOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[TeamQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:team:query"]))],
) -> JSONResponse:
    """
    查询招生组列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (TeamQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含招生组列表分页信息的JSON响应
    """
    result_dict = await TeamService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询招生组列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@TeamRouter.get(
    "/tree",
    summary="获取招生组树形结构",
    description="获取招生组树形结构",
    response_model=ResponseSchema,
)
async def get_tree_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:team:query"]))],
) -> JSONResponse:
    """
    获取招生组树形结构

    参数:
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含招生组树形结构的JSON响应
    """
    result_list = await TeamService.tree_service(auth=auth)
    log.info("获取招生组树形结构成功")
    return SuccessResponse(data=result_list, msg="获取树形结构成功")


@TeamRouter.post(
    "/create",
    summary="创建招生组",
    description="创建招生组",
    response_model=ResponseSchema[TeamOutSchema],
)
async def create_obj_controller(
    data: TeamCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:team:create"]))],
) -> JSONResponse:
    """
    创建招生组

    参数:
    - data (TeamCreateSchema): 招生组创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建招生组详情的JSON响应
    """
    result_dict = await TeamService.create_service(auth=auth, data=data)
    log.info("创建招生组成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@TeamRouter.put(
    "/update/{id}",
    summary="更新招生组",
    description="更新招生组",
    response_model=ResponseSchema[TeamOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="招生组ID")],
    data: TeamUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:team:update"]))],
) -> JSONResponse:
    """
    更新招生组

    参数:
    - id (int): 招生组ID
    - data (TeamUpdateSchema): 招生组更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后招生组详情的JSON响应
    """
    result_dict = await TeamService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新招生组成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@TeamRouter.delete(
    "/delete/{id}",
    summary="删除招生组",
    description="删除招生组",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="招生组ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:team:delete"]))],
) -> JSONResponse:
    """
    删除招生组

    参数:
    - id (int): 招生组ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await TeamService.delete_service(auth=auth, id=id)
    log.info(f"删除招生组成功 {id}")
    return SuccessResponse(msg="删除成功")


@TeamRouter.delete(
    "/batch-delete",
    summary="批量删除招生组",
    description="批量删除招生组",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:team:delete"]))],
) -> JSONResponse:
    """
    批量删除招生组

    参数:
    - ids (list[int]): 招生组ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await TeamService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除招生组成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@TeamRouter.post(
    "/set-status/{id}",
    summary="设置招生组状态",
    description="设置招生组状态",
    response_model=ResponseSchema[TeamOutSchema],
)
async def set_status_controller(
    id: Annotated[int, Path(description="招生组ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:team:update"]))],
    status: Annotated[str, Query(description="状态(active/inactive/dissolved)")],
) -> JSONResponse:
    """
    设置招生组状态

    参数:
    - id (int): 招生组ID
    - status (str): 状态
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 设置状态成功的JSON响应
    """
    result_dict = await TeamService.set_status_service(auth=auth, id=id, status=status)
    log.info(f"设置招生组状态成功 {id}, status={status}")
    return SuccessResponse(data=result_dict, msg="设置状态成功")
