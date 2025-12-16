# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, UploadFile, Body, Path, Query
from fastapi.responses import StreamingResponse, JSONResponse

from app.common.response import SuccessResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_params import PaginationQueryParam
from app.utils.common_util import bytes2file_response
from app.core.logger import log
from app.core.base_schema import BatchSetAvailable

from .service import GenDemo01Service
from .schema import GenDemo01CreateSchema, GenDemo01UpdateSchema, GenDemo01QueryParam

GenDemo01Router = APIRouter(prefix='/gen_demo01', tags=["示例模块"]) 

@GenDemo01Router.get("/detail/{id}", summary="获取示例详情", description="获取示例详情")
async def get_gen_demo01_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:gen_demo01:query"]))
) -> JSONResponse:
    """获取示例详情接口"""
    result_dict = await GenDemo01Service.detail_gen_demo01_service(auth=auth, id=id)
    log.info(f"获取示例详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取示例详情成功")

@GenDemo01Router.get("/list", summary="查询示例列表", description="查询示例列表")
async def get_gen_demo01_list_controller(
    page: PaginationQueryParam = Depends(),
    search: GenDemo01QueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:gen_demo01:query"]))
) -> JSONResponse:
    """查询示例列表接口（数据库分页）"""
    result_dict = await GenDemo01Service.page_gen_demo01_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询示例列表成功")
    return SuccessResponse(data=result_dict, msg="查询示例列表成功")

@GenDemo01Router.post("/create", summary="创建示例", description="创建示例")
async def create_gen_demo01_controller(
    data: GenDemo01CreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:gen_demo01:create"]))
) -> JSONResponse:
    """创建示例接口"""
    result_dict = await GenDemo01Service.create_gen_demo01_service(auth=auth, data=data)
    log.info("创建示例成功")
    return SuccessResponse(data=result_dict, msg="创建示例成功")

@GenDemo01Router.put("/update/{id}", summary="修改示例", description="修改示例")
async def update_gen_demo01_controller(
    data: GenDemo01UpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:gen_demo01:update"]))
) -> JSONResponse:
    """修改示例接口"""
    result_dict = await GenDemo01Service.update_gen_demo01_service(auth=auth, id=id, data=data)
    log.info("修改示例成功")
    return SuccessResponse(data=result_dict, msg="修改示例成功")

@GenDemo01Router.delete("/delete", summary="删除示例", description="删除示例")
async def delete_gen_demo01_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:gen_demo01:delete"]))
) -> JSONResponse:
    """删除示例接口"""
    await GenDemo01Service.delete_gen_demo01_service(auth=auth, ids=ids)
    log.info(f"删除示例成功: {ids}")
    return SuccessResponse(msg="删除示例成功")

@GenDemo01Router.patch("/available/setting", summary="批量修改示例状态", description="批量修改示例状态")
async def batch_set_available_gen_demo01_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:gen_demo01:patch"]))
) -> JSONResponse:
    """批量修改示例状态接口"""
    await GenDemo01Service.set_available_gen_demo01_service(auth=auth, data=data)
    log.info(f"批量修改示例状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改示例状态成功")

@GenDemo01Router.post('/export', summary="导出示例", description="导出示例")
async def export_gen_demo01_list_controller(
    search: GenDemo01QueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:gen_demo01:export"]))
) -> StreamingResponse:
    """导出示例接口"""
    result_dict_list = await GenDemo01Service.list_gen_demo01_service(search=search, auth=auth)
    export_result = await GenDemo01Service.batch_export_gen_demo01_service(obj_list=result_dict_list)
    log.info('导出示例成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=gen_demo01.xlsx'
        }
    )

@GenDemo01Router.post('/import', summary="导入示例", description="导入示例")
async def import_gen_demo01_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:gen_demo01:import"]))
) -> JSONResponse:
    """导入示例接口"""
    batch_import_result = await GenDemo01Service.batch_import_gen_demo01_service(file=file, auth=auth, update_support=True)
    log.info("导入示例成功")
    
    return SuccessResponse(data=batch_import_result, msg="导入示例成功")

@GenDemo01Router.post('/download/template', summary="获取示例导入模板", description="获取示例导入模板", dependencies=[Depends(AuthPermission(["module_gencode:gen_demo01:download"]))])
async def export_gen_demo01_template_controller() -> StreamingResponse:
    """获取示例导入模板接口"""
    import_template_result = await GenDemo01Service.import_template_download_gen_demo01_service()
    log.info('获取示例导入模板成功')

    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=gen_demo01_template.xlsx'}
    )