# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.request import PaginationService
from app.common.response import SuccessResponse, StreamResponse
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response
from app.core.dependencies import AuthPermission
from app.core.base_params import PaginationQueryParam
from app.core.logger import log

from ..auth.schema import AuthSchema
from .schema import OperationLogQueryParam
from .service import OperationLogService


LogRouter = APIRouter(route_class=OperationLogRoute, prefix="/log", tags=["日志管理"])


@LogRouter.get("/list", summary="查询日志", description="查询日志")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: OperationLogQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:log:query"]))
) -> JSONResponse:
    """ 
    查询日志 
    
    参数:
    - page (PaginationQueryParam): 分页查询参数模型
    - search (OperationLogQueryParam): 日志查询参数模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含分页日志详情的 JSON 响应模型
    """
    order_by = [{"created_time": "desc"}]
    if page.order_by:
        order_by = page.order_by
    result_dict_list = await OperationLogService.get_log_list_service(search=search, auth=auth, order_by=order_by)
    result_dict = await PaginationService.paginate(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    log.info(f"查询日志成功")
    return SuccessResponse(data=result_dict, msg="查询日志成功")


@LogRouter.get("/detail/{id}", summary="日志详情", description="日志详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="操作日志ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:log:query"]))
) -> JSONResponse:
    """ 
    获取日志详情 
    
    参数:
    - id (int): 操作日志ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含日志详情的 JSON 响应模型
    """
    result_dict = await OperationLogService.get_log_detail_service(id=id, auth=auth)
    log.info(f"查询日志成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取日志详情成功")


@LogRouter.delete("/delete", summary="删除日志", description="删除日志")
async def delete_obj_log_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:log:delete"]))
) -> JSONResponse:
    """ 
    删除日志 
    
    参数:
    - ids (list[int]): 日志 ID 列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含删除结果的 JSON 响应模型
    """
    await OperationLogService.delete_log_service(ids=ids, auth=auth)
    log.info(f"删除日志成功 {ids}")
    return SuccessResponse(msg="删除日志成功")


@LogRouter.post("/export", summary="导出日志", description="导出日志")
async def export_obj_list_controller(
    search: OperationLogQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:log:export"]))
) -> StreamingResponse:
    """ 
    导出日志 
    
    参数:
    - search (OperationLogQueryParam): 日志查询参数模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - StreamingResponse: 包含导出日志的流式响应模型
    """
    operation_log_list = await OperationLogService.get_log_list_service(search=search, auth=auth)
    operation_log_export_result = await OperationLogService.export_log_list_service(operation_log_list=operation_log_list)
    log.info('导出日志成功')

    return StreamResponse(
        data=bytes2file_response(operation_log_export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {
            'Content-Disposition': 'attachment; filename=log.xlsx'
        }
    )
