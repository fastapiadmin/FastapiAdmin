"""
行程方案管理 - 控制器
"""
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    ItineraryCreateSchema,
    ItineraryOutSchema,
    ItineraryQuerySchema,
    ItineraryUpdateSchema,
)
from .service import ItineraryService

ItineraryRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/itinerary",
    tags=["招生咨询会 - 行程方案"],
)


@ItineraryRouter.get(
    "/detail/{id}",
    summary="获取行程方案详情",
    description="获取行程方案详情",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:detail"]))],
) -> JSONResponse:
    """获取行程方案详情"""
    result_dict = await ItineraryService.detail_service(auth=auth, id=id)
    log.info(f"获取行程方案详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@ItineraryRouter.get(
    "/list",
    summary="查询行程方案列表",
    description="查询行程方案列表",
    response_model=ResponseSchema[list[ItineraryOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ItineraryQuerySchema, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:query"]))],
) -> JSONResponse:
    """查询行程方案列表"""
    result_dict = await ItineraryService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询行程方案列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@ItineraryRouter.post(
    "/create",
    summary="创建行程方案",
    description="创建行程方案",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def create_obj_controller(
    data: ItineraryCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:create"]))],
) -> JSONResponse:
    """创建行程方案"""
    result_dict = await ItineraryService.create_service(auth=auth, data=data)
    log.info(f"创建行程方案成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@ItineraryRouter.put(
    "/update/{id}",
    summary="更新行程方案",
    description="更新行程方案",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    data: ItineraryUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:update"]))],
) -> JSONResponse:
    """更新行程方案"""
    result_dict = await ItineraryService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新行程方案成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@ItineraryRouter.delete(
    "/delete/{id}",
    summary="删除行程方案",
    description="删除行程方案",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:delete"]))],
) -> JSONResponse:
    """删除行程方案"""
    await ItineraryService.delete_service(auth=auth, id=id)
    log.info(f"删除行程方案成功 {id}")
    return SuccessResponse(msg="删除成功")


@ItineraryRouter.delete(
    "/batch-delete",
    summary="批量删除行程方案",
    description="批量删除行程方案",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:delete"]))],
) -> JSONResponse:
    """批量删除行程方案"""
    await ItineraryService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除行程方案成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@ItineraryRouter.post(
    "/confirm/{id}",
    summary="确认行程方案",
    description="确认行程方案",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def confirm_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:update"]))],
) -> JSONResponse:
    """确认行程方案"""
    result_dict = await ItineraryService.confirm_service(auth=auth, id=id)
    log.info(f"确认行程方案 {id}")
    return SuccessResponse(data=result_dict, msg="确认成功")


@ItineraryRouter.post(
    "/execute/{id}",
    summary="执行行程方案",
    description="执行行程方案",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def execute_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:update"]))],
) -> JSONResponse:
    """执行行程方案"""
    result_dict = await ItineraryService.execute_service(auth=auth, id=id)
    log.info(f"执行行程方案 {id}")
    return SuccessResponse(data=result_dict, msg="执行成功")


@ItineraryRouter.post(
    "/archive/{id}",
    summary="归档行程方案",
    description="归档行程方案",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def archive_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:update"]))],
) -> JSONResponse:
    """归档行程方案"""
    result_dict = await ItineraryService.archive_service(auth=auth, id=id)
    log.info(f"归档行程方案 {id}")
    return SuccessResponse(data=result_dict, msg="归档成功")


@ItineraryRouter.post(
    "/sync-calendar/{id}",
    summary="同步到日历",
    description="同步行程方案到日历",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def sync_calendar_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:update"]))],
) -> JSONResponse:
    """同步到日历"""
    result_dict = await ItineraryService.sync_calendar_service(auth=auth, id=id)
    log.info(f"同步行程方案到日历 {id}")
    return SuccessResponse(data=result_dict, msg="同步成功")


@ItineraryRouter.post(
    "/add-consultation/{id}",
    summary="添加咨询会到行程",
    description="添加咨询会到行程",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def add_consultation_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    consultation_id: Annotated[int, Query(description="咨询会ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:update"]))],
) -> JSONResponse:
    """添加咨询会到行程"""
    result_dict = await ItineraryService.add_consultation_service(
        auth=auth, id=id, consultation_id=consultation_id
    )
    log.info(f"添加咨询会到行程 {id}")
    return SuccessResponse(data=result_dict, msg="添加成功")


@ItineraryRouter.post(
    "/remove-consultation/{id}",
    summary="从行程移除咨询会",
    description="从行程移除咨询会",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def remove_consultation_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    consultation_id: Annotated[int, Query(description="咨询会ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:update"]))],
) -> JSONResponse:
    """从行程移除咨询会"""
    result_dict = await ItineraryService.remove_consultation_service(
        auth=auth, id=id, consultation_id=consultation_id
    )
    log.info(f"从行程移除咨询会 {id}")
    return SuccessResponse(data=result_dict, msg="移除成功")


@ItineraryRouter.post(
    "/optimize-route/{id}",
    summary="优化路线",
    description="优化行程路线",
    response_model=ResponseSchema[ItineraryOutSchema],
)
async def optimize_route_controller(
    id: Annotated[int, Path(description="行程方案ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:itinerary:update"]))],
) -> JSONResponse:
    """优化路线"""
    result_dict = await ItineraryService.optimize_route_service(auth=auth, id=id)
    log.info(f"优化行程路线 {id}")
    return SuccessResponse(data=result_dict, msg="优化成功")
