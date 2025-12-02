# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import StreamResponse, SuccessResponse
from app.common.request import PaginationService
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.base_schema import BatchSetAvailable
from app.core.logger import log

from ..auth.schema import AuthSchema
from .service import PositionService
from .schema import (
    PositionCreateSchema,
    PositionUpdateSchema,
    PositionQueryParam
)


PositionRouter = APIRouter(route_class=OperationLogRoute, prefix="/position", tags=["岗位管理"])


@PositionRouter.get("/list", summary="查询岗位", description="查询岗位")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: PositionQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:position:query"])),
) -> JSONResponse:
    """
    查询岗位列表
    
    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (PositionQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 分页查询结果
    """
    order_by = [{"order": "asc"}]
    if page.order_by:
        order_by = page.order_by
    result_dict_list = await PositionService.get_position_list_service(search=search, auth=auth, order_by=order_by)
    result_dict = await PaginationService.paginate(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    log.info(f"查询岗位列表成功")
    return SuccessResponse(data=result_dict, msg="查询岗位列表成功")


@PositionRouter.get("/detail/{id}", summary="查询岗位详情", description="查询岗位详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="岗位ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:position:query"])),
) -> JSONResponse:
    """
    查询岗位详情
    
    参数:
    - id (int): 岗位ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 岗位详情对象
    """
    result_dict = await PositionService.get_position_detail_service(id=id, auth=auth)
    log.info(f"查询岗位详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取岗位详情成功")


@PositionRouter.post("/create", summary="创建岗位", description="创建岗位")
async def create_obj_controller(
    data: PositionCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_system:position:create"])),
) -> JSONResponse:
    """
    创建岗位
    
    参数:
    - data (PositionCreateSchema): 创建岗位模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 岗位详情对象
    """
    result_dict = await PositionService.create_position_service(data=data, auth=auth)
    log.info(f"创建岗位成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建岗位成功")


@PositionRouter.put("/update/{id}", summary="修改岗位", description="修改岗位")
async def update_obj_controller(
    data: PositionUpdateSchema,
    id: int = Path(..., description="岗位ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:position:update"])),
) -> JSONResponse:
    """
    修改岗位
    
    参数:
    - data (PositionUpdateSchema): 修改岗位模型
    - id (int): 岗位ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 岗位详情对象
    """
    result_dict = await PositionService.update_position_service(id=id, data=data, auth=auth)
    log.info(f"修改岗位成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改岗位成功")


@PositionRouter.delete("/delete", summary="删除岗位", description="删除岗位")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:position:delete"])),
) -> JSONResponse:
    """
    删除岗位
    
    参数:
    - ids (list[int]): ID列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 成功消息
    """
    await PositionService.delete_position_service(ids=ids, auth=auth)
    log.info(f"删除岗位成功: {ids}")
    return SuccessResponse(msg="删除岗位成功")


@PositionRouter.patch("/available/setting", summary="批量修改岗位状态", description="批量修改岗位状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_system:position:patch"])),
) -> JSONResponse:
    """
    批量修改岗位状态
    
    参数:
    - data (BatchSetAvailable): 批量修改岗位状态模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 成功消息
    """
    await PositionService.set_position_available_service(data=data, auth=auth)
    log.info(f"批量修改岗位状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改岗位状态成功")


@PositionRouter.post('/export', summary="导出岗位", description="导出岗位")
async def export_obj_list_controller(
    search: PositionQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:position:export"])),
) -> StreamingResponse:
    """
    导出岗位
    
    参数:
    - search (PositionQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - StreamingResponse: 岗位Excel文件流
    """
    position_query_result = await PositionService.get_position_list_service(search=search, auth=auth)
    position_export_result = await PositionService.export_position_list_service(position_list=position_query_result)
    log.info('导出岗位成功')

    return StreamResponse(
        data=bytes2file_response(position_export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {
            'Content-Disposition': 'attachment; filename=position.xlsx'
        }
    )
