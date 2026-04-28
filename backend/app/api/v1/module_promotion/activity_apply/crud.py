"""
活动申请审批 - 数据访问层
"""

from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import ActivityApplyModel
from .schema import ActivityApplyCreateSchema, ActivityApplyOutSchema, ActivityApplyUpdateSchema


class ActivityApplyCRUD(
    CRUDBase[ActivityApplyModel, ActivityApplyCreateSchema, ActivityApplyUpdateSchema]
):
    """
    活动申请数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=ActivityApplyModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> ActivityApplyModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[ActivityApplyModel]:
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
            out_schema=ActivityApplyOutSchema,
        )

    async def create_crud(self, data: dict) -> ActivityApplyModel:
        """创建记录"""
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> ActivityApplyModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def get_by_activity_code_crud(self, activity_code: str) -> ActivityApplyModel | None:
        """根据编码获取活动申请"""
        result = await self.get(row_key="activity_code", row_value=activity_code)
        return result

    async def get_by_team_id_crud(self, team_id: int) -> list[ActivityApplyModel]:
        """获取招生组下所有活动申请"""
        search = {"team_id": ("eq", team_id)}
        return await self.list(search=search)

    async def get_pending_approvals_crud(self) -> list[ActivityApplyModel]:
        """获取待审批的活动申请"""
        search = {"approval_status": ("eq", "pending")}
        return await self.list(search=search)
