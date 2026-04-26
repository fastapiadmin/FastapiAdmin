"""
目标学校管理 - 数据模型
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import BIGINT, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class FollowStatus(str, Enum):
    """跟进状态枚举"""
    NEW = "new"
    CONTACTED = "contacted"
    VISITED = "visited"
    COOPERATING = "cooperating"
    INACTIVE = "inactive"


class IntentionLevel(str, Enum):
    """意向级别枚举"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PromotionTargetSchoolModel(ModelMixin, UserMixin):
    """
    目标学校表

    存储招生宣传活动中的目标学校信息
    """

    __tablename__: str = "promotion_target_school"
    __table_args__: dict[str, str] = {"comment": "目标学校表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="学校名称"
    )

    school_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="学校类型"
    )

    province: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="省份"
    )

    city: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="城市"
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="地址"
    )

    contact_person: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="联系人"
    )

    contact_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="联系电话"
    )

    student_scale: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="学生规模"
    )

    intention_level: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="意向级别"
    )

    follow_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="跟进状态"
    )

    follow_person_id: Mapped[int | None] = mapped_column(
        BIGINT,
        nullable=True,
        comment="跟进人ID"
    )

    last_follow_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="最后跟进时间"
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="备注"
    )
