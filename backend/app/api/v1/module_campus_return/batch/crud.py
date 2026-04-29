"""
批次管理 - CRUD操作
"""

from typing import Any

from sqlalchemy import select

from app.api.v1.module_campus_return.batch.model import CampusReturnBatchModel
from app.core.base_crud import CRUDBase


class BatchCRUD(CRUDBase):
    """批次CRUD操作类"""

    async def get_list(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, Any]] | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[CampusReturnBatchModel], int]:
        """获取批次列表"""
        return await self.get_list_distinct(
            search=search,
            order_by=order_by,
            page=page,
            page_size=page_size,
        )

    async def get_by_batch_name(self, batch_name: str) -> CampusReturnBatchModel | None:
        """根据批次名称获取批次"""
        stmt = select(CampusReturnBatchModel).where(CampusReturnBatchModel.batch_name == batch_name)
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_batches(self) -> list[CampusReturnBatchModel]:
        """获取激活的批次列表"""
        stmt = (
            select(CampusReturnBatchModel)
            .where(CampusReturnBatchModel.is_active)
            .order_by(
                CampusReturnBatchModel.year.desc(), CampusReturnBatchModel.created_time.desc()
            )
        )
        result = await self._db.execute(stmt)
        return list(result.scalars().all())
