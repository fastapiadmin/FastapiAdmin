"""
行程管理 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

ItineraryRouter = APIRouter(prefix="/itinerary", tags=["行程管理"])


@ItineraryRouter.get("", summary="行程列表")
async def list_itinerary_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:itinerary:query"]))],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取行程列表"""
    return ResponseSchema(data=[])


@ItineraryRouter.get("/{itinerary_id}", summary="行程详情")
async def get_itinerary_controller(
    itinerary_id: Annotated[int, Path(description="行程ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:itinerary:query"]))],
) -> ResponseSchema[dict]:
    """获取单个行程详情"""
    return ResponseSchema(data={})


@ItineraryRouter.post("", summary="创建行程")
async def create_itinerary_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:itinerary:create"]))],
) -> ResponseSchema[dict]:
    """创建行程"""
    return ResponseSchema(data={})


@ItineraryRouter.put("/{itinerary_id}", summary="更新行程")
async def update_itinerary_controller(
    itinerary_id: Annotated[int, Path(description="行程ID")],
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:itinerary:update"]))],
) -> ResponseSchema[dict]:
    """更新行程"""
    return ResponseSchema(data={})


@ItineraryRouter.delete("/{itinerary_id}", summary="删除行程")
async def delete_itinerary_controller(
    itinerary_id: Annotated[int, Path(description="行程ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:itinerary:delete"]))],
) -> ResponseSchema[bool]:
    """删除行程"""
    return ResponseSchema(data=True)
