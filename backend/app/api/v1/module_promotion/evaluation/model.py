"""
表彰评优 - 数据模型
"""

from datetime import datetime
from enum import Enum

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
    __mapper_args__: dict[str, list[str]] = {"exclude_properties": ["description"]}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    evaluation_name: Mapped[str | None] = mapped_column(
        String(200), nullable=True, comment="表彰名称"
    )

    evaluation_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="表彰类型"
    )

    evaluation_period: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="评选周期"
    )

    target_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="目标类型")

    target_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="目标ID")

    achievement_score: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="成绩得分"
    )

    ranking: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="排名")

    award_level: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="获奖级别")

    award_content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="获奖内容")

    evaluation_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="评选时间"
    )
