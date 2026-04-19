"""
行程报备 - 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BIGINT, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class TripStatus(str, Enum):
    """行程状态枚举"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PromotionTripModel(ModelMixin, UserMixin):
    """
    行程报备表

    存储招生宣传活动中的行程报备信息
    """

    __tablename__: str = "promotion_trip"
    __table_args__: dict[str, str] = {"comment": "行程报备表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    personnel_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="人员ID"
    )

    trip_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="行程名称"
    )

    departure_location: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="出发地"
    )

    destination: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="目的地"
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

    transportation: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="交通方式"
    )

    trip_status: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="行程状态"
    )

    enable_location_sharing: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="启用位置共享"
    )

    last_location_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="最后位置时间"
    )

    last_latitude: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(10, 7),
        nullable=True,
        comment="最后纬度"
    )

    last_longitude: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(10, 7),
        nullable=True,
        comment="最后经度"
    )

    last_location_address: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="最后位置地址"
    )
