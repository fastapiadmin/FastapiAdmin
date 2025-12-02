# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.base_schema import BatchSetAvailable
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from ..auth.schema import AuthSchema
from .service import MenuService
from .schema import (
    MenuCreateSchema,
    MenuUpdateSchema,
    MenuQueryParam
)

MenuRouter = APIRouter(route_class=OperationLogRoute, prefix="/menu", tags=["菜单管理"])


@MenuRouter.get("/tree", summary="查询菜单树", description="查询菜单树")
async def get_menu_tree_controller(
    search: MenuQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_system:menu:query"]))
) -> JSONResponse:
    """
    查询菜单树。
    
    参数:
    - search (MenuQueryParam): 查询参数模型。
    
    返回:
    - JSONResponse: 包含菜单树的 JSON 响应。
    """
    order_by = [{"order": "asc"}]
    result_dict_list = await MenuService.get_menu_tree_service(search=search, auth=auth, order_by=order_by)
    log.info(f"查询菜单树成功")
    return SuccessResponse(data=result_dict_list, msg="查询菜单树成功")


@MenuRouter.get("/detail/{id}", summary="查询菜单详情", description="查询菜单详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="菜单ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:menu:query"]))
) -> JSONResponse:
    """
    查询菜单详情。
    
    参数:
    - id (int): 菜单ID。
    
    返回:
    - JSONResponse: 包含菜单详情的 JSON 响应。
    """
    result_dict = await MenuService.get_menu_detail_service(id=id, auth=auth)
    log.info(f"查询菜单情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取菜单成功")


@MenuRouter.post("/create", summary="创建菜单", description="创建菜单")
async def create_obj_controller(
    data: MenuCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_system:menu:create"]))
) -> JSONResponse:
    """
    创建菜单。
    
    参数:
    - data (MenuCreateSchema): 菜单创建模型。
    
    返回:
    - JSONResponse: 包含创建菜单的 JSON 响应。
    """
    result_dict = await MenuService.create_menu_service(data=data, auth=auth)
    log.info(f"创建菜单成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建菜单成功")


@MenuRouter.put("/update/{id}", summary="修改菜单", description="修改菜单")
async def update_obj_controller(
    data: MenuUpdateSchema,
    id: int = Path(..., description="菜单ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:menu:update"]))
) -> JSONResponse:
    """
    修改菜单。
    
    参数:
    - id (int): 菜单ID。
    - data (MenuUpdateSchema): 菜单更新模型。
    
    返回:
    - JSONResponse: 包含修改菜单的 JSON 响应。
    """
    result_dict = await MenuService.update_menu_service(id=id, data=data, auth=auth)
    log.info(f"修改菜单成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改菜单成功")


@MenuRouter.delete("/delete", summary="删除菜单", description="删除菜单")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_system:menu:delete"]))
) -> JSONResponse:
    """
    删除菜单。
    
    参数:
    - ids (list[int]): 菜单ID列表。
    
    返回:
    - JSONResponse: 包含删除菜单的 JSON 响应。
    """
    await MenuService.delete_menu_service(ids=ids, auth=auth)
    log.info(f"删除菜单成功: {ids}")
    return SuccessResponse(msg="删除菜单成功")


@MenuRouter.patch("/available/setting", summary="批量修改菜单状态", description="批量修改菜单状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_system:menu:patch"]))
) -> JSONResponse:
    """
    批量修改菜单状态。
    
    参数:
    - data (BatchSetAvailable): 批量修改菜单状态模型。
    
    返回:
    - JSONResponse: 批量修改菜单状态的 JSON 响应。
    """
    await MenuService.set_menu_available_service(data=data, auth=auth)
    log.info(f"批量修改菜单状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改菜单状态成功")