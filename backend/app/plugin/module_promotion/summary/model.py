"""
总结上传 - 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    BIGINT,
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SummaryStatus(str, Enum):
    """总结状态枚举"""
    DRAFT = "draft"         # 草稿
    SUBMITTED = "submitted"   # 已提交
    APPROVED = "approved"     # 已审批
    REJECTED = "rejected"     # 已拒绝


class PromotionSummaryModel(ModelMixin, UserMixin):
    """
    总结上传表

    存储招生宣传活动中的活动总结信息
    """

    __tablename__: str = "promotion_summary"
    __table_args__: dict[str, str] = {"comment": "总结上传表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 总结基本信息
    summary_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="总结单号"
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

    # 关联行程
    trip_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="关联行程ID"
    )

    trip_no: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="行程单号"
    )

    # 招生人员和组
    personnel_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="招生人员ID"
    )

    personnel_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="招生人员姓名"
    )

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

    # 总结内容
    summary_title: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="总结标题"
    )

    summary_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="总结内容"
    )

    # 附件
    attachment_urls: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="附件URL(JSON数组)"
    )

    attachment_names: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="附件名称(JSON数组)"
    )

    # 活动数据统计
    visitor_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="来访人数"
    )

    consultation_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="咨询人数"
    )

    registration_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="报名人数"
    )

    # 总结状态
    summary_status: Mapped[str] = mapped_column(
        String(20),
        default=SummaryStatus.DRAFT.value,
        nullable=False,
        comment="总结状态(draft/submitted/approved/rejected)"
    )

    # 提交时间
    submit_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="提交时间"
    )

    # 审批信息
    approval_comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="审批意见"
    )

    approver_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="审批人ID"
    )

    approver_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="审批人姓名"
    )

    approval_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="审批时间"
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