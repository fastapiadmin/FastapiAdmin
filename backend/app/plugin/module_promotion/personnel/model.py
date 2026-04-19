"""
人员管理 - 数据模型
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

    # 基本信息
    personnel_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="人员姓名"
    )

    personnel_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
        comment="人员编号"
    )

    personnel_type: Mapped[str] = mapped_column(
        String(20),
        default=PersonnelType.MANUAL.value,
        nullable=False,
        comment="人员类型(recruit/invite/manual)"
    )

    # 用户关联
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

    # 招生组关联
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

    # 区域信息
    province: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="负责省份"
    )

    city: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="负责城市"
    )

    # 职务信息
    position: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="职务"
    )

    # 人员状态
    status: Mapped[str] = mapped_column(
        String(20),
        default=PersonnelStatus.ACTIVE.value,
        nullable=False,
        comment="状态(active/inactive/invited/pending)"
    )

    # 入职/邀请信息
    join_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="加入日期"
    )

    leave_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="离开日期"
    )

    leave_reason: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="离开原因"
    )

    # 邀请信息
    invite_code: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="邀请码"
    )

    invite_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="邀请时间"
    )

    invite_expire_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="邀请过期时间"
    )

    # 绩效统计
    target_schools: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="目标学校数量"
    )

    visited_schools: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="已访问学校数量"
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