from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_schema import AuthSchema, BatchSetAvailable
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from .schema import DeptCreateSchema, DeptOutSchema, DeptQueryParam, DeptUpdateSchema
from .service import DeptService

DeptRouter = APIRouter(route_class=OperationLogRoute, prefix="/dept", tags=["系统管理", "部门管理"])

_DEPT_NS = "dept"

@DeptRouter.get(
    "/tree",
    summary="查询部门树",
    response_model=ResponseSchema[list[DeptOutSchema]],
)
@cache(expire=300, namespace=_DEPT_NS)
async def get_dept_tree_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:query"]))],
    search: Annotated[DeptQueryParam, Query(description="部门查询参数")],
) -> JSONResponse:
    order_by = [{"order": "asc"}]
    result_dict_tree = await DeptService(auth).tree(search=search, order_by=order_by)
    return SuccessResponse(data=result_dict_tree, msg="查询部门树成功")

@DeptRouter.get(
    "/detail/{id}",
    summary="查询部门详情",
    response_model=ResponseSchema[DeptOutSchema],
)
async def get_obj_detail_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:detail"]))],
    id: Annotated[int, Path(description="部门ID")],
) -> JSONResponse:
    result_dict = await DeptService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="查询部门详情成功")

@DeptRouter.post(
    "/create",
    summary="创建部门",
    response_model=ResponseSchema[DeptOutSchema],
)
async def create_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:create"]))],
    data: Annotated[DeptCreateSchema, Body(description="部门创建参数")],
) -> JSONResponse:
    result_dict = await DeptService(auth).create(data=data)
    await FastAPICache.clear(namespace=_DEPT_NS)
    return SuccessResponse(data=result_dict, msg="创建部门成功")

@DeptRouter.put(
    "/update/{id}",
    summary="修改部门",
    response_model=ResponseSchema[DeptOutSchema],
)
async def update_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:update"]))],
    id: Annotated[int, Path(description="部门ID")],
    data: Annotated[DeptUpdateSchema, Body(description="部门修改参数")],
) -> JSONResponse:
    result_dict = await DeptService(auth).update(id=id, data=data)
    await FastAPICache.clear(namespace=_DEPT_NS)
    return SuccessResponse(data=result_dict, msg="修改部门成功")

@DeptRouter.delete(
    "/delete",
    summary="删除部门",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:delete"]))],
    ids: Annotated[list[int], Body(description="ID列表")],
) -> JSONResponse:
    await DeptService(auth).delete(ids=ids)
    await FastAPICache.clear(namespace=_DEPT_NS)
    return SuccessResponse(msg="删除部门成功")

@DeptRouter.patch(
    "/status/batch",
    summary="批量修改部门状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_obj_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:patch"]))],
    data: Annotated[BatchSetAvailable, Body(description="批量修改部门状态参数")],
) -> JSONResponse:
    await DeptService(auth).batch_set_available(data=data)
    await FastAPICache.clear(namespace=_DEPT_NS)
    return SuccessResponse(msg="批量修改部门状态成功")
