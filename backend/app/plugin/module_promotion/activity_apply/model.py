"""
活动申请审批 - 数据模型
"""
from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    BIGINT,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ApprovalStatus(str, Enum):
    """审批状态枚举"""
    PENDING = "pending"       # 待审批
    APPROVED = "approved"     # 已批准
    REJECTED = "rejected"     # 已拒绝
    CANCELLED = "cancelled"   # 已取消


class ActivityType(str, Enum):
    """活动类型枚举"""
    CAMPUS_VISIT = "campus_visit"     # 校园走访
    SCHOOL_LECTURE = "school_lecture" # 学校讲座
    COMMUNITY_ACTIVITY = "community_activity"  # 社区活动
    ONLINE_PROMOTION = "online_promotion"      # 在线宣传
    OTHER = "other"                 # 其他


class ActivityApplyModel(ModelMixin, UserMixin):
    """
    活动申请表

    存储招生宣传活动中的活动申请信息
    """

    __tablename__: str = "promotion_activity_apply"
    __table_args__: dict[str, str] = {"comment": "活动申请表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 活动基本信息
    activity_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="活动名称"
    )

    activity_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
        comment="活动编码"
    )

    activity_type: Mapped[str] = mapped_column(
        String(50),
        default=ActivityType.OTHER.value,
        nullable=False,
        comment="活动类型(campus_visit/school_lecture/community_activity/online_promotion/other)"
    )

    # 招生组关联
    team_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="招生组ID"
    )

    team_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="招生组名称"
    )

    # 申请人员
    applicant_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="申请人ID"
    )

    applicant_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="申请人姓名"
    )

    # 活动时间和地点
    activity_start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="活动开始日期"
    )

    activity_end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="活动结束日期"
    )

    province: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="省份"
    )

    city: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="城市"
    )

    district: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="区县"
    )

    address: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="详细地址"
    )

    # 活动目标学校
    target_school_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="目标学校ID"
    )

    target_school_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="目标学校名称"
    )

    # 活动内容
    activity_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="活动内容"
    )

    expected_participants: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="预计参与人数"
    )

    # 预算信息
    budget: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="预算金额"
    )

    budget_usage: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="预算用途"
    )

    # 物料需求
    materials_needed: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="所需物料"
    )

    # 人员需求
    personnel_needed: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="所需人员数"
    )

    # 审批信息
    approval_status: Mapped[str] = mapped_column(
        String(20),
        default=ApprovalStatus.PENDING.value,
        nullable=False,
        comment="审批状态(pending/approved/rejected/cancelled)"
    )

    approval_comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="审批意见"
    )

    approval_by: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="审批人ID"
    )

    approval_by_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="审批人姓名"
    )

    approval_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="审批时间"
    )

    # 审批流程信息
    approval_level: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="审批级别"
    )

    current_approval_level: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="当前审批级别"
    )

    # 备注
    remark: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="备注"
    )

    # 排序
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="显示排序"
    )