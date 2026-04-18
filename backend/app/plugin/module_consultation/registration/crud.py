"""
咨询会报名管理 - 数据访问层
"""
from datetime import datetime
from typing import Any

from sqlalchemy import select, update, func

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase
from app.core.database import async_db_session

from .model import RegistrationModel
from .schema import RegistrationCreateSchema, RegistrationOutSchema, RegistrationUpdateSchema


class RegistrationCRUD(CRUDBase[RegistrationModel, RegistrationCreateSchema, RegistrationUpdateSchema]):
    """
    咨询会报名数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=RegistrationModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> RegistrationModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[RegistrationModel]:
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
            out_schema=RegistrationOutSchema,
        )

    async def create_crud(self, data: dict) -> RegistrationModel:
        """创建记录"""
        data["registration_time"] = datetime.now()
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> RegistrationModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def approve_crud(
        self,
        id: int,
        booth_number: str | None = None,
        booth_size: str | None = None,
        booth_fee: float | None = None,
        comment: str | None = None,
    ) -> RegistrationModel:
        """审核通过"""
        data = {
            "registration_status": "approved",
            "approval_time": datetime.now(),
            "approval_by": self.auth.user.id if self.auth.user else None,
            "approval_comment": comment,
        }
        if booth_number:
            data["booth_number"] = booth_number
        if booth_size:
            data["booth_size"] = booth_size
        return await self.update(id=id, data=data)

    async def reject_crud(self, id: int, comment: str) -> RegistrationModel:
        """审核拒绝"""
        data = {
            "registration_status": "rejected",
            "approval_time": datetime.now(),
            "approval_by": self.auth.user.id if self.auth.user else None,
            "approval_comment": comment,
        }
        return await self.update(id=id, data=data)

    async def cancel_crud(self, id: int, reason: str | None = None) -> RegistrationModel:
        """取消报名"""
        data = {
            "registration_status": "cancelled",
            "approval_comment": reason,
        }
        return await self.update(id=id, data=data)

    async def confirm_payment_crud(
        self, id: int, payment_time: datetime, comment: str | None = None
    ) -> RegistrationModel:
        """确认支付"""
        data = {
            "is_paid": True,
            "payment_time": payment_time,
        }
        if comment:
            data["approval_comment"] = comment
        return await self.update(id=id, data=data)

    async def get_by_consultation_and_university(
        self, consultation_id: int, university_id: int
    ) -> RegistrationModel | None:
        """根据咨询会和高校获取报名记录"""
        result = await self.list(
            search={
                "consultation_id": (consultation_id, "eq"),
                "university_id": (university_id, "eq"),
            }
        )
        return result[0] if result else None

    async def statistics_by_status_crud(self) -> dict:
        """按状态统计报名数量"""
        async with async_db_session() as session:
            stmt = select(
                RegistrationModel.registration_status,
                func.count(RegistrationModel.id).label("count"),
            ).group_by(RegistrationModel.registration_status)
            result = await session.execute(stmt)
            rows = result.all()
            return {row.registration_status: row.count for row in rows}

    async def statistics_by_consultation_crud(self, consultation_id: int) -> dict:
        """统计某咨询会的报名情况"""
        async with async_db_session() as session:
            stmt = select(
                RegistrationModel.registration_status,
                func.count(RegistrationModel.id).label("count"),
            ).where(RegistrationModel.consultation_id == consultation_id).group_by(
                RegistrationModel.registration_status
            )
            result = await session.execute(stmt)
            rows = result.all()
            return {row.registration_status: row.count for row in rows}
