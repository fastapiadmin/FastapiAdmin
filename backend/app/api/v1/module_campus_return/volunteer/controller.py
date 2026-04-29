"""
志愿服务时长 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

VolunteerRouter = APIRouter(prefix="/volunteer", tags=["志愿服务时长"])


@VolunteerRouter.get("", summary="志愿时长列表")
async def list_volunteer_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:volunteer:query"]))],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取志愿服务时长列表"""
    return ResponseSchema(data=[])


@VolunteerRouter.get("/{volunteer_id}", summary="志愿时长详情")
async def get_volunteer_controller(
    volunteer_id: Annotated[int, Path(description="记录ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:volunteer:query"]))],
) -> ResponseSchema[dict]:
    """获取单个志愿服务时长详情"""
    return ResponseSchema(data={})


@VolunteerRouter.post("", summary="记录时长")
async def create_volunteer_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:volunteer:create"]))],
) -> ResponseSchema[dict]:
    """记录志愿服务时长"""
    return ResponseSchema(data={})


@VolunteerRouter.put("/{volunteer_id}", summary="更新时长")
async def update_volunteer_controller(
    volunteer_id: Annotated[int, Path(description="记录ID")],
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:volunteer:update"]))],
) -> ResponseSchema[dict]:
    """更新志愿服务时长"""
    return ResponseSchema(data={})
