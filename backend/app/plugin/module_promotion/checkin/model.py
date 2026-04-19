"""
活动打卡 - 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    BIGINT,
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class CheckinStatus(str, Enum):
    """打卡状态枚举"""
    CHECKED_IN = "checked_in"     # 已打卡
    VALIDATED = "validated"       # 已验证
    INVALID = "invalid"           # 无效


class PromotionCheckinModel(ModelMixin, UserMixin):
    """
    活动打卡表

    存储招生宣传活动中的活动打卡信息
    """

    __tablename__: str = "promotion_checkin"
    __table_args__: dict[str, str] = {"comment": "活动打卡表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 打卡基本信息
    checkin_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="打卡单号"
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

    # 招生人员
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

    # 招生组
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

    # 打卡时间
    checkin_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="打卡时间"
    )

    # 打卡地点
    checkin_location: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="打卡地点"
    )

    # 打卡位置
    latitude: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="纬度"
    )

    longitude: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="经度"
    )

    # 打卡类型
    checkin_type: Mapped[str] = mapped_column(
        String(50),
        default="location",
        nullable=False,
        comment="打卡类型(location/photo/activity)"
    )

    # 打卡状态
    checkin_status: Mapped[str] = mapped_column(
        String(20),
        default=CheckinStatus.CHECKED_IN.value,
        nullable=False,
        comment="打卡状态(checked_in/validated/invalid)"
    )

    # 验证信息
    validated_by: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="验证人ID"
    )

    validated_by_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="验证人姓名"
    )

    validated_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="验证时间"
    )

    # 打卡内容
    checkin_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="打卡内容"
    )

    # 打卡图片
    checkin_images: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="打卡图片(JSON数组)"
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