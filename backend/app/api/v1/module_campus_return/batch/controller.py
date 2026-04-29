"""
批次管理 - 路由控制器
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.api.v1.module_campus_return.batch.schema import (
    BatchCreateSchema,
    BatchOutSchema,
    BatchUpdateSchema,
)
from app.api.v1.module_campus_return.batch.service import batch_service
from app.common.response import ResponseSchema
from app.core.dependencies import AuthPermission, AuthSchema

BatchRouter = APIRouter(prefix="/batch", tags=["批次管理"])


@BatchRouter.post("", summary="创建批次")
async def create_batch_controller(
    data: BatchCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:batch:create"]))],
) -> ResponseSchema[BatchOutSchema]:
    """创建新批次"""
    batch = await batch_service.create_batch(data=data, auth=auth)
    return ResponseSchema(data=batch)


@BatchRouter.put("/{batch_id}", summary="更新批次")
async def update_batch_controller(
    batch_id: Annotated[int, Path(description="批次ID")],
    data: BatchUpdateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:batch:update"]))],
) -> ResponseSchema[BatchOutSchema]:
    """更新批次信息"""
    batch = await batch_service.update_batch(batch_id=batch_id, data=data, auth=auth)
    return ResponseSchema(data=batch)


@BatchRouter.delete("/{batch_id}", summary="删除批次")
async def delete_batch_controller(
    batch_id: Annotated[int, Path(description="批次ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:batch:delete"]))],
) -> ResponseSchema[bool]:
    """删除批次"""
    result = await batch_service.delete_batch(batch_id=batch_id, auth=auth)
    return ResponseSchema(data=result)


@BatchRouter.get("/{batch_id}", summary="获取批次详情")
async def get_batch_controller(
    batch_id: Annotated[int, Path(description="批次ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:batch:query"]))],
) -> ResponseSchema[BatchOutSchema]:
    """获取单个批次详情"""
    batch = await batch_service.get_batch(batch_id=batch_id, auth=auth)
    return ResponseSchema(data=batch)


@BatchRouter.get("", summary="获取批次列表")
async def list_batches_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_campus_return:batch:query"]))],
    page: Annotated[int, Query(description="页码", ge=1)] = 1,
    page_size: Annotated[int, Query(description="每页数量", ge=1, le=100)] = 10,
    batch_name: Annotated[str | None, Query(description="批次名称")] = None,
    year: Annotated[int | None, Query(description="年度")] = None,
    semester: Annotated[str | None, Query(description="学期")] = None,
    status: Annotated[str | None, Query(description="批次状态")] = None,
    is_active: Annotated[bool | None, Query(description="是否激活")] = None,
) -> ResponseSchema[dict]:
    """获取批次列表"""
    result = await batch_service.list_batches(
        page=page,
        page_size=page_size,
        batch_name=batch_name,
        year=year,
        semester=semester,
        status=status,
        is_active=is_active,
        auth=auth,
    )
    return ResponseSchema(data=result)
