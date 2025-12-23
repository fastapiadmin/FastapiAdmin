# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.router_class import OperationLogRoute
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.base_schema import BatchSetAvailable
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .service import TokenService
from .schema import (
    TokenCreateSchema,
    TokenUpdateSchema,
    TokenQueryParam
)


TokenRouter = APIRouter(route_class=OperationLogRoute, prefix="/token", tags=["令牌模块"])

@TokenRouter.get("/detail/{id}", summary="获取令牌详情", description="获取令牌详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="令牌ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:token:detail"]))
) -> JSONResponse:
    """
    获取令牌详情
    
    参数:
    - id (int): 令牌ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含令牌详情的JSON响应
    """
    result_dict = await TokenService.detail_service(id=id, auth=auth)
    log.info(f"获取令牌详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取令牌详情成功")

@TokenRouter.get("/list", summary="查询令牌列表", description="查询令牌列表")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: TokenQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:token:query"]))
) -> JSONResponse:
    """
    查询令牌列表
    
    参数:
    - page (PaginationQueryParam): 分页查询参数
    - search (TokenQueryParam): 查询参数
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含令牌列表分页信息的JSON响应
    """
    # 使用数据库分页而不是应用层分页
    result_dict = await TokenService.page_service(
        auth=auth, 
        page_no=page.page_no, 
        page_size=page.page_size, 
        search=search, 
        order_by=page.order_by
    )
    log.info("查询令牌列表成功")
    return SuccessResponse(data=result_dict, msg="查询令牌列表成功")

@TokenRouter.post("/create", summary="创建令牌", description="创建令牌")
async def create_obj_controller(
    data: TokenCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_system:token:create"]))
) -> JSONResponse:
    """
    创建令牌
    
    参数:
    - data (TokenCreateSchema): 令牌创建模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含创建令牌详情的JSON响应
    """
    result_dict = await TokenService.create_service(auth=auth, data=data)
    log.info(f"创建令牌成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="创建令牌成功")

@TokenRouter.put("/update/{id}", summary="修改令牌", description="修改令牌")
async def update_obj_controller(
    data: TokenUpdateSchema,
    id: int = Path(..., description="令牌ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:token:update"]))
) -> JSONResponse:
    """
    修改令牌
    
    参数:
    - data (TokenUpdateSchema): 令牌更新模型
    - id (int): 令牌ID
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含修改令牌详情的JSON响应
    """
    result_dict = await TokenService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改令牌成功: {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="修改令牌成功")

@TokenRouter.delete("/delete", summary="删除令牌", description="删除令牌")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:token:delete"]))
) -> JSONResponse:
    """
    删除令牌
    
    参数:
    - ids (list[int]): 令牌ID列表
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含删除令牌详情的JSON响应
    """
    await TokenService.delete_service(auth=auth, ids=ids)
    log.info(f"删除令牌成功: {ids}")
    return SuccessResponse(msg="删除令牌成功")

@TokenRouter.patch("/available/setting", summary="批量修改令牌状态", description="批量修改令牌状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_system:token:patch"]))
) -> JSONResponse:
    """
    批量修改令牌状态
    
    参数:
    - data (BatchSetAvailable): 批量修改令牌状态模型
    - auth (AuthSchema): 认证信息模型
    
    返回:
    - JSONResponse: 包含批量修改令牌状态详情的JSON响应
    """
    await TokenService.set_available_service(auth=auth, data=data)
    log.info(f"批量修改令牌状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改令牌状态成功")
