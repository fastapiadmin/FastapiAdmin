"""
行程方案管理 - 数据访问层
"""
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import ItineraryModel
from .schema import ItineraryCreateSchema, ItineraryOutSchema, ItineraryUpdateSchema


class ItineraryCRUD(CRUDBase[ItineraryModel, ItineraryCreateSchema, ItineraryUpdateSchema]):
    """
    行程方案数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=ItineraryModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> ItineraryModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[ItineraryModel]:
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
            out_schema=ItineraryOutSchema,
        )

    async def create_crud(self, data: dict) -> ItineraryModel:
        """创建记录"""
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> ItineraryModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def confirm_crud(self, id: int) -> ItineraryModel:
        """确认行程方案"""
        return await self.update(id=id, data={"status": "confirmed"})

    async def execute_crud(self, id: int) -> ItineraryModel:
        """执行行程方案"""
        return await self.update(id=id, data={"status": "executed"})

    async def archive_crud(self, id: int) -> ItineraryModel:
        """归档行程方案"""
        return await self.update(id=id, data={"status": "archived"})

    async def sync_calendar_crud(self, id: int) -> ItineraryModel:
        """同步到日历"""
        return await self.update(id=id, data={"is_synced": True})

    async def add_consultation_crud(
        self, id: int, consultation_id: int, consultation_detail: dict
    ) -> ItineraryModel:
        """添加咨询会到行程"""
        obj = await self.get_by_id_crud(id)
        if not obj:
            return None

        consultation_ids = obj.consultation_ids or []
        consultation_details = obj.consultation_details or []

        if consultation_id not in consultation_ids:
            consultation_ids.append(consultation_id)
            consultation_details.append(consultation_detail)

        return await self.update(id=id, data={
            "consultation_ids": consultation_ids,
            "consultation_details": consultation_details,
        })

    async def remove_consultation_crud(self, id: int, consultation_id: int) -> ItineraryModel:
        """从行程中移除咨询会"""
        obj = await self.get_by_id_crud(id)
        if not obj:
            return None

        consultation_ids = obj.consultation_ids or []
        consultation_details = obj.consultation_details or []

        if consultation_id in consultation_ids:
            consultation_ids.remove(consultation_id)
            consultation_details = [
                d for d in consultation_details if d.get("id") != consultation_id
            ]

        return await self.update(id=id, data={
            "consultation_ids": consultation_ids,
            "consultation_details": consultation_details,
        })

    async def optimize_route_crud(self, id: int) -> ItineraryModel:
        """优化路线"""
        obj = await self.get_by_id_crud(id)
        if not obj:
            return None

        consultation_details = obj.consultation_details or []
        if len(consultation_details) < 2:
            return obj

        sorted_details = self._calculate_optimal_route(consultation_details)

        return await self.update(id=id, data={"consultation_details": sorted_details})

    def _calculate_optimal_route(self, consultations: list[dict]) -> list[dict]:
        """简单的贪心算法优化路线"""
        if not consultations:
            return consultations

        sorted_list = sorted(consultations, key=lambda x: (x.get("start_date", ""), x.get("city", "")))
        return sorted_list
