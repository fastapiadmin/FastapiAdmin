"""
团队管理 - 数据模型

功能：支持学生组队，队长发起和邀请机制
"""

from enum import Enum

from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class TeamStatus(str, Enum):
    """团队状态"""

    DRAFT = "draft"
    RECRUITING = "recruiting"
    FULL = "full"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class CampusReturnTeamModel(ModelMixin, UserMixin):
    """团队表"""

    __tablename__ = "campus_return_team"
    __table_args__ = {"comment": "返校宣讲团队表"}
    __loader_options__ = ["created_by", "updated_by"]

    batch_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="批次ID")
    team_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="团队名称")
    team_code: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, comment="团队邀请码"
    )
    captain_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="队长ID")
    high_school_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="目标高中ID")
    high_school_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="高中名称")
    status: Mapped[str] = mapped_column(
        String(20), default=TeamStatus.DRAFT.value, comment="团队状态"
    )
    max_members: Mapped[int] = mapped_column(Integer, default=10, comment="最大成员数")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="团队介绍")
    plan_date: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="计划宣讲日期")
    extra_info: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="扩展信息")
