"""
咨询会筛选匹配 - 控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    ScreeningFilterCreateSchema,
    ScreeningFilterOutSchema,
    ScreeningFilterQueryParam,
    ScreeningFilterUpdateSchema,
)
from .service import ScreeningService

ScreeningRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/screening",
    tags=["招生咨询会 - 筛选匹配"],
)


@ScreeningRouter.get(
    "/detail/{id}",
    summary="获取筛选条件详情",
    description="获取筛选条件详情",
    response_model=ResponseSchema[ScreeningFilterOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="筛选条件ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:screening:detail"]))],
) -> JSONResponse:
    """获取筛选条件详情"""
    result_dict = await ScreeningService.detail_service(auth=auth, id=id)
    log.info(f"获取筛选条件详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取详情成功")


@ScreeningRouter.get(
    "/list",
    summary="查询筛选条件列表",
    description="查询筛选条件列表",
    response_model=ResponseSchema[list[ScreeningFilterOutSchema]],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ScreeningFilterQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:screening:query"]))],
) -> JSONResponse:
    """查询筛选条件列表"""
    result_dict = await ScreeningService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询筛选条件列表成功")
    return SuccessResponse(data=result_dict, msg="查询列表成功")


@ScreeningRouter.post(
    "/create",
    summary="创建筛选条件",
    description="创建筛选条件",
    response_model=ResponseSchema[ScreeningFilterOutSchema],
)
async def create_obj_controller(
    data: ScreeningFilterCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:screening:create"]))],
) -> JSONResponse:
    """创建筛选条件"""
    result_dict = await ScreeningService.create_service(auth=auth, data=data)
    log.info("创建筛选条件成功")
    return SuccessResponse(data=result_dict, msg="创建成功")


@ScreeningRouter.put(
    "/update/{id}",
    summary="更新筛选条件",
    description="更新筛选条件",
    response_model=ResponseSchema[ScreeningFilterOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="筛选条件ID")],
    data: ScreeningFilterUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:screening:update"]))],
) -> JSONResponse:
    """更新筛选条件"""
    result_dict = await ScreeningService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新筛选条件成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@ScreeningRouter.delete(
    "/delete/{id}",
    summary="删除筛选条件",
    description="删除筛选条件",
)
async def delete_obj_controller(
    id: Annotated[int, Path(description="筛选条件ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:screening:delete"]))],
) -> JSONResponse:
    """删除筛选条件"""
    await ScreeningService.delete_service(auth=auth, id=id)
    log.info(f"删除筛选条件成功 {id}")
    return SuccessResponse(msg="删除成功")


@ScreeningRouter.delete(
    "/batch-delete",
    summary="批量删除筛选条件",
    description="批量删除筛选条件",
)
async def batch_delete_obj_controller(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:screening:delete"]))],
) -> JSONResponse:
    """批量删除筛选条件"""
    await ScreeningService.batch_delete_service(auth=auth, ids=ids)
    log.info(f"批量删除筛选条件成功 {ids}")
    return SuccessResponse(msg="批量删除成功")


@ScreeningRouter.put(
    "/set-default/{id}",
    summary="设为默认筛选",
    description="设为默认筛选条件",
    response_model=ResponseSchema[ScreeningFilterOutSchema],
)
async def set_default_controller(
    id: Annotated[int, Path(description="筛选条件ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:screening:update"]))],
) -> JSONResponse:
    """设为默认筛选"""
    result_dict = await ScreeningService.set_default_service(auth=auth, id=id)
    log.info(f"设为默认筛选成功 {id}")
    return SuccessResponse(data=result_dict, msg="设置默认成功")


@ScreeningRouter.get(
    "/default",
    summary="获取默认筛选条件",
    description="获取默认筛选条件",
    response_model=ResponseSchema[ScreeningFilterOutSchema],
)
async def get_default_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:screening:query"]))],
) -> JSONResponse:
    """获取默认筛选条件"""
    result_dict = await ScreeningService.get_default_filter_service(auth=auth)
    log.info("获取默认筛选条件成功")
    return SuccessResponse(data=result_dict, msg="获取成功")


@ScreeningRouter.post(
    "/apply/{filter_id}",
    summary="应用筛选条件",
    description="应用筛选条件查询咨询会列表",
)
async def apply_filter_controller(
    filter_id: Annotated[int, Path(description="筛选条件ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_consultation:screening:query"]))],
) -> JSONResponse:
    """应用筛选条件"""
    result_list = await ScreeningService.apply_filter_service(auth=auth, filter_id=filter_id)
    log.info(f"应用筛选条件 {filter_id} 成功，找到 {len(result_list)} 条结果")
    return SuccessResponse(data=result_list, msg="应用筛选成功")
