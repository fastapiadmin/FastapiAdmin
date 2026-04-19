"""
人员管理 - 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BIGINT, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class PersonnelStatus(str, Enum):
    """人员状态枚举"""
    ACTIVE = "active"           # 在岗
    INACTIVE = "inactive"       # 离岗
    INVITED = "invited"         # 已邀请待加入
    PENDING = "pending"         # 待审核


class PersonnelType(str, Enum):
    """人员类型枚举"""
    RECRUIT = "recruit"         # 招募
    INVITE = "invite"           # 邀请
    MANUAL = "manual"           # 手动新增


class PromotionPersonnelModel(ModelMixin, UserMixin):
    """
    招生人员表

    存储招生宣传活动中的招生人员信息
    """

    __tablename__: str = "promotion_personnel"
    __table_args__: dict[str, str] = {"comment": "招生人员表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="人员姓名"
    )

    user_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="关联用户ID"
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="手机号"
    )

    email: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="邮箱"
    )

    team_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="招生组ID"
    )

    role: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="角色"
    )

    invitation_status: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="邀请状态"
    )

    join_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="加入时间"
    )

    exit_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="离开时间"
    )
