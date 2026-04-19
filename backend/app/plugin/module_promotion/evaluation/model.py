"""
表彰评优 - 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BIGINT, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class EvaluationStatus(str, Enum):
    """评选状态枚举"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"


class PromotionEvaluationModel(ModelMixin, UserMixin):
    """
    表彰评优表

    存储招生宣传活动中的表彰评优信息
    """

    __tablename__: str = "promotion_evaluation"
    __table_args__: dict[str, str] = {"comment": "表彰评优表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    evaluation_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="表彰名称"
    )

    evaluation_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="表彰类型"
    )

    evaluation_period: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="评选周期"
    )

    target_type: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="目标类型"
    )

    target_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="目标ID"
    )

    achievement_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="成绩得分"
    )

    ranking: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="排名"
    )

    award_level: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="获奖级别"
    )

    award_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="获奖内容"
    )

    evaluation_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="评选时间"
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="备注/描述"
    )
