"""
行程报备 - 控制器
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

from .schema import TripCreateSchema, TripOutSchema, TripQuerySchema, TripUpdateSchema
from .service import TripService

TripRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/trip",
    tags=["招生宣传活动 - 行程报备"],
)


@TripRouter.get(
    "/detail/{id}",
    summary="获取行程报备详情",
    description="获取行程报备详情",
    response_model=ResponseSchema[TripOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="行程报备ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:detail"]))],
) -> JSONResponse:
    """
    获取行程报备详情

    参数:
    - id (int): 行程报备ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含行程报备详情的JSON响应
    """
    result_dict = await TripService.detail_service(auth=auth, id=id)
    log.info(f"获取行程报备详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@TripRouter.get(
    "/list",
    summary="查询行程报备列表",
    description="查询行程报备列表",
    response_model=ResponseSchema[list[TripOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[TripQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:query"]))],
) -> JSONResponse:
    """
    查询行程报备列表

    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (TripQuerySchema): 查询参数
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含行程报备列表分页信息的JSON响应
    """
    result_dict = await TripService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询行程报备列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@TripRouter.post(
    "/create",
    summary="创建行程报备",
    description="创建行程报备",
    response_model=ResponseSchema[TripOutSchema],
)
async def create_obj_controller(
    data: TripCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:create"]))],
) -> JSONResponse:
    """
    创建行程报备

    参数:
    - data (TripCreateSchema): 行程报备创建模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含创建行程报备详情的JSON响应
    """
    result_dict = await TripService.create_service(auth=auth, data=data)
    log.info("创建行程报备成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@TripRouter.put(
    "/update/{id}",
    summary="更新行程报备",
    description="更新行程报备",
    response_model=ResponseSchema[TripOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="行程报备ID")],
    data: TripUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:update"]))],
) -> JSONResponse:
    """
    更新行程报备

    参数:
    - id (int): 行程报备ID
    - data (TripUpdateSchema): 行程报备更新模型
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 包含更新后行程报备详情的JSON响应
    """
    result_dict = await TripService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新行程报备成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@TripRouter.delete(
    "/delete/{id}",
    summary="删除行程报备",
    description="删除行程报备",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="行程报备ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:delete"]))],
) -> JSONResponse:
    """
    删除行程报备

    参数:
    - id (int): 行程报备ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 删除成功的JSON响应
    """
    await TripService.delete_service(auth=auth, id=id)
    log.info(f"删除行程报备成功 {id}")
    return SuccessResponse(msg="删除成功")


@TripRouter.delete(
    "/batch-delete",
    summary="批量删除行程报备",
    description="批量删除行程报备",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:delete"]))],
) -> JSONResponse:
    """
    批量删除行程报备

    参数:
    - ids (list[int]): 行程报备ID列表
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 批量删除成功的JSON响应
    """
    await TripService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除行程报备成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@TripRouter.post(
    "/start/{id}",
    summary="开始行程",
    description="开始行程",
    response_model=ResponseSchema[TripOutSchema],
)
async def start_trip_controller(
    id: Annotated[int, Path(description="行程报备ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:update"]))],
) -> JSONResponse:
    """
    开始行程

    参数:
    - id (int): 行程报备ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 开始行程的JSON响应
    """
    result_dict = await TripService.start_trip_service(auth=auth, id=id)
    log.info(f"开始行程成功 {id}")
    return SuccessResponse(data=result_dict, msg="开始行程成功")


@TripRouter.post(
    "/complete/{id}",
    summary="完成行程",
    description="完成行程",
    response_model=ResponseSchema[TripOutSchema],
)
async def complete_trip_controller(
    id: Annotated[int, Path(description="行程报备ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:update"]))],
) -> JSONResponse:
    """
    完成行程

    参数:
    - id (int): 行程报备ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 完成行程的JSON响应
    """
    result_dict = await TripService.complete_trip_service(auth=auth, id=id)
    log.info(f"完成行程成功 {id}")
    return SuccessResponse(data=result_dict, msg="完成行程成功")


@TripRouter.post(
    "/cancel/{id}",
    summary="取消行程",
    description="取消行程",
    response_model=ResponseSchema[TripOutSchema],
)
async def cancel_trip_controller(
    id: Annotated[int, Path(description="行程报备ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:update"]))],
) -> JSONResponse:
    """
    取消行程

    参数:
    - id (int): 行程报备ID
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 取消行程的JSON响应
    """
    result_dict = await TripService.cancel_trip_service(auth=auth, id=id)
    log.info(f"取消行程成功 {id}")
    return SuccessResponse(data=result_dict, msg="取消行程成功")


@TripRouter.post(
    "/location/{id}",
    summary="更新位置",
    description="更新位置",
    response_model=ResponseSchema[TripOutSchema],
)
async def update_location_controller(
    id: Annotated[int, Path(description="行程报备ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_promotion:trip:location"]))],
    latitude: Annotated[float, Query(description="纬度")],
    longitude: Annotated[float, Query(description="经度")],
    address: Annotated[str | None, Query(description="地址")] = None,
) -> JSONResponse:
    """
    更新位置

    参数:
    - id (int): 行程报备ID
    - latitude (float): 纬度
    - longitude (float): 经度
    - address (str | None): 地址
    - auth (AuthSchema): 认证信息模型

    返回:
    - JSONResponse: 更新位置的JSON响应
    """
    result_dict = await TripService.update_location_service(
        auth=auth, id=id, latitude=latitude, longitude=longitude, address=address
    )
    log.info(f"更新位置成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新位置成功")
