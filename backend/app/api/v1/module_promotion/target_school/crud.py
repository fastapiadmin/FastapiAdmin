"""
目标学校管理 - 数据访问层
"""
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import PromotionTargetSchoolModel
from .schema import TargetSchoolCreateSchema, TargetSchoolOutSchema, TargetSchoolUpdateSchema


class TargetSchoolCRUD(CRUDBase[PromotionTargetSchoolModel, TargetSchoolCreateSchema, TargetSchoolUpdateSchema]):
    """
    目标学校数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=PromotionTargetSchoolModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> PromotionTargetSchoolModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[PromotionTargetSchoolModel]:
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
            out_schema=TargetSchoolOutSchema,
        )

    async def create_crud(self, data: dict) -> PromotionTargetSchoolModel:
        """创建记录"""
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> PromotionTargetSchoolModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def get_by_school_code_crud(self, school_code: str) -> PromotionTargetSchoolModel | None:
        """根据代码获取目标学校"""
        result = await self.get(row_key="school_code", row_value=school_code)
        return result

    async def get_by_team_id_crud(self, team_id: int) -> list[PromotionTargetSchoolModel]:
        """获取招生组下所有目标学校"""
        search = {"team_id": ("eq", team_id)}
        return await self.list(search=search)

    async def get_by_personnel_id_crud(self, personnel_id: int) -> list[PromotionTargetSchoolModel]:
        """获取负责人下所有目标学校"""
        search = {"personnel_id": ("eq", personnel_id)}
        return await self.list(search=search)
