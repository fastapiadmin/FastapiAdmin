"""
高中对接 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

HighSchoolRouter = APIRouter(prefix="/highschool", tags=["高中对接"])


@HighSchoolRouter.get("/docking", summary="对接列表")
async def list_docking_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:highschool:query"]))],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取高中对接列表"""
    return ResponseSchema(data=[])


@HighSchoolRouter.get("/docking/{docking_id}", summary="对接详情")
async def get_docking_controller(
    docking_id: Annotated[int, Path(description="对接ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:highschool:query"]))],
) -> ResponseSchema[dict]:
    """获取单个对接详情"""
    return ResponseSchema(data={})


@HighSchoolRouter.post("/docking", summary="创建对接")
async def create_docking_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:highschool:create"]))],
) -> ResponseSchema[dict]:
    """创建高中对接"""
    return ResponseSchema(data={})


@HighSchoolRouter.put("/docking/{docking_id}", summary="更新对接")
async def update_docking_controller(
    docking_id: Annotated[int, Path(description="对接ID")],
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:highschool:update"]))],
) -> ResponseSchema[dict]:
    """更新高中对接"""
    return ResponseSchema(data={})


@HighSchoolRouter.delete("/docking/{docking_id}", summary="删除对接")
async def delete_docking_controller(
    docking_id: Annotated[int, Path(description="对接ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:highschool:delete"]))],
) -> ResponseSchema[bool]:
    """删除高中对接"""
    return ResponseSchema(data=True)
