"""
合规诊断 - 数据访问层
"""
from datetime import datetime
from typing import Any

from sqlalchemy import update

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase
from app.core.database import async_db_session

from .model import ComplianceDiagnosisModel, ComplianceRuleModel
from .schema import (
    ComplianceDiagnosisCreateSchema,
    ComplianceDiagnosisOutSchema,
    ComplianceDiagnosisUpdateSchema,
    ComplianceRuleCreateSchema,
    ComplianceRuleOutSchema,
    ComplianceRuleUpdateSchema,
)


class ComplianceDiagnosisCRUD(CRUDBase[ComplianceDiagnosisModel, ComplianceDiagnosisCreateSchema, ComplianceDiagnosisUpdateSchema]):
    """
    合规诊断数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=ComplianceDiagnosisModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> ComplianceDiagnosisModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[ComplianceDiagnosisModel]:
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
            out_schema=ComplianceDiagnosisOutSchema,
        )

    async def create_crud(self, data: dict) -> ComplianceDiagnosisModel:
        """创建记录"""
        data["diagnosis_time"] = datetime.now()
        consultation_id = data.get("consultation_id")

        if consultation_id:
            await self._mark_old_diagnosis_not_latest(consultation_id)

        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> ComplianceDiagnosisModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def get_latest_by_consultation_crud(
        self, consultation_id: int
    ) -> ComplianceDiagnosisModel | None:
        """获取某咨询会的最新诊断"""
        result = await self.list(
            search={"consultation_id": (consultation_id, "eq"), "is_latest": (True, "eq")}
        )
        return result[0] if result else None

    async def _mark_old_diagnosis_not_latest(self, consultation_id: int) -> None:
        """标记旧诊断为非最新"""
        async with async_db_session() as session:
            stmt = (
                update(ComplianceDiagnosisModel)
                .where(
                    ComplianceDiagnosisModel.consultation_id == consultation_id,
                    ComplianceDiagnosisModel.is_latest.is_(True),
                )
                .values(is_latest=False)
            )
            await session.execute(stmt)
            await session.commit()


class ComplianceRuleCRUD(CRUDBase[ComplianceRuleModel, ComplianceRuleCreateSchema, ComplianceRuleUpdateSchema]):
    """
    合规规则数据访问层
    """

    def __init__(self, auth: AuthSchema):
        super().__init__(model=ComplianceRuleModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> ComplianceRuleModel | None:
        """根据ID获取详情"""
        return await self.get(id=id)

    async def list_crud(
        self,
        search: dict[str, Any] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[ComplianceRuleModel]:
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
            out_schema=ComplianceRuleOutSchema,
        )

    async def create_crud(self, data: dict) -> ComplianceRuleModel:
        """创建记录"""
        return await self.create(data=data)

    async def update_crud(self, id: int, data: dict) -> ComplianceRuleModel:
        """更新记录"""
        return await self.update(id=id, data=data)

    async def delete_crud(self, id: int) -> None:
        """删除记录"""
        await self.delete(ids=[id])

    async def batch_delete_crud(self, ids: list[int]) -> None:
        """批量删除"""
        await self.delete(ids=ids)

    async def get_active_rules_crud(self) -> list[ComplianceRuleModel]:
        """获取所有启用的规则"""
        return await self.list(search={"is_active": (True, "eq")}, order_by=[{"order": "asc"}])

    async def toggle_status_crud(self, id: int) -> ComplianceRuleModel:
        """切换规则启用状态"""
        obj = await self.get_by_id_crud(id)
        if obj:
            return await self.update(id=id, data={"is_active": not obj.is_active})
        return None
