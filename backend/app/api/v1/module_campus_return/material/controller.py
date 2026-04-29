"""
物料领取 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

MaterialRouter = APIRouter(prefix="/material", tags=["物料领取"])


@MaterialRouter.get("/list", summary="物料列表")
async def list_material_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:material:query"]))],
    batch_id: Annotated[int | None, Query(description="批次ID")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量")] = 10,
) -> ResponseSchema[list]:
    """获取物料列表"""
    return ResponseSchema(data=[])


@MaterialRouter.get("/{material_id}", summary="物料详情")
async def get_material_controller(
    material_id: Annotated[int, Path(description="物料ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:material:query"]))],
) -> ResponseSchema[dict]:
    """获取单个物料详情"""
    return ResponseSchema(data={})


@MaterialRouter.post("/claim", summary="申领物料")
async def claim_material_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:material:claim"]))],
) -> ResponseSchema[dict]:
    """申领物料"""
    return ResponseSchema(data={})


@MaterialRouter.post("/receive", summary="领取登记")
async def receive_material_controller(
    data: dict,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:material:receive"]))],
) -> ResponseSchema[dict]:
    """线下领取登记"""
    return ResponseSchema(data={})
