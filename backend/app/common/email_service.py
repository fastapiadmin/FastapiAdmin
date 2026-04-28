"""
通用邮件服务

提供异步 SMTP 邮件发送功能，支持 HTML/纯文本邮件和简单模板渲染
"""

import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

try:
    import aiosmtplib

    HAS_AIOSMTPLIB = True
except ImportError:
    HAS_AIOSMTPLIB = False

from app.config.setting import settings
from app.core.logger import log


class EmailService:
    """
    异步邮件服务

    使用 aiosmtplib 实现异步 SMTP 发送
    """

    @classmethod
    def _validate_email(cls, email: str) -> bool:
        """验证邮箱格式"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @classmethod
    def _render_template(cls, template: str, variables: dict[str, Any]) -> str:
        """
        简单模板渲染

        使用 {{ variable }} 作为占位符

        参数:
            template (str): 模板字符串
            variables (dict): 变量字典

        返回:
            str: 渲染后的字符串
        """
        result = template
        for key, value in variables.items():
            placeholder = f"{{{{ {key} }}}}"
            result = result.replace(placeholder, str(value))
            placeholder2 = f"{{{{{key}}}}}"
            result = result.replace(placeholder2, str(value))
        return result

    @classmethod
    async def send_email(
        cls,
        to_email: str | list[str],
        subject: str,
        body: str | None = None,
        html_body: str | None = None,
        template: str | None = None,
        template_variables: dict[str, Any] | None = None,
        from_email: str | None = None,
        from_name: str | None = None,
    ) -> dict[str, Any]:
        """
        发送邮件

        参数:
            to_email (str | list[str]): 收件人邮箱，支持单个或多个
            subject (str): 邮件主题
            body (str | None): 纯文本邮件内容
            html_body (str | None): HTML 邮件内容
            template (str | None): 模板字符串（与 template_variables 配合使用）
            template_variables (dict | None): 模板变量
            from_email (str | None): 发件人邮箱，默认使用配置
            from_name (str | None): 发件人名称，默认使用配置

        返回:
            dict: 发送结果 {"success": bool, "message": str}
        """
        if not HAS_AIOSMTPLIB:
            log.warning("aiosmtplib 未安装，邮件发送功能不可用")
            return {"success": False, "message": "邮件服务未配置"}

        # 处理收件人
        if isinstance(to_email, str):
            to_list = [to_email]
        else:
            to_list = to_email

        # 验证收件人邮箱
        for email in to_list:
            if not cls._validate_email(email):
                log.error(f"邮箱格式无效: {email}")
                return {"success": False, "message": f"邮箱格式无效: {email}"}

        # 渲染模板
        if template and template_variables:
            body = cls._render_template(template, template_variables)

        if not body and not html_body:
            return {"success": False, "message": "邮件内容不能为空"}

        # 构建邮件
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{from_name or settings.SMTP_FROM_NAME} <{from_email or settings.SMTP_FROM}>"
        msg["To"] = ", ".join(to_list) if len(to_list) > 1 else to_list[0]

        # 添加纯文本内容
        if body:
            msg.attach(MIMEText(body, "plain", "utf-8"))

        # 添加 HTML 内容
        if html_body:
            msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            # 发送邮件
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=settings.SMTP_TLS,
            )
            log.info(f"邮件发送成功: {subject} -> {to_list}")
            return {"success": True, "message": "发送成功"}

        except Exception as e:
            log.error(f"邮件发送失败: {e}")
            return {"success": False, "message": f"发送失败: {str(e)}"}

    @classmethod
    async def sendRegistrationReceipt(
        cls,
        to_email: str,
        university_name: str,
        consultation_title: str,
        consultation_date: str,
        consultation_location: str,
        booth_number: str | None = None,
        contact_person: str | None = None,
    ) -> dict[str, Any]:
        """
        发送报名回执邮件

        参数:
            to_email (str): 收件人邮箱
            university_name (str): 高校名称
            consultation_title (str): 咨询会标题
            consultation_date (str): 咨询会日期
            consultation_location (str): 咨询会地点
            booth_number (str | None): 展位号
            contact_person (str | None): 联系人

        返回:
            dict: 发送结果
        """
        from app.api.v1.module_consultation.registration.email_template import (
            RegistrationEmailTemplate,
        )

        template = RegistrationEmailTemplate.get_default_template()
        variables = {
            "university_name": university_name,
            "consultation_title": consultation_title,
            "consultation_date": consultation_date,
            "consultation_location": consultation_location,
            "booth_number": booth_number or "待分配",
            "contact_person": contact_person or "",
            "contact_person_greeting": f"尊敬的 {contact_person or university_name} 负责人"
            if contact_person
            else f"尊敬的 {university_name} 负责人",
        }

        subject = f"【参会确认】{consultation_title} - {university_name}"

        return await cls.send_email(
            to_email=to_email,
            subject=subject,
            template=template,
            template_variables=variables,
        )
