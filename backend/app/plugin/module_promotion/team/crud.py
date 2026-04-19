"""
组织架构管理 - 数据访问层
"""
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import PromotionTeamModel
from .schema import TeamCreateSchema, TeamOutSchema, TeamUpdateSchema


class TeamCRUD(CRUDBase[PromotionTeamModel, TeamCreateSchema, TeamUpdateSchema]):
    """
    招生组数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=PromotionTeamModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> PromotionTeamModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[PromotionTeamModel]:
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
            out_schema=TeamOutSchema,
        )

    async def create_crud(self, data: dict) -> PromotionTeamModel:
        """创建记录"""
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> PromotionTeamModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def get_children_crud(self, parent_id: int) -> list[PromotionTeamModel]:
        """获取下级招生组"""
        search = {"parent_id": ("eq", parent_id)}
        return await self.list(search=search)

    async def get_root_teams_crud(self) -> list[PromotionTeamModel]:
        """获取顶级招生组"""
        search = {"parent_id": ("is_null", None)}
        return await self.list(search=search)

    async def get_by_team_code_crud(self, team_code: str) -> PromotionTeamModel | None:
        """根据编码获取招生组"""
        result = await self.get(row_key="team_code", row_value=team_code)
        return result