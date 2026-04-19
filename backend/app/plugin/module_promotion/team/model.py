"""
组织架构管理 - 数据模型
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


class TeamStatus(str, Enum):
    """招生组状态枚举"""
    ACTIVE = "active"        # 在用
    INACTIVE = "inactive"    # 停用
    DISSOLVED = "dissolved"  # 已解散


class TeamLevel(str, Enum):
    """招生组级别枚举"""
    HEADQUARTERS = "headquarters"  # 总部
    REGION = "region"              # 大区
    PROVINCE = "province"         # 省区
    CITY = "city"                 # 城市


class PromotionTeamModel(ModelMixin, UserMixin):
    """
    招生组表

    存储招生宣传活动中的组织架构信息
    """

    __tablename__: str = "promotion_team"
    __table_args__: dict[str, str] = {"comment": "招生组表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 基本信息
    team_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="招生组名称"
    )

    team_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
        comment="招生组编码"
    )

    team_level: Mapped[str] = mapped_column(
        String(20),
        default=TeamLevel.CITY.value,
        nullable=False,
        comment="招生组级别(headquarters/region/province/city)"
    )

    # 层级关系
    parent_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="上级招生组ID"
    )

    level_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="层级路径，如：/1/2/3/"
    )

    level_depth: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="层级深度"
    )

    # 区域信息
    region_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="区域名称"
    )

    province: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="省份"
    )

    city: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="城市"
    )

    district: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="区县"
    )

    # 职责信息
    responsibility: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="职责描述"
    )

    target_schools: Mapped[Optional[int]] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="目标学校数量"
    )

    target_students: Mapped[Optional[int]] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="目标学生数量"
    )

    # 负责人信息
    leader_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="负责人用户ID"
    )

    leader_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="负责人姓名"
    )

    leader_phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="负责人电话"
    )

    # 人员统计
    member_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="成员数量"
    )

    # 状态信息
    status: Mapped[str] = mapped_column(
        String(20),
        default=TeamStatus.ACTIVE.value,
        nullable=False,
        comment="状态(active/inactive/dissolved)"
    )

    # 排序
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="显示排序"
    )