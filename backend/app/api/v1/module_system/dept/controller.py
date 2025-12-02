# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.base_schema import BatchSetAvailable
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from ..auth.schema import AuthSchema
from .service import DeptService
from .schema import (
    DeptCreateSchema,
    DeptUpdateSchema,
    DeptQueryParam
)


DeptRouter = APIRouter(route_class=OperationLogRoute, prefix="/dept", tags=["部门管理"])


@DeptRouter.get("/tree", summary="查询部门树", description="查询部门树")
async def get_dept_tree_controller(
    search: DeptQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:dept:query"]))
) -> JSONResponse:
    """
    查询部门树

    参数:
    - search (DeptQueryParam): 查询参数模型
    - auth (AuthSchema): 认证信息模型
        
    返回:
    - JSONResponse: 包含部门树的响应模型
        
    异常:
    - CustomException: 查询部门树失败时抛出异常。
    """
    order_by = [{"order": "asc"}]
    result_dict_list = await DeptService.get_dept_tree_service(search=search, auth=auth, order_by=order_by)
    log.info(f"查询部门树成功")
    return SuccessResponse(data=result_dict_list, msg="查询部门树成功")


@DeptRouter.get("/detail/{id}", summary="查询部门详情", description="查询部门详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="部门ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:dept:query"]))
) -> JSONResponse:
    """
    查询部门详情

    参数:
    - id (int): 部门ID
    - auth (AuthSchema): 认证信息模型
        
    返回:
    - JSONResponse: 包含部门详情的响应模型
        
    异常:
    - CustomException: 查询部门详情失败时抛出异常。
    """
    result_dict = await DeptService.get_dept_detail_service(id=id, auth=auth)
    log.info(f"查询部门详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="查询部门详情成功")


@DeptRouter.post("/create", summary="创建部门", description="创建部门")
async def create_obj_controller(
    data: DeptCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_system:dept:create"]))
) -> JSONResponse:
    """
    创建部门

    参数:
    - data (DeptCreateSchema): 创建部门负载模型
    - auth (AuthSchema): 认证信息模型
        
    返回:
    - JSONResponse: 包含创建部门结果的响应模型
        
    异常:
    - CustomException: 创建部门失败时抛出异常。
    """
    result_dict = await DeptService.create_dept_service(data=data, auth=auth)
    log.info(f"创建部门成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建部门成功")


@DeptRouter.put("/update/{id}", summary="修改部门", description="修改部门")
async def update_obj_controller(
    data: DeptUpdateSchema,
    id: int = Path(..., description="部门ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:dept:update"]))
) -> JSONResponse:
    """
    修改部门

    参数:
    - data (DeptUpdateSchema): 修改部门负载模型
    - id (int): 部门ID
    - auth (AuthSchema): 认证信息模型
        
    返回:
    - JSONResponse: 包含修改部门结果的响应模型
        
    异常:
    - CustomException: 修改部门失败时抛出异常。
    """
    result_dict = await DeptService.update_dept_service(auth=auth, id=id, data=data)
    log.info(f"修改部门成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改部门成功")


@DeptRouter.delete("/delete", summary="删除部门", description="删除部门")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:dept:delete"]))
) -> JSONResponse:
    """
    删除部门

    参数:
    - ids (list[int]): 部门ID列表
    - auth (AuthSchema): 认证信息模型
        
    返回:
    - JSONResponse: 包含删除部门结果的响应模型
        
    异常:
    - CustomException: 删除部门失败时抛出异常。
    """
    await DeptService.delete_dept_service(ids=ids, auth=auth)
    log.info(f"删除部门成功: {ids}")
    return SuccessResponse(msg="删除部门成功")


@DeptRouter.patch("/available/setting", summary="批量修改部门状态", description="批量修改部门状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_system:dept:patch"]))
) -> JSONResponse:
    """
    批量修改部门状态

    参数:
    - data (BatchSetAvailable): 批量修改部门状态负载模型
    - auth (AuthSchema): 认证信息模型
        
    返回:
    - JSONResponse: 包含批量修改部门状态结果的响应模型
        
    异常:
    - CustomException: 批量修改部门状态失败时抛出异常。
    """
    await DeptService.batch_set_available_service(data=data, auth=auth)
    log.info(f"批量修改部门状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改部门状态成功")
