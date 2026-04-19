"""
费用报销 - 数据模型
"""
from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BIGINT, Date, DateTime, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ExpenseStatus(str, Enum):
    """费用状态枚举"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REIMBURSED = "reimbursed"


class PromotionExpenseModel(ModelMixin, UserMixin):
    """
    费用报销表

    存储招生宣传活动中的费用报销信息
    """

    __tablename__: str = "promotion_expense"
    __table_args__: dict[str, str] = {"comment": "费用报销表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    expense_no: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="报销单号"
    )

    applicant_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="申请人ID"
    )

    team_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="招生组ID"
    )

    activity_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="活动ID"
    )

    expense_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="费用类型"
    )

    amount: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
        comment="金额"
    )

    expense_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="费用日期"
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="描述"
    )

    attachments: Mapped[Optional[JSON]] = mapped_column(
        JSON,
        nullable=True,
        comment="附件"
    )

    approval_status: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="审批状态"
    )

    approval_comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="审批意见"
    )

    approval_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="审批时间"
    )

    approval_by: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="审批人ID"
    )
