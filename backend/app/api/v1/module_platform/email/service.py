from datetime import datetime

from app.core.base_schema import AuthSchema
from app.core.dependencies import require_superadmin
from app.core.exceptions import CustomException
from app.utils.email_util import render_template, send_email

from .crud import EmailConfigCRUD, EmailLogCRUD, EmailTemplateCRUD
from .schema import (
    EmailConfigCreateSchema,
    EmailConfigOutSchema,
    EmailConfigQueryParam,
    EmailConfigUpdateSchema,
    EmailLogOutSchema,
    EmailLogQueryParam,
    EmailSendSchema,
    EmailTemplateCreateSchema,
    EmailTemplateOutSchema,
    EmailTemplateQueryParam,
    EmailTemplateUpdateSchema,
    EmailTestSchema,
)


class EmailConfigService:
    """SMTP 配置管理（仅超级管理员可操作）"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    @require_superadmin
    async def page(
        self,
        page_no: int,
        page_size: int,
        search: EmailConfigQueryParam | None = None,
        order_by: list | None = None,
    ) -> dict:
        return await EmailConfigCRUD(self.auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=vars(search) if search else None,
            out_schema=EmailConfigOutSchema,
        )

    @require_superadmin
    async def detail(self, id: int) -> EmailConfigOutSchema:
        return await EmailConfigCRUD(self.auth).get_or_404(id=id, out_schema=EmailConfigOutSchema, msg="SMTP 配置不存在")

    async def create(self, data: EmailConfigCreateSchema) -> EmailConfigOutSchema:
        crud = EmailConfigCRUD(self.auth)
        if data.is_default:
            await crud.clear_default()
        obj = await crud.create(data=data)
        return EmailConfigOutSchema.model_validate(obj)

    async def update(self, id: int, data: EmailConfigUpdateSchema) -> EmailConfigOutSchema:
        crud = EmailConfigCRUD(self.auth)
        _ = await crud.get_or_404(id=id, msg="SMTP 配置不存在")
        if data.is_default is True:
            await crud.clear_default()
        updated = await crud.update(id=id, data=data)
        return EmailConfigOutSchema.model_validate(updated)

    async def delete(self, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除对象不能为空")
        crud = EmailConfigCRUD(self.auth)
        configs = await crud.get_list(search={"id": ("in", ids)})
        for obj in configs:
            if obj.is_default:
                raise CustomException(msg=f"配置「{obj.name}」是默认配置，请先将其他配置设为默认后再删除")
        await crud.delete(ids=ids)

    @require_superadmin
    async def test(self, data: EmailTestSchema) -> dict:
        config = await EmailConfigCRUD(self.auth).get(id=data.config_id)
        if not config:
            raise CustomException(msg="SMTP 配置不存在")

        subject = ("【FastapiAdmin】SMTP 连接测试")
        body_html = ("<p>这是一封测试邮件，SMTP 配置「{name}」连接成功！</p>"
                     "<p>发送时间：{time}</p>").format(name=config.name, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        try:
            await send_email(
                smtp_host=config.smtp_host,
                smtp_port=config.smtp_port,
                smtp_user=config.smtp_user,
                smtp_password=config.smtp_password,
                use_tls=config.use_tls,
                from_name=config.from_name,
                to_email=data.to_email,
                to_name=None,
                subject=subject,
                body_html=body_html,
                timeout=config.timeout,
            )
        except Exception as e:
            raise CustomException(msg=f"SMTP 连接测试失败：{e!s}") from e

        return {"message": f"测试邮件已发送至 {data.to_email}"}


class EmailTemplateService:
    """邮件模板管理（仅超级管理员可操作）"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    @require_superadmin
    async def page(
        self,
        page_no: int,
        page_size: int,
        search: EmailTemplateQueryParam | None = None,
        order_by: list | None = None,
    ) -> dict:
        return await EmailTemplateCRUD(self.auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"id": "asc"}],
            search=vars(search) if search else None,
            out_schema=EmailTemplateOutSchema,
        )

    @require_superadmin
    async def detail(self, id: int) -> EmailTemplateOutSchema:
        return await EmailTemplateCRUD(self.auth).get_or_404(id=id, out_schema=EmailTemplateOutSchema, msg="邮件模板不存在")

    @require_superadmin
    async def create(self, data: EmailTemplateCreateSchema) -> EmailTemplateOutSchema:
        existing = await EmailTemplateCRUD(self.auth).get_by_code(template_code=data.template_code)
        if existing:
            raise CustomException(msg=f"模板编码「{data.template_code}」已存在")

        obj = await EmailTemplateCRUD(self.auth).create(data=data)
        return EmailTemplateOutSchema.model_validate(obj)

    @require_superadmin
    async def update(self, id: int, data: EmailTemplateUpdateSchema) -> EmailTemplateOutSchema:
        _ = await EmailTemplateCRUD(self.auth).get_or_404(id=id, msg="邮件模板不存在")
        updated = await EmailTemplateCRUD(self.auth).update(id=id, data=data)
        return EmailTemplateOutSchema.model_validate(updated)

    @require_superadmin
    async def delete(self, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除对象不能为空")
        await EmailTemplateCRUD(self.auth).delete(ids=ids)


class EmailSendService:
    """邮件发送服务 — 供其他模块调用"""
    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def send_by_template(
        self,
        *,
        to_email: str,
        template_code: str,
        variables: dict,
        biz_type: str = "other",
        to_name: str | None = None,
        tenant_id: int | None = None,
        config_id: int | None = None,
    ) -> bool:
        template = await EmailTemplateCRUD(self.auth).get_active_by_code(template_code)

        if not template:
            await EmailLogCRUD.create_log(
                to_email=to_email,
                subject=f"[{template_code}]",
                biz_type=biz_type,
                to_name=to_name,
                template_code=template_code,
                tenant_id=tenant_id,
                status=2,
                error_msg=f"模板「{template_code}」不存在或已禁用",
            )
            return False

        try:
            rendered_subject = render_template(template.subject, variables)
            rendered_html = render_template(template.body_html, variables)
            rendered_text = render_template(template.body_text, variables) if template.body_text else None
        except Exception as e:
            await EmailLogCRUD.create_log(
                to_email=to_email,
                subject=template.subject,
                biz_type=biz_type,
                to_name=to_name,
                template_code=template_code,
                tenant_id=tenant_id,
                status=2,
                error_msg=f"模板渲染失败：{e!s}",
            )
            return False

        if config_id:
            config = await EmailConfigCRUD(self.auth).get_active_by_id(config_id)
        else:
            config = await EmailConfigCRUD(self.auth).get_active_default()

        if not config:
            await EmailLogCRUD.create_log(
                to_email=to_email,
                subject=rendered_subject,
                biz_type=biz_type,
                to_name=to_name,
                template_code=template_code,
                tenant_id=tenant_id,
                status=2,
                error_msg="无可用的 SMTP 配置，邮件未发送（已降级为站内信）",
            )
            return False

        try:
            await send_email(
                smtp_host=config.smtp_host,
                smtp_port=config.smtp_port,
                smtp_user=config.smtp_user,
                smtp_password=config.smtp_password,
                use_tls=config.use_tls,
                from_name=config.from_name,
                to_email=to_email,
                to_name=to_name,
                subject=rendered_subject,
                body_html=rendered_html,
                body_text=rendered_text,
                timeout=config.timeout,
            )
        except Exception as e:
            await EmailLogCRUD.create_log(
                to_email=to_email,
                subject=rendered_subject,
                biz_type=biz_type,
                to_name=to_name,
                template_code=template_code,
                config_id=config.id,
                tenant_id=tenant_id,
                status=2,
                error_msg=f"SMTP 发送失败：{e!s}",
            )
            return False

        await EmailLogCRUD.create_log(
            config_id=config.id,
            template_code=template_code,
            to_email=to_email,
            to_name=to_name,
            subject=rendered_subject,
            biz_type=biz_type,
            status=1,
            tenant_id=tenant_id,
        )

        return True

    async def manual_send(self, data: EmailSendSchema) -> dict:
        success = await self.send_by_template(
            to_email=data.to_email,
            template_code=data.template_code,
            variables=data.variables,
            biz_type=data.biz_type,
            to_name=data.to_name,
            config_id=data.config_id,
        )
        if not success:
            raise CustomException(msg="邮件发送失败，请查看邮件日志获取详情")
        return {"message": f"邮件已发送至 {data.to_email}"}


class EmailLogService:
    """邮件日志查询"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def page(
        self,
        page_no: int,
        page_size: int,
        search: EmailLogQueryParam | None = None,
        order_by: list | None = None,
    ) -> dict:
        return await EmailLogCRUD(self.auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"created_time": "desc"}],
            search=vars(search) if search else None,
            out_schema=EmailLogOutSchema,
        )
