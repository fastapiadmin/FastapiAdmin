"""
咨询会信息聚合 - 数据访问层
"""

from datetime import datetime
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase
from app.core.exceptions import CustomException

from .model import ConsultationInfoModel, InfoStatus
from .schema import InfoCollectionCreateSchema, InfoCollectionOutSchema, InfoCollectionUpdateSchema


class InfoCollectionCRUD(
    CRUDBase[ConsultationInfoModel, InfoCollectionCreateSchema, InfoCollectionUpdateSchema]
):
    """
    咨询会信息数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=ConsultationInfoModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> ConsultationInfoModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[ConsultationInfoModel]:
        """获取列表"""
        return await self.list(search=search, order_by=order_by)

    async def page_crud(
        self,
        offset: int,
        limit: int,
        order_by: list[dict[str, str]] | None = None,
        search: dict[str, Any] | None = None,
    ) -> dict:
        """分页查询"""
        return await self.page(
            offset=offset,
            limit=limit,
            order_by=order_by,
            search=search,
            out_schema=InfoCollectionOutSchema,
        )

    async def create_crud(self, data: dict) -> ConsultationInfoModel:
        """创建记录"""
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> ConsultationInfoModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def _update_status_crud(self, id: int, data: dict) -> ConsultationInfoModel:
        """状态审核更新（直接 UPDATE，减少行锁持有时间）"""
        from sqlalchemy import update

        values = {**data}
        if self.auth.user:
            values["updated_id"] = self.auth.user.id

        await self.auth.db.execute(
            update(ConsultationInfoModel).where(ConsultationInfoModel.id == id).values(**values)
        )
        await self.auth.db.flush()
        obj = await self.get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="更新失败，记录不存在")
        return obj

    async def approve_crud(
        self, id: int, review_comment: str | None = None
    ) -> ConsultationInfoModel:
        """审核通过"""
        data = {
            "status": InfoStatus.APPROVED.value,
            "review_comment": review_comment,
            "reviewed_by": self.auth.user.id if self.auth.user else None,
            "reviewed_time": datetime.now(),
        }
        return await self._update_status_crud(id, data)

    async def reject_crud(self, id: int, review_comment: str) -> ConsultationInfoModel:
        """审核拒绝"""
        data = {
            "status": InfoStatus.REJECTED.value,
            "review_comment": review_comment,
            "reviewed_by": self.auth.user.id if self.auth.user else None,
            "reviewed_time": datetime.now(),
        }
        return await self._update_status_crud(id, data)

    async def archive_crud(self, id: int) -> ConsultationInfoModel:
        """归档"""
        data = {
            "is_archived": True,
            "archived_by": self.auth.user.id if self.auth.user else None,
            "archived_time": datetime.now(),
        }
        return await self.update(id=id, data=data)
