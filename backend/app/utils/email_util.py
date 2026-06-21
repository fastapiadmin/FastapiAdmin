"""
email_util.py — 邮件发送工具

职责：
- 渲染 Jinja2 模板（文件 & 内联字符串）
- 通过 fastapi-mail 发送邮件

使用方：EmailService.send_email_service()
"""

from pathlib import Path
from typing import Any

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader, StrictUndefined

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"
_file_env: Environment | None = None


def _get_file_env() -> Environment:
    """获取文件模板 Jinja2 环境（懒加载）。"""
    global _file_env
    if _file_env is None:
        _file_env = Environment(
            loader=FileSystemLoader(str(_TEMPLATES_DIR)),
            undefined=StrictUndefined,
            autoescape=True,
        )
    return _file_env


def render_template_file(file_path: str, variables: dict[str, Any]) -> str:
    """
    从 templates/ 目录加载 Jinja2 文件模板并渲染。

    参数：
    - file_path: 相对于 templates/ 的模板路径，如 "emails/welcome.html"
    - variables: 变量字典

    返回：渲染后的字符串
    """
    env = _get_file_env()
    tmpl = env.get_template(file_path)
    return tmpl.render(**variables)


def render_template(template_str: str, variables: dict[str, Any]) -> str:
    """
    使用 Jinja2 渲染邮件模板。

    参数：
    - template_str: Jinja2 模板字符串
    - variables: 变量字典

    返回：渲染后的字符串

    异常：TemplateError — 模板语法错误或变量缺失
    """
    env = Environment(undefined=StrictUndefined, autoescape=True)
    tmpl = env.from_string(template_str)
    return tmpl.render(**variables)


async def send_email(
    *,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    use_tls: bool,
    from_name: str,
    to_email: str,
    to_name: str | None,
    subject: str,
    body_html: str,
    body_text: str | None = None,
    timeout: int = 30,
) -> None:
    """
    异步发送邮件（通过 fastapi-mail）。

    参数均为关键字参数。

    异常：
    - SMTPException — SMTP 协议错误
    - TimeoutError — 连接/发送超时
    """
    # 构建 fastapi-mail 连接配置
    # 端口 465 = 隐式 SSL，端口 587 = STARTTLS
    is_ssl = smtp_port == 465

    conf = ConnectionConfig(
        MAIL_USERNAME=smtp_user,
        MAIL_PASSWORD=smtp_password,
        MAIL_FROM=smtp_user,
        MAIL_FROM_NAME=from_name,
        MAIL_SERVER=smtp_host,
        MAIL_PORT=smtp_port,
        MAIL_STARTTLS=not is_ssl and use_tls,
        MAIL_SSL_TLS=is_ssl,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=False,
        MAIL_TIMEOUT=timeout,
    )

    # 收件人格式：支持 "姓名 <邮箱>"（若有 to_name）
    recipient = f"{to_name} <{to_email}>" if to_name else to_email

    # 构建邮件消息
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body_html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
