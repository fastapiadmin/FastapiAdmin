"""
组织架构管理 - 数据模型
"""
from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    BIGINT,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class TeamStatus(str, Enum):
    """招生组状态枚举"""
    ACTIVE = "0"        # 在用
    INACTIVE = "1"      # 停用


class PromotionTeamModel(ModelMixin, UserMixin):
    """
    招生组表

    存储招生宣传活动中的组织架构信息
    """

    __tablename__: str = "promotion_team"
    __table_args__: dict[str, str] = {"comment": "招生组表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="招生组名称"
    )

    parent_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="上级招生组ID"
    )

    level: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="层级"
    )

    leader_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="负责人用户ID"
    )

    responsible_area: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="负责区域"
    )