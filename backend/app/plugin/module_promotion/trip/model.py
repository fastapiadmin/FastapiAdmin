"""
行程报备 - 数据模型
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


class TripStatus(str, Enum):
    """行程状态枚举"""
    PLANNED = "planned"         # 计划中
    IN_PROGRESS = "in_progress" # 进行中
    COMPLETED = "completed"     # 已完成
    CANCELLED = "cancelled"     # 已取消


class PromotionTripModel(ModelMixin, UserMixin):
    """
    行程报备表

    存储招生宣传活动中的行程报备信息
    """

    __tablename__: str = "promotion_trip"
    __table_args__: dict[str, str] = {"comment": "行程报备表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 行程基本信息
    trip_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="行程单号"
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

    # 招生组和人员
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

    personnel_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="行程人员ID"
    )

    personnel_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="行程人员姓名"
    )

    # 行程时间
    departure_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="出发日期"
    )

    departure_time: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        comment="出发时间"
    )

    return_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="返回日期"
    )

    return_time: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        comment="返回时间"
    )

    # 出发地
    departure_province: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="出发省份"
    )

    departure_city: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="出发城市"
    )

    departure_address: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="出发详细地址"
    )

    # 目的地
    destination_province: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="目的省份"
    )

    destination_city: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="目的城市"
    )

    destination_address: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="目的详细地址"
    )

    # 交通信息
    transportation_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="交通类型(飞机/火车/汽车/其他)"
    )

    transportation_no: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="航班/车次号"
    )

    # 行程状态
    trip_status: Mapped[str] = mapped_column(
        String(20),
        default=TripStatus.PLANNED.value,
        nullable=False,
        comment="行程状态(planned/in_progress/completed/cancelled)"
    )

    # 位置共享
    enable_location_sharing: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="启用位置共享"
    )

    last_location_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="最后位置更新时间"
    )

    last_latitude: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="最后位置纬度"
    )

    last_longitude: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="最后位置经度"
    )

    last_location_address: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="最后位置地址"
    )

    # 行程目的
    trip_purpose: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="行程目的"
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