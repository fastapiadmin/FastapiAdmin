"""
活动申请审批 - 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BIGINT, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ApprovalStatus(str, Enum):
    """审批状态枚举"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class ActivityApplyModel(ModelMixin, UserMixin):
    """
    活动申请表

    存储招生宣传活动中的活动申请信息
    """

    __tablename__: str = "promotion_activity_apply"
    __table_args__: dict[str, str] = {"comment": "活动申请表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    activity_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="活动名称"
    )

    activity_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="活动类型"
    )

    team_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="招生组ID"
    )

    applicant_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="申请人ID"
    )

    target_school_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="目标学校ID"
    )

    plan_start_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="计划开始时间"
    )

    plan_end_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="计划结束时间"
    )

    plan_location: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="计划地点"
    )

    plan_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="计划内容"
    )

    expected_people: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="预期人数"
    )

    budget: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
        comment="预算"
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
