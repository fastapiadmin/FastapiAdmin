# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.common.request import PaginationService
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.base_schema import BatchSetAvailable
from app.core.logger import log

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.router_class import OperationLogRoute
from .service import ApplicationService
from .schema import (
    ApplicationCreateSchema,
    ApplicationUpdateSchema,
    ApplicationQueryParam
)


MyAppRouter = APIRouter(route_class=OperationLogRoute, prefix="/myapp", tags=["应用管理"])

@MyAppRouter.get("/detail/{id}", summary="获取应用详情", description="获取应用详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="应用ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_application:myapp:detail"]))
) -> JSONResponse:
    """
    获取应用详情
    
    参数:
    - id (int): 应用ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含应用详情的JSON响应
    """
    result_dict = await ApplicationService.detail_service(id=id, auth=auth)
    log.info(f"获取应用详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取应用详情成功")

@MyAppRouter.get("/list", summary="查询应用列表", description="查询应用列表")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ApplicationQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_application:myapp:query"]))
) -> JSONResponse:
    """
    查询应用列表
    
    参数:
    - page (PaginationQueryParam): 分页参数模型
    - search (ApplicationQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含应用列表的JSON响应
    """
    result_dict_list = await ApplicationService.list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.paginate(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    log.info(f"查询应用列表成功")
    return SuccessResponse(data=result_dict, msg="查询应用列表成功")

@MyAppRouter.post("/create", summary="创建应用", description="创建应用")
async def create_obj_controller(
    data: ApplicationCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_application:myapp:create"]))
) -> JSONResponse:
    """
    创建应用
    
    参数:
    - data (ApplicationCreateSchema): 应用创建模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含创建应用详情的JSON响应
    """
    result_dict = await ApplicationService.create_service(auth=auth, data=data)
    log.info(f"创建应用成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建应用成功")

@MyAppRouter.put("/update/{id}", summary="修改应用", description="修改应用")
async def update_obj_controller(
    data: ApplicationUpdateSchema,
    id: int = Path(..., description="应用ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_application:myapp:update"]))
) -> JSONResponse:
    """
    修改应用
    
    参数:
    - data (ApplicationUpdateSchema): 应用更新模型
    - id (int): 应用ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含修改应用详情的JSON响应
    """
    result_dict = await ApplicationService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改应用成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改应用成功")

@MyAppRouter.delete("/delete", summary="删除应用", description="删除应用")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_application:myapp:delete"]))
) -> JSONResponse:
    """
    删除应用
    
    参数:
    - ids (list[int]): 应用ID列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含删除应用详情的JSON响应
    """
    await ApplicationService.delete_service(auth=auth, ids=ids)
    log.info(f"删除应用成功: {ids}")
    return SuccessResponse(msg="删除应用成功")

@MyAppRouter.patch("/available/setting", summary="批量修改应用状态", description="批量修改应用状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_application:myapp:patch"]))
) -> JSONResponse:
    """
    批量修改应用状态
    
    参数:
    - data (BatchSetAvailable): 批量修改应用状态模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 批量修改应用状态成功
    """
    await ApplicationService.set_available_service(auth=auth, data=data)
    log.info(f"批量修改应用状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改应用状态成功")