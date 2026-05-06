"""
批次管理 - 业务逻辑
"""

from typing import Any

from app.api.v1.module_campus_return.batch.crud import BatchCRUD
from app.api.v1.module_campus_return.batch.schema import (
    BatchCreateSchema,
    BatchOutSchema,
    BatchUpdateSchema,
)
from app.core.dependencies import AuthSchema
from app.core.exceptions import CustomException


class BatchService:
    """批次服务类"""

    @classmethod
    async def create_batch(cls, data: BatchCreateSchema, auth: AuthSchema) -> BatchOutSchema:
        """创建批次"""
        crud = BatchCRUD(model=None, auth=auth)
        existing = await crud.get_by_batch_name(data.batch_name)
        if existing:
            raise CustomException(msg="批次名称已存在")

        batch = await crud.create(data=data, auth=auth)
        return BatchOutSchema.model_validate(batch)

    @classmethod
    async def update_batch(
        cls, batch_id: int, data: BatchUpdateSchema, auth: AuthSchema
    ) -> BatchOutSchema:
        """更新批次"""
        crud = BatchCRUD(model=None, auth=auth)
        batch = await crud.get_by_id(batch_id)
        if not batch:
            raise CustomException(msg="批次不存在")

        existing = await crud.get_by_batch_name(data.batch_name)
        if existing and existing.id != batch_id:
            raise CustomException(msg="批次名称已存在")

        updated = await crud.update(id=batch_id, data=data, auth=auth)
        return BatchOutSchema.model_validate(updated)

    @classmethod
    async def delete_batch(cls, batch_id: int, auth: AuthSchema) -> bool:
        """删除批次"""
        crud = BatchCRUD(model=None, auth=auth)
        batch = await crud.get_by_id(batch_id)
        if not batch:
            raise CustomException(msg="批次不存在")

        await crud.delete(ids=[batch_id])
        return True

    @classmethod
    async def get_batch(cls, batch_id: int, auth: AuthSchema) -> BatchOutSchema:
        """获取单个批次"""
        crud = BatchCRUD(model=None, auth=auth)
        batch = await crud.get_by_id(batch_id)
        if not batch:
            raise CustomException(msg="批次不存在")

        return BatchOutSchema.model_validate(batch)

    @classmethod
    async def list_batches(
        cls,
        page: int = 1,
        page_size: int = 10,
        batch_name: str | None = None,
        year: int | None = None,
        semester: str | None = None,
        status: str | None = None,
        is_active: bool | None = None,
        auth: AuthSchema | None = None,
    ) -> dict[str, Any]:
        """获取批次列表"""
        crud = BatchCRUD(model=None, auth=auth) if auth else None
        search = {}
        if batch_name:
            search["batch_name"] = ("like", f"%{batch_name}%")
        if year:
            search["year"] = year
        if semester:
            search["semester"] = semester
        if status:
            search["status"] = status
        if is_active is not None:
            search["is_active"] = is_active

        order_by = [{"order": "asc"}]
        if crud:
            result, total = await crud.get_list(
                search=search, order_by=order_by, page=page, page_size=page_size
            )
        else:
            result, total = [], 0

        return {
            "list": [BatchOutSchema.model_validate(r) for r in result],
            "total": total,
            "page": page,
            "page_size": page_size,
        }


batch_service = BatchService()
