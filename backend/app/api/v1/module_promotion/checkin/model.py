"""
活动打卡 - 数据模型
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import BIGINT, JSON, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class CheckinStatus(str, Enum):
    """打卡状态枚举"""

    CHECKED_IN = "checked_in"
    VALIDATED = "validated"
    INVALID = "invalid"


class PromotionCheckinModel(ModelMixin, UserMixin):
    """
    活动打卡表

    存储招生宣传活动中的活动打卡信息
    """

    __tablename__: str = "promotion_checkin"
    __table_args__: dict[str, str] = {"comment": "活动打卡表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]
    __mapper_args__: dict[str, list[str]] = {"exclude_properties": ["description"]}

    activity_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="活动ID")

    personnel_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="人员ID")

    checkin_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="打卡时间"
    )

    checkin_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="打卡类型")

    location: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="位置")

    longitude: Mapped[Numeric | None] = mapped_column(Numeric(10, 7), nullable=True, comment="经度")

    latitude: Mapped[Numeric | None] = mapped_column(Numeric(10, 7), nullable=True, comment="纬度")

    photo_urls: Mapped[JSON | None] = mapped_column(JSON, nullable=True, comment="照片URLs")

    remarks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
