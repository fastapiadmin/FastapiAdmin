from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse
from app.core import cache_util
from app.core.base_schema import AuthSchema, BatchSetAvailable
from app.core.cache_util import cache
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

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
    search: Annotated[DeptQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:query"]))],
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
    id: Annotated[int, Path(description="部门ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:detail"]))],
) -> JSONResponse:
    result_dict = await DeptService(auth).detail(id=id)
    return SuccessResponse(data=result_dict, msg="查询部门详情成功")

@DeptRouter.post(
    "/create",
    summary="创建部门",
    response_model=ResponseSchema[DeptOutSchema],
)
async def create_obj_controller(
    data: DeptCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:create"]))],
) -> JSONResponse:
    result_dict = await DeptService(auth).create(data=data)
    await cache_util.clear(namespace=_DEPT_NS)
    return SuccessResponse(data=result_dict, msg="创建部门成功")

@DeptRouter.put(
    "/update/{id}",
    summary="修改部门",
    response_model=ResponseSchema[DeptOutSchema],
)
async def update_obj_controller(
    data: DeptUpdateSchema,
    id: Annotated[int, Path(description="部门ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:update"]))],
) -> JSONResponse:
    result_dict = await DeptService(auth).update(id=id, data=data)
    await cache_util.clear(namespace=_DEPT_NS)
    return SuccessResponse(data=result_dict, msg="修改部门成功")

@DeptRouter.delete(
    "/delete",
    summary="删除部门",
    response_model=ResponseSchema[None],
)
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:delete"]))],
) -> JSONResponse:
    await DeptService(auth).delete(ids=ids)
    await cache_util.clear(namespace=_DEPT_NS)
    return SuccessResponse(msg="删除部门成功")

@DeptRouter.patch(
    "/status/batch",
    summary="批量修改部门状态",
    response_model=ResponseSchema[None],
)
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:dept:patch"]))],
) -> JSONResponse:
    await DeptService(auth).batch_set_available(data=data)
    await cache_util.clear(namespace=_DEPT_NS)
    return SuccessResponse(msg="批量修改部门状态成功")
