"""
人员管理 - 数据模型
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import BIGINT, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class PersonnelStatus(str, Enum):
    """人员状态枚举，控制人员生命周期：invited -> active -> inactive"""

    ACTIVE = "active"  # 在岗
    INACTIVE = "inactive"  # 离岗
    INVITED = "invited"  # 已邀请待加入（通过邀请码加入后变为active）
    PENDING = "pending"  # 待审核


class PersonnelType(str, Enum):
    """人员来源类型：区分不同入职方式"""

    RECRUIT = "recruit"  # 招募
    INVITE = "invite"  # 邀请（通过邀请码加入）
    MANUAL = "manual"  # 手动新增


class PromotionPersonnelModel(ModelMixin, UserMixin):
    """
    招生人员表

    存储招生宣传活动中的招生人员信息
    """

    __tablename__: str = "promotion_personnel"
    __mapper_args__: dict[str, list[str]] = {"exclude_properties": ["description"]}
    __table_args__: dict[str, str] = {"comment": "招生人员表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="人员姓名")

    user_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="关联用户ID")

    phone: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="手机号")

    email: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="邮箱")

    team_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="招生组ID")

    role: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="角色")

    province: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="省份")

    city: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="城市")

    responsible_area: Mapped[str | None] = mapped_column(
        String(200), nullable=True, comment="负责区域"
    )

    invitation_status: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="邀请状态"
    )

    join_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="加入时间")

    exit_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="离开时间")
