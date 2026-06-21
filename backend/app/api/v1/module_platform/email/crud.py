from typing import Any

from app.core.base_crud import CRUDBase
from app.core.base_schema import AuthSchema

from .model import EmailConfigModel, EmailLogModel, EmailTemplateModel
from .schema import EmailConfigCreateSchema, EmailConfigUpdateSchema, EmailTemplateCreateSchema, EmailTemplateUpdateSchema


class EmailConfigCRUD(CRUDBase[EmailConfigModel, EmailConfigCreateSchema, EmailConfigUpdateSchema]):
    """SMTP 配置 CRUD"""

    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=EmailConfigModel, auth=auth)

    async def get_default(self) -> EmailConfigModel | None:
        return await self.get(is_default=True)

    async def clear_default(self) -> None:
        """清除所有配置的 is_default 标记（不管理事务，由调用方控制）"""
        from sqlalchemy import update as sa_update

        await self.db.execute(sa_update(EmailConfigModel).where(EmailConfigModel.is_default.is_(True)).values(is_default=False))

    async def get_active_by_id(self, config_id: int) -> EmailConfigModel | None:
        return await self.get(id=config_id, status=0)

    async def get_active_default(self) -> EmailConfigModel | None:
        return await self.get(is_default=True, status=0)


class EmailTemplateCRUD(CRUDBase[EmailTemplateModel, EmailTemplateCreateSchema, EmailTemplateUpdateSchema]):
    """邮件模板 CRUD"""

    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=EmailTemplateModel, auth=auth)

    async def get_by_code(self, template_code: str) -> EmailTemplateModel | None:
        return await self.get(template_code=template_code)

    async def get_active_by_code(self, template_code: str) -> EmailTemplateModel | None:
        return await self.get(template_code=template_code, status=0)


class EmailLogCRUD(CRUDBase[EmailLogModel, Any, Any]):
    """邮件日志 CRUD"""

    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=EmailLogModel, auth=auth)

    @staticmethod
    async def create_log(
        to_email: str,
        subject: str,
        biz_type: str = "other",
        to_name: str | None = None,
        template_code: str | None = None,
        config_id: int | None = None,
        tenant_id: int | None = None,
        status: int = 0,
        error_msg: str | None = None,
    ) -> EmailLogModel:
        """写入邮件日志（独立事务，日志失败不回滚调用方业务）"""
        from datetime import datetime

        from app.core.database import async_db_session

        async with async_db_session() as session:
            async with session.begin():
                log_obj = EmailLogModel(
                    to_email=to_email,
                    to_name=to_name,
                    subject=subject,
                    biz_type=biz_type,
                    template_code=template_code,
                    config_id=config_id,
                    tenant_id=tenant_id,
                    status=status,
                    error_msg=error_msg,
                    sent_time=datetime.now() if status == 1 else None,
                )
                session.add(log_obj)
                await session.flush()
                await session.refresh(log_obj)
                return log_obj
