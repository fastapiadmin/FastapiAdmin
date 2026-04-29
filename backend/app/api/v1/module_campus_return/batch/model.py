"""
批次管理 - 数据模型

功能：按年度/学期设置宣讲批次，配置时间和规则
"""

from datetime import date
from enum import Enum

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class BatchStatus(str, Enum):
    """批次状态枚举"""

    DRAFT = "draft"  # 草稿
    RECRUITING = "recruiting"  # 招募中
    REVIEWING = "reviewing"  # 审核中
    CONFIRMED = "confirmed"  # 已确认
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


class ReviewType(str, Enum):
    """审核方式枚举"""

    MANUAL = "manual"  # 手动审核
    AUTO = "auto"  # 自动审核
    MIXED = "mixed"  # 混合审核


class CampusReturnBatchModel(ModelMixin, UserMixin):
    """
    返校宣讲批次表

    按年度/学期设置宣讲批次，配置时间和规则
    """

    __tablename__: str = "campus_return_batch"
    __table_args__: dict[str, str] = {"comment": "返校宣讲批次表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 批次基本信息
    batch_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="批次名称")
    year: Mapped[int] = mapped_column(Integer, nullable=False, comment="年度")
    semester: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="学期(上学期/下学期/暑假/寒假)"
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="批次描述")

    # 时间配置
    recruitment_start: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="招募开始日期"
    )
    recruitment_end: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="招募结束日期"
    )
    activity_start: Mapped[date | None] = mapped_column(Date, nullable=True, comment="活动开始日期")
    activity_end: Mapped[date | None] = mapped_column(Date, nullable=True, comment="活动结束日期")
    registration_deadline: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="报名截止日期"
    )

    # 规则配置
    status: Mapped[str] = mapped_column(
        String(20), default=BatchStatus.DRAFT.value, comment="批次状态"
    )
    review_type: Mapped[str] = mapped_column(
        String(20), default=ReviewType.MANUAL.value, comment="审核方式"
    )
    max_teams: Mapped[int] = mapped_column(Integer, default=100, comment="最大团队数")
    min_team_members: Mapped[int] = mapped_column(Integer, default=1, comment="团队最小人数")
    max_team_members: Mapped[int] = mapped_column(Integer, default=10, comment="团队最大人数")
    require_training: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否需要培训")
    require_exam: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否需要考试")
    exam_pass_score: Mapped[int] = mapped_column(Integer, default=60, comment="考试及格分数")
    require_insurance: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否需要保险")
    require_checkin: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否需要打卡")
    min_checkin_count: Mapped[int] = mapped_column(Integer, default=3, comment="最少打卡次数")

    # 扩展配置
    extra_config: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="扩展配置(JSON)")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否激活")
