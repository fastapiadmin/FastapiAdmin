"""
审批记录 - 数据模型
"""

from datetime import datetime

from sqlalchemy import BIGINT, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class PromotionApprovalRecordModel(ModelMixin, UserMixin):
    """
    审批记录表

    记录活动申请每个审批步骤的详细信息，用于审计追溯
    """

    __tablename__: str = "promotion_approval_record"
    __table_args__: dict[str, str] = {"comment": "审批记录表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    activity_apply_id: Mapped[int] = mapped_column(
        BIGINT, nullable=False, index=True, comment="活动申请ID"
    )

    approval_level: Mapped[int] = mapped_column(Integer, nullable=False, comment="审批级别")

    approval_action: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="审批动作(approved/rejected)"
    )

    approver_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="审批人ID")

    approver_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="审批人姓名"
    )

    approval_comment: Mapped[str | None] = mapped_column(Text, nullable=True, comment="审批意见")

    approval_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="审批时间"
    )
