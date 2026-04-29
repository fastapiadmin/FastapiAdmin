"""
打卡总结 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

CheckInRouter = APIRouter(prefix="/checkin", tags=["打卡总结"])


@CheckInRouter.get("", summary="打卡列表")
async def list_checkin_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:checkin:query"]))],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取打卡列表"""
    return ResponseSchema(data=[])


@CheckInRouter.get("/{checkin_id}", summary="打卡详情")
async def get_checkin_controller(
    checkin_id: Annotated[int, Path(description="打卡ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:checkin:query"]))],
) -> ResponseSchema[dict]:
    """获取单个打卡详情"""
    return ResponseSchema(data={})


@CheckInRouter.post("", summary="创建打卡")
async def create_checkin_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:checkin:create"]))],
) -> ResponseSchema[dict]:
    """创建打卡"""
    return ResponseSchema(data={})


@CheckInRouter.post("/summary", summary="提交总结")
async def submit_summary_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:checkin:summary"]))],
) -> ResponseSchema[dict]:
    """提交活动总结"""
    return ResponseSchema(data={})
