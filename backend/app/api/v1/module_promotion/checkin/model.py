"""
活动打卡 - 数据模型
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import BIGINT, JSON, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class CheckinStatus(str, Enum):
    """打卡状态枚举，由管理员审核或GPS验证自动判定"""

    CHECKED_IN = "checked_in"  # 已打卡（待验证）
    VALIDATED = "validated"  # 已验证（有效打卡）
    INVALID = "invalid"  # 无效打卡


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

    target_longitude: Mapped[Numeric | None] = mapped_column(
        Numeric(10, 7), nullable=True, comment="目标经度"
    )

    target_latitude: Mapped[Numeric | None] = mapped_column(
        Numeric(10, 7), nullable=True, comment="目标纬度"
    )

    allowed_radius: Mapped[Numeric | None] = mapped_column(
        Numeric(10, 2), nullable=True, comment="允许打卡半径(米)"
    )

    gps_validated: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="GPS是否验证通过(0否,1是)"
    )

    gps_distance: Mapped[Numeric | None] = mapped_column(
        Numeric(10, 2), nullable=True, comment="GPS距离(米)"
    )

    photo_urls: Mapped[JSON | None] = mapped_column(JSON, nullable=True, comment="照片URLs")

    remarks: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
