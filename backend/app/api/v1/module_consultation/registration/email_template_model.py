"""
报名回执邮件模板 - 数据模型
"""

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class RegistrationEmailTemplateModel(ModelMixin, UserMixin):
    """
    报名回执邮件模板表

    存储可编辑的报名回执邮件模板
    """

    __tablename__: str = "consultation_registration_email_template"
    __table_args__: dict[str, str] = {"comment": "报名回执邮件模板表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    template_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="模板名称")

    template_content: Mapped[str] = mapped_column(
        Text, nullable=False, comment="模板内容(支持变量)"
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否默认模板"
    )
