"""
人员管理 - 数据访问层
"""

from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import PromotionPersonnelModel
from .schema import PersonnelCreateSchema, PersonnelOutSchema, PersonnelUpdateSchema


class PersonnelCRUD(
    CRUDBase[PromotionPersonnelModel, PersonnelCreateSchema, PersonnelUpdateSchema]
):
    """
    招生人员数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=PromotionPersonnelModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> PromotionPersonnelModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[PromotionPersonnelModel]:
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
            out_schema=PersonnelOutSchema,
        )

    async def create_crud(self, data: dict) -> PromotionPersonnelModel:
        """创建记录"""
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> PromotionPersonnelModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def get_by_personnel_code_crud(
        self, personnel_code: str
    ) -> PromotionPersonnelModel | None:
        """根据编号获取招生人员"""
        result = await self.get(row_key="personnel_code", row_value=personnel_code)
        return result

    async def get_by_user_id_crud(self, user_id: int) -> PromotionPersonnelModel | None:
        """根据用户ID获取招生人员"""
        result = await self.get(row_key="user_id", row_value=user_id)
        return result

    async def get_by_team_id_crud(self, team_id: int) -> list[PromotionPersonnelModel]:
        """获取招生组下所有人员"""
        search = {"team_id": ("eq", team_id)}
        return await self.list(search=search)

    async def get_active_personnel_crud(self) -> list[PromotionPersonnelModel]:
        """获取所有在岗人员"""
        search = {"status": ("eq", "active")}
        return await self.list(search=search)
