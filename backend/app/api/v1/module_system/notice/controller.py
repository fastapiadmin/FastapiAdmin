# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission, get_current_user
from app.core.base_schema import BatchSetAvailable
from app.core.logger import log
from app.common.request import PaginationService
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

from ..auth.schema import AuthSchema
from .service import NoticeService
from .schema import (
    NoticeCreateSchema,
    NoticeUpdateSchema,
    NoticeQueryParam
)


NoticeRouter = APIRouter(route_class=OperationLogRoute, prefix="/notice", tags=["公告通知"])

@NoticeRouter.get("/detail/{id}", summary="获取公告详情", description="获取公告详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="公告ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:notice:query"]))
) -> JSONResponse:
    """
    获取公告详情。
    
    参数:
    - id (int): 公告ID。
    - auth (AuthSchema): 认证信息模型。
    
    返回:
    - JSONResponse: 包含公告详情的响应模型。
    """
    result_dict = await NoticeService.get_notice_detail_service(id=id, auth=auth)
    log.info(f"获取公告详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取公告详情成功")

@NoticeRouter.get("/list", summary="查询公告", description="查询公告")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: NoticeQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:notice:query"]))
) -> JSONResponse:
    """
    查询公告。
    
    参数:
    - page (PaginationQueryParam): 分页查询参数模型。
    - search (NoticeQueryParam): 查询公告参数模型。
    - auth (AuthSchema): 认证信息模型。
    
    返回:
    - JSONResponse: 包含分页公告详情的响应模型。
    """
    result_dict_list = await NoticeService.get_notice_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.paginate(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    log.info(f"查询公告列表成功")
    return SuccessResponse(data=result_dict, msg="查询公告列表成功")

@NoticeRouter.post("/create", summary="创建公告", description="创建公告")
async def create_obj_controller(
    data: NoticeCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_system:notice:create"]))
) -> JSONResponse:
    """
    创建公告。
    
    参数:
    - data (NoticeCreateSchema): 创建公告负载模型。
    - auth (AuthSchema): 认证信息模型。
    
    返回:
    - JSONResponse: 包含创建公告结果的响应模型。
    """
    result_dict = await NoticeService.create_notice_service(auth=auth, data=data)
    log.info(f"创建公告成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建公告成功")

@NoticeRouter.put("/update/{id}", summary="修改公告", description="修改公告")
async def update_obj_controller(
    data: NoticeUpdateSchema,
    id: int = Path(..., description="公告ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:notice:update"]))
) -> JSONResponse:
    """
    修改公告。
    
    参数:
    - data (NoticeUpdateSchema): 修改公告负载模型。
    - id (int): 公告ID。
    - auth (AuthSchema): 认证信息模型。
    
    返回:
    - JSONResponse: 包含修改公告结果的响应模型。
    """
    result_dict = await NoticeService.update_notice_service(auth=auth, id=id, data=data)
    log.info(f"修改公告成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改公告成功")

@NoticeRouter.delete("/delete", summary="删除公告", description="删除公告")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:notice:delete"]))
) -> JSONResponse:
    """
    删除公告。
    
    参数:
    - ids (list[int]): 公告ID列表。
    - auth (AuthSchema): 认证信息模型。
    
    返回:
    - JSONResponse: 包含删除公告结果的响应模型。
    """
    await NoticeService.delete_notice_service(auth=auth, ids=ids)
    log.info(f"删除公告成功: {ids}")
    return SuccessResponse(msg="删除公告成功")

@NoticeRouter.patch("/available/setting", summary="批量修改公告状态", description="批量修改公告状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_system:notice:patch"]))
) -> JSONResponse:
    """
    批量修改公告状态。
    
    参数:
    - data (BatchSetAvailable): 批量修改公告状态负载模型。
    - auth (AuthSchema): 认证信息模型。
    
    返回:
    - JSONResponse: 包含批量修改公告状态结果的响应模型。
    """
    await NoticeService.set_notice_available_service(auth=auth, data=data)
    log.info(f"批量修改公告状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改公告状态成功")

@NoticeRouter.post('/export', summary="导出公告", description="导出公告")
async def export_obj_list_controller(
    search: NoticeQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:notice:export"]))
) -> StreamingResponse:
    """
    导出公告。
    
    参数:
    - search (NoticeQueryParam): 查询公告参数模型。
    - auth (AuthSchema): 认证信息模型。
    
    返回:
    - StreamingResponse: 包含导出公告的流式响应模型。
    """
    result_dict_list = await NoticeService.get_notice_list_service(search=search, auth=auth)
    export_result = await NoticeService.export_notice_service(notice_list=result_dict_list)
    log.info('导出公告成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {'Content-Disposition': 'attachment; filename=notice.xlsx'}
    )

@NoticeRouter.get("/available", summary="获取全局启用公告", description="获取全局启用公告")
async def get_obj_list_available_controller(
    auth: AuthSchema = Depends(get_current_user)
) -> JSONResponse:
    """
    获取全局启用公告。
    
    参数:
    - auth (AuthSchema): 认证信息模型。
    
    返回:
    - JSONResponse: 包含分页已启用公告详情的响应模型。
    """
    result_dict_list = await NoticeService.get_notice_list_available_service(auth=auth)
    result_dict = await PaginationService.paginate(data_list= result_dict_list)
    log.info(f"查询已启用公告列表成功")
    return SuccessResponse(data=result_dict, msg="查询已启用公告列表成功")
