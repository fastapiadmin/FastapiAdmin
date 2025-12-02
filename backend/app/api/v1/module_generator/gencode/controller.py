# -*- coding: utf-8 -*-

from typing import List
from fastapi import APIRouter, Depends, Body, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.core.base_params import PaginationQueryParam
from app.common.request import PaginationService
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema

from .schema import GenTableSchema, GenTableQueryParam
from .service import GenTableService


GenRouter = APIRouter(route_class=OperationLogRoute, prefix='/gencode', tags=["代码生成模块"])


@GenRouter.get("/list", summary="查询代码生成业务表列表", description="查询代码生成业务表列表")
async def gen_table_list_controller(
    page: PaginationQueryParam = Depends(),
    search: GenTableQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:gencode:query"]))
) -> JSONResponse:
    """
    查询代码生成业务表列表
    
    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (GenTableQueryParam): 搜索参数
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含查询结果和分页信息的JSON响应
    """
    result_dict_list = await GenTableService.get_gen_table_list_service(auth=auth, search=search)
    result_dict = await PaginationService.paginate(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    log.info('获取代码生成业务表列表成功')
    return SuccessResponse(data=result_dict, msg="获取代码生成业务表列表成功")


@GenRouter.get("/db/list", summary="查询数据库表列表", description="查询数据库表列表")
async def get_gen_db_table_list_controller(
    page: PaginationQueryParam = Depends(),
    search: GenTableQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:dblist:query"]))
) -> JSONResponse:
    """
    查询数据库表列表
    
    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (GenTableQueryParam): 搜索参数
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含查询结果和分页信息的JSON响应
    """
    result_dict_list = await GenTableService.get_gen_db_table_list_service(auth=auth, search=search)
    result_dict = await PaginationService.paginate(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    log.info('获取数据库表列表成功')
    return SuccessResponse(data=result_dict, msg="获取数据库表列表成功")


@GenRouter.post("/import", summary="导入表结构", description="导入表结构")
async def import_gen_table_controller(
    table_names: List[str] = Body(..., description="表名列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:gencode:import"])),
) -> JSONResponse:
    """
    导入表结构
    
    参数:
    - table_names (List[str]): 表名列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含导入结果和导入的表结构列表的JSON响应
    """
    add_gen_table_list = await GenTableService.get_gen_db_table_list_by_name_service(auth, table_names)
    result = await GenTableService.import_gen_table_service(auth, add_gen_table_list)
    log.info('导入表结构成功')
    return SuccessResponse(msg="导入表结构成功", data=result)


@GenRouter.get("/detail/{table_id}", summary="获取业务表详细信息", description="获取业务表详细信息")
async def gen_table_detail_controller(
    table_id: int = Path(..., description="业务表ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:gencode:query"]))
) -> JSONResponse:
    """
    获取业务表详细信息
    
    参数:
    - table_id (int): 业务表ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含业务表详细信息的JSON响应
    """
    gen_table_detail_result = await GenTableService.get_gen_table_detail_service(auth, table_id)
    log.info(f'获取table_id为{table_id}的信息成功')
    return SuccessResponse(data=gen_table_detail_result, msg="获取业务表详细信息成功")


@GenRouter.post("/create", summary="创建表结构", description="创建表结构")
async def create_table_controller(
    sql: str = Body(..., description="SQL语句，用于创建表结构"),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:gencode:create"])),
) -> JSONResponse:
    """
    创建表结构
    
    参数:
    - sql (str): SQL语句，用于创建表结构
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含创建结果的JSON响应
    """
    result = await GenTableService.create_table_service(auth, sql)
    log.info('创建表结构成功')
    return SuccessResponse(msg="创建表结构成功", data=result)


@GenRouter.put("/update/{table_id}", summary="编辑业务表信息", description="编辑业务表信息")
async def update_gen_table_controller(
    table_id: int = Path(..., description="业务表ID"),
    data: GenTableSchema = Body(..., description="业务表信息"),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:gencode:update"])),
) -> JSONResponse:
    """
    编辑业务表信息
    
    参数:
    - table_id (int): 业务表ID
    - data (GenTableSchema): 业务表信息模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含编辑结果的JSON响应
    """
    result_dict = await GenTableService.update_gen_table_service(auth, data, table_id)
    log.info('编辑业务表信息成功')
    return SuccessResponse(data=result_dict, msg="编辑业务表信息成功")


@GenRouter.delete("/delete", summary="删除业务表信息", description="删除业务表信息")
async def delete_gen_table_controller(
    ids: List[int] = Body(..., description="业务表ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:gencode:delete"]))
) -> JSONResponse:
    """
    删除业务表信息
    
    参数:
    - ids (List[int]): 业务表ID列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含删除结果的JSON响应
    """
    result = await GenTableService.delete_gen_table_service(auth, ids)
    log.info('删除业务表信息成功')
    return SuccessResponse(msg="删除业务表信息成功", data=result)


@GenRouter.patch("/batch/output", summary="批量生成代码", description="批量生成代码")
async def batch_gen_code_controller(
    table_names: List[str] = Body(..., description="表名列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:gencode:patch"]))
) -> StreamResponse:
    """
    批量生成代码
    
    参数:
    - table_names (List[str]): 表名列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - StreamResponse: 包含批量生成代码的ZIP文件流响应
    """
    batch_gen_code_result = await GenTableService.batch_gen_code_service(auth, table_names)
    log.info(f'批量生成代码成功,表名列表：{table_names}')
    return StreamResponse(
        data=bytes2file_response(batch_gen_code_result),
        media_type='application/zip',
        headers={'Content-Disposition': 'attachment; filename=code.zip'}
    )


@GenRouter.post("/output/{table_name}", summary="生成代码到指定路径", description="生成代码到指定路径")
async def gen_code_local_controller(
    table_name: str = Path(..., description="表名"),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:gencode:code"]))
) -> JSONResponse:
    """
    生成代码到指定路径
    
    参数:
    - table_name (str): 表名
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含生成结果的JSON响应
    """
    result = await GenTableService.generate_code_service(auth, table_name)
    log.info(f'生成代码,表名：{table_name},到指定路径成功')
    return SuccessResponse(msg="生成代码到指定路径成功", data=result)


@GenRouter.get("/preview/{table_id}", summary="预览代码", description="预览代码")
async def preview_code_controller(
    table_id: int = Path(..., description="业务表ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:gencode:query"]))
) -> JSONResponse:
    """
    预览代码
    
    参数:
    - table_id (int): 业务表ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含预览代码的JSON响应
    """
    preview_code_result = await GenTableService.preview_code_service(auth, table_id)
    log.info(f'预览代码,表id：{table_id},成功')
    return SuccessResponse(data=preview_code_result, msg="预览代码成功")


@GenRouter.post("/sync_db/{table_name}", summary="同步数据库", description="同步数据库")
async def sync_db_controller(
    table_name: str = Path(..., description="表名"),
    auth: AuthSchema = Depends(AuthPermission(["module_generator:db:sync"]))
) -> JSONResponse:
    """
    同步数据库
    
    参数:
    - table_name (str): 表名
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含同步数据库结果的JSON响应
    """
    result = await GenTableService.sync_db_service(auth, table_name)
    log.info(f'同步数据库,表名：{table_name},成功')
    return SuccessResponse(msg="同步数据库成功", data=result)