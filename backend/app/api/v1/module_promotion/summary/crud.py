"""
总结上传 - 数据访问层
"""
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import PromotionSummaryModel
from .schema import SummaryCreateSchema, SummaryOutSchema, SummaryUpdateSchema


class SummaryCRUD(CRUDBase[PromotionSummaryModel, SummaryCreateSchema, SummaryUpdateSchema]):
    """
    总结上传数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=PromotionSummaryModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> PromotionSummaryModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[PromotionSummaryModel]:
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
            out_schema=SummaryOutSchema,
        )

    async def create_crud(self, data: dict) -> PromotionSummaryModel:
        """创建记录"""
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> PromotionSummaryModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)
