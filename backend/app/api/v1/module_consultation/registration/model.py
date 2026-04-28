"""
报名管理 - 数据模型
"""

from datetime import datetime

from sqlalchemy import (
    BIGINT,
    Boolean,
    DateTime,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class RegistrationModel(ModelMixin, UserMixin):
    """
    咨询会报名表

    存储高校报名参加咨询会的记录
    """

    __tablename__: str = "consultation_registration"
    __table_args__: dict[str, str] = {"comment": "咨询会报名表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    consultation_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="咨询会ID")
    university_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="高校ID")
    university_name: Mapped[str | None] = mapped_column(String(200), comment="高校名称")

    contact_person: Mapped[str | None] = mapped_column(String(100), comment="联系人")
    contact_phone: Mapped[str | None] = mapped_column(String(20), comment="联系电话")
    contact_email: Mapped[str | None] = mapped_column(String(100), comment="联系邮箱")

    booth_number: Mapped[str | None] = mapped_column(String(50), comment="展位号")
    booth_size: Mapped[str | None] = mapped_column(String(50), comment="展位大小")

    registration_status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
        comment="报名状态(pending/approved/rejected/cancelled)",
    )
    registration_time: Mapped[datetime | None] = mapped_column(DateTime, comment="报名时间")
    approval_time: Mapped[datetime | None] = mapped_column(DateTime, comment="审核时间")
    approval_by: Mapped[int | None] = mapped_column(BIGINT, comment="审核人ID")
    approval_comment: Mapped[str | None] = mapped_column(Text, comment="审核意见")

    # 一键报名相关
    registration_email: Mapped[str | None] = mapped_column(String(100), comment="报名接收邮箱")
    is_registered: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否已完成一键报名"
    )
    register_time: Mapped[datetime | None] = mapped_column(DateTime, comment="一键报名时间")
