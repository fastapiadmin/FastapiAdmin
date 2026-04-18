"""
咨询会筛选匹配 - 数据访问层
"""
from datetime import datetime
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import ScreeningFilterModel
from .schema import ScreeningFilterCreateSchema, ScreeningFilterUpdateSchema


class ScreeningCRUD(CRUDBase[ScreeningFilterModel, ScreeningFilterCreateSchema, ScreeningFilterUpdateSchema]):
    """
    咨询会筛选数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=ScreeningFilterModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> ScreeningFilterModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[ScreeningFilterModel]:
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
        )

    async def create_crud(self, data: dict) -> ScreeningFilterModel:
        """创建记录"""
        if data.get("is_default"):
            await self._clear_default()
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> ScreeningFilterModel:
        """更新记录"""
        if data.get("is_default"):
            await self._clear_default()
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def set_default_crud(self, id: int) -> ScreeningFilterModel:
        """设为默认"""
        await self._clear_default()
        return await self.update(id=id, data={"is_default": True})

    async def get_default_crud(self) -> ScreeningFilterModel | None:
        """获取默认筛选"""
        result = await self.list(search={"is_default": (True, "eq")})
        return result[0] if result else None

    async def _clear_default(self) -> None:
        """清除所有默认筛选"""
        from app.core.database import async_db_session
        from sqlalchemy import update

        async with async_db_session() as session:
            stmt = update(ScreeningFilterModel).where(
                ScreeningFilterModel.is_default == True
            ).values(is_default=False)
            await session.execute(stmt)
            await session.commit()

    async def apply_filter_crud(
        self,
        filter_id: int,
        search: dict[str, Any] | None = None,
    ) -> list[dict]:
        """应用筛选条件查询咨询会"""
        from app.plugin.module_consultation.info_collection.crud import InfoCollectionCRUD

        filter_obj = await self.get_by_id_crud(filter_id)
        if not filter_obj:
            return []

        filter_conditions = {
            "province": filter_obj.province,
            "city": filter_obj.city,
            "start_date_begin": filter_obj.start_date_begin,
            "start_date_end": filter_obj.start_date_end,
            "organizer_type": filter_obj.organizer_type,
            "university_count_min": filter_obj.university_count_min,
            "university_count_max": filter_obj.university_count_max,
            "booth_fee_min": filter_obj.booth_fee_min,
            "booth_fee_max": filter_obj.booth_fee_max,
            "estimated_visitors_min": filter_obj.estimated_visitors_min,
            "estimated_visitors_max": filter_obj.estimated_visitors_max,
            "compliance_score_min": filter_obj.compliance_score_min,
            "compliance_score_max": filter_obj.compliance_score_max,
            "compliance_level": filter_obj.compliance_level,
            "source_type": filter_obj.source_type,
            "consultation_status": filter_obj.status,
        }

        if search:
            filter_conditions.update(search)

        order_by_list = []
        if filter_obj.order_by:
            order_by_list.append({filter_obj.order_by: filter_obj.order_direction or "desc"})

        consultation_crud = InfoCollectionCRUD(self.auth)
        result = await consultation_crud.list_crud(search=filter_conditions, order_by=order_by_list)
        return result
