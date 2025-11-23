# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
import urllib.parse

from app.common.response import StreamResponse, SuccessResponse
from app.utils.common_util import bytes2file_response
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.base_schema import BatchSetAvailable
from app.core.logger import log

from app.api.v1.module_system.auth.schema import AuthSchema
from .param import TenantQueryParam
from .service import TenantService
from .schema import (
    TenantCreateSchema,
    TenantUpdateSchema
)


TenantRouter = APIRouter(route_class=OperationLogRoute, prefix="/tenant", tags=["租户模块"])

@TenantRouter.get("/detail/{id}", summary="获取租户详情", description="获取租户详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="租户ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:tenant:query"]))
) -> JSONResponse:
    """
    获取租户详情
    
    参数:
    - id (int): 租户ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含租户详情的JSON响应
    """
    result_dict = await TenantService.detail_service(id=id, auth=auth)
    log.info(f"获取租户详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取租户详情成功")

@TenantRouter.get("/list", summary="查询租户列表", description="查询租户列表")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: TenantQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:tenant:query"]))
) -> JSONResponse:
    """
    查询租户列表
    
    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (TenantQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含租户列表分页信息的JSON响应
    """
    # 使用数据库分页而不是应用层分页
    result_dict = await TenantService.page_service(
        auth=auth, 
        page_no=page.page_no if page.page_no is not None else 1, 
        page_size=page.page_size if page.page_size is not None else 10, 
        search=search, 
        order_by=page.order_by
    )
    log.info("查询租户列表成功")
    return SuccessResponse(data=result_dict, msg="查询租户列表成功")

@TenantRouter.post("/create", summary="创建租户", description="创建租户")
async def create_obj_controller(
    data: TenantCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_system:tenant:create"]))
) -> JSONResponse:
    """
    创建租户
    
    参数:
    - data (TenantCreateSchema): 租户创建模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含创建租户详情的JSON响应
    """
    result_dict = await TenantService.create_service(auth=auth, data=data)
    log.info(f"创建租户成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="创建租户成功")

@TenantRouter.put("/update/{id}", summary="修改租户", description="修改租户")
async def update_obj_controller(
    data: TenantUpdateSchema,
    id: int = Path(..., description="租户ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:tenant:update"]))
) -> JSONResponse:
    """
    修改租户
    
    参数:
    - data (TenantUpdateSchema): 租户更新模型
    - id (int): 租户ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含修改租户详情的JSON响应
    """
    result_dict = await TenantService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改租户成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="修改租户成功")

@TenantRouter.delete("/delete", summary="删除租户", description="删除租户")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:tenant:delete"]))
) -> JSONResponse:
    """
    删除租户
    
    参数:
    - ids (list[int]): 租户ID列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含删除租户详情的JSON响应
    """
    await TenantService.delete_service(auth=auth, ids=ids)
    log.info(f"删除租户成功: {ids}")
    return SuccessResponse(msg="删除租户成功")

@TenantRouter.patch("/available/setting", summary="批量修改租户状态", description="批量修改租户状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_system:tenant:patch"]))
) -> JSONResponse:
    """
    批量修改租户状态
    
    参数:
    - data (BatchSetAvailable): 批量修改租户状态模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含批量修改租户状态详情的JSON响应
    """
    await TenantService.set_available_service(auth=auth, data=data)
    log.info(f"批量修改租户状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改租户状态成功")

@TenantRouter.post('/export', summary="导出租户", description="导出租户")
async def export_obj_list_controller(
    search: TenantQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:tenant:export"]))
) -> StreamingResponse:
    """
    导出租户
    
    参数:
    - search (TenantQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - StreamingResponse: 包含租户列表的Excel文件流响应
    """
    result_dict_list = await TenantService.list_service(search=search, auth=auth)
    export_result = await TenantService.batch_export_service(obj_list=result_dict_list)
    log.info('导出租户成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=example.xlsx'
        }
    )

@TenantRouter.post('/import', summary="导入租户", description="导入租户")
async def import_obj_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_system:tenant:import"]))
) -> JSONResponse:
    """
    导入租户
    
    参数:
    - file (UploadFile): 导入的Excel文件
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含导入租户详情的JSON响应
    """
    batch_import_result = await TenantService.batch_import_service(file=file, auth=auth, update_support=True)
    log.info(f"导入租户成功: {batch_import_result}")
    return SuccessResponse(data=batch_import_result, msg="导入租户成功")

@TenantRouter.post('/download/template', summary="获取租户导入模板", description="获取租户导入模板", dependencies=[Depends(AuthPermission(["module_system:tenant:download"]))])
async def export_obj_template_controller() -> StreamingResponse:
    """
    获取租户导入模板
    
    返回:
    - StreamingResponse: 包含租户导入模板的Excel文件流响应
    """
    example_import_template_result = await TenantService.import_template_download_service()
    log.info('获取租户导入模板成功')

    return StreamResponse(
        data=bytes2file_response(example_import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': f'attachment; filename={urllib.parse.quote("租户导入模板.xlsx")}',
            'Access-Control-Expose-Headers': 'Content-Disposition'
        }
    )