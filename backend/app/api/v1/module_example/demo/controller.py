# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
import urllib.parse

from app.common.response import StreamResponse, SuccessResponse
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.base_schema import BatchSetAvailable
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .service import DemoService
from .schema import (
    DemoCreateSchema,
    DemoUpdateSchema,
    DemoQueryParam
)


DemoRouter = APIRouter(route_class=OperationLogRoute, prefix="/demo", tags=["示例模块"])

@DemoRouter.get("/detail/{id}", summary="获取示例详情", description="获取示例详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="示例ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:demo:query"]))
) -> JSONResponse:
    """
    获取示例详情
    
    参数:
    - id (int): 示例ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含示例详情的JSON响应
    """
    result_dict = await DemoService.detail_service(id=id, auth=auth)
    log.info(f"获取示例详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取示例详情成功")

@DemoRouter.get("/list", summary="查询示例列表", description="查询示例列表")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: DemoQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_example:demo:query"]))
) -> JSONResponse:
    """
    查询示例列表
    
    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (DemoQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含示例列表分页信息的JSON响应
    """
    # 使用数据库分页而不是应用层分页
    result_dict = await DemoService.page_service(
        auth=auth, 
        page_no=page.page_no, 
        page_size=page.page_size, 
        search=search, 
        order_by=page.order_by
    )
    log.info("查询示例列表成功")
    return SuccessResponse(data=result_dict, msg="查询示例列表成功")

@DemoRouter.post("/create", summary="创建示例", description="创建示例")
async def create_obj_controller(
    data: DemoCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_example:demo:create"]))
) -> JSONResponse:
    """
    创建示例
    
    参数:
    - data (DemoCreateSchema): 示例创建模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含创建示例详情的JSON响应
    """
    result_dict = await DemoService.create_service(auth=auth, data=data)
    log.info(f"创建示例成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="创建示例成功")

@DemoRouter.put("/update/{id}", summary="修改示例", description="修改示例")
async def update_obj_controller(
    data: DemoUpdateSchema,
    id: int = Path(..., description="示例ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:demo:update"]))
) -> JSONResponse:
    """
    修改示例
    
    参数:
    - data (DemoUpdateSchema): 示例更新模型
    - id (int): 示例ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含修改示例详情的JSON响应
    """
    result_dict = await DemoService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改示例成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="修改示例成功")

@DemoRouter.delete("/delete", summary="删除示例", description="删除示例")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:demo:delete"]))
) -> JSONResponse:
    """
    删除示例
    
    参数:
    - ids (list[int]): 示例ID列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含删除示例详情的JSON响应
    """
    await DemoService.delete_service(auth=auth, ids=ids)
    log.info(f"删除示例成功: {ids}")
    return SuccessResponse(msg="删除示例成功")

@DemoRouter.patch("/available/setting", summary="批量修改示例状态", description="批量修改示例状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_example:demo:patch"]))
) -> JSONResponse:
    """
    批量修改示例状态
    
    参数:
    - data (BatchSetAvailable): 批量修改示例状态模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含批量修改示例状态详情的JSON响应
    """
    await DemoService.set_available_service(auth=auth, data=data)
    log.info(f"批量修改示例状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改示例状态成功")

@DemoRouter.post('/export', summary="导出示例", description="导出示例")
async def export_obj_list_controller(
    search: DemoQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_example:demo:export"]))
) -> StreamingResponse:
    """
    导出示例
    
    参数:
    - search (DemoQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - StreamingResponse: 包含示例列表的Excel文件流响应
    """
    result_dict_list = await DemoService.list_service(search=search, auth=auth)
    export_result = await DemoService.batch_export_service(obj_list=result_dict_list)
    log.info('导出示例成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=example.xlsx'
        }
    )

@DemoRouter.post('/import', summary="导入示例", description="导入示例")
async def import_obj_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_example:demo:import"]))
) -> JSONResponse:
    """
    导入示例
    
    参数:
    - file (UploadFile): 导入的Excel文件
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含导入示例详情的JSON响应
    """
    batch_import_result = await DemoService.batch_import_service(file=file, auth=auth, update_support=True)
    log.info(f"导入示例成功: {batch_import_result}")
    return SuccessResponse(data=batch_import_result, msg="导入示例成功")

@DemoRouter.post('/download/template', summary="获取示例导入模板", description="获取示例导入模板", dependencies=[Depends(AuthPermission(["module_example:demo:download"]))])
async def export_obj_template_controller() -> StreamingResponse:
    """
    获取示例导入模板
    
    返回:
    - StreamingResponse: 包含示例导入模板的Excel文件流响应
    """
    example_import_template_result = await DemoService.import_template_download_service()
    log.info('获取示例导入模板成功')

    return StreamResponse(
        data=bytes2file_response(example_import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': f'attachment; filename={urllib.parse.quote("示例导入模板.xlsx")}',
            'Access-Control-Expose-Headers': 'Content-Disposition'
        }
    )