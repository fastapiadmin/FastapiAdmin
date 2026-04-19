"""
表彰评优 - 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    BIGINT,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class EvaluationStatus(str, Enum):
    """评选状态枚举"""
    DRAFT = "draft"         # 草稿
    SUBMITTED = "submitted"   # 已提交
    REVIEWING = "reviewing"   # 审核中
    APPROVED = "approved"     # 已批准
    REJECTED = "rejected"     # 已拒绝


class EvaluationLevel(str, Enum):
    """评选级别枚举"""
    INDIVIDUAL = "individual"   # 个人
    TEAM = "team"             # 团队


class PromotionEvaluationModel(ModelMixin, UserMixin):
    """
    表彰评优表

    存储招生宣传活动中的表彰评优信息
    """

    __tablename__: str = "promotion_evaluation"
    __table_args__: dict[str, str] = {"comment": "表彰评优表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 表彰基本信息
    evaluation_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="表彰单号"
    )

    # 关联活动
    activity_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="关联活动ID"
    )

    activity_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="关联活动名称"
    )

    # 评选类型
    evaluation_level: Mapped[str] = mapped_column(
        String(20),
        default=EvaluationLevel.INDIVIDUAL.value,
        nullable=False,
        comment="评选级别(individual/team)"
    )

    evaluation_type: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        comment="评选类型"
    )

    evaluation_title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="表彰标题"
    )

    # 被表彰对象
    # 个人
    personnel_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="被表彰人员ID"
    )

    personnel_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="被表彰人员姓名"
    )

    # 团队
    team_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="被表彰团队ID"
    )

    team_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="被表彰团队名称"
    )

    # 招生组
    org_team_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="所属招生组ID"
    )

    org_team_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="所属招生组名称"
    )

    # 表彰内容
    award_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="奖项名称"
    )

    award_level: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="奖项级别"
    )

    evaluation_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="评选内容/先进事迹"
    )

    # 佐证材料
    evidence_urls: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="佐证材料URL(JSON数组)"
    )

    evidence_names: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="佐证材料名称(JSON数组)"
    )

    # 评选状态
    evaluation_status: Mapped[str] = mapped_column(
        String(20),
        default=EvaluationStatus.DRAFT.value,
        nullable=False,
        comment="评选状态(draft/submitted/reviewing/approved/rejected)"
    )

    # 提交信息
    submit_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="提交时间"
    )

    submitter_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="提交人ID"
    )

    submitter_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="提交人姓名"
    )

    # 审核信息
    review_comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="审核意见"
    )

    reviewer_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="审核人ID"
    )

    reviewer_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="审核人姓名"
    )

    review_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="审核时间"
    )

    # 批准信息
    approval_comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="批准意见"
    )

    approver_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="批准人ID"
    )

    approver_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="批准人姓名"
    )

    approval_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="批准时间"
    )

    # 奖励信息
    reward_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="奖励类型"
    )

    reward_amount: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="奖励金额"
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