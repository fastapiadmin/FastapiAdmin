"""
目标学校管理 - 数据模型
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


class FollowStatus(str, Enum):
    """跟进状态枚举"""
    NEW = "new"                 # 新增
    CONTACTED = "contacted"   # 已联系
    VISITED = "visited"       # 已走访
    COOPERATING = "cooperating" # 合作中
    INACTIVE = "inactive"      # 已终止


class PriorityLevel(str, Enum):
    """优先级枚举"""
    HIGH = "high"     # 高
    MEDIUM = "medium" # 中
    LOW = "low"      # 低


class PromotionTargetSchoolModel(ModelMixin, UserMixin):
    """
    目标学校表

    存储招生宣传活动中的目标学校信息
    """

    __tablename__: str = "promotion_target_school"
    __table_args__: dict[str, str] = {"comment": "目标学校表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 学校基本信息
    school_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="学校名称"
    )

    school_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
        comment="学校代码"
    )

    school_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="学校类型(高中/初中/完中)"
    )

    # 地理位置
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

    address: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="详细地址"
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

    # 负责人员
    personnel_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="负责人ID"
    )

    personnel_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="负责人姓名"
    )

    # 优先级
    priority: Mapped[str] = mapped_column(
        String(20),
        default=PriorityLevel.MEDIUM.value,
        nullable=False,
        comment="优先级(high/medium/low)"
    )

    # 跟进状态
    follow_status: Mapped[str] = mapped_column(
        String(20),
        default=FollowStatus.NEW.value,
        nullable=False,
        comment="跟进状态(new/contacted/visited/cooperating/inactive)"
    )

    # 学校信息
    student_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="学生数量"
    )

    graduate_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="毕业生数量"
    )

    admission_rate: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="升学率"
    )

    # 联系信息
    contact_person: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="联系人"
    )

    contact_phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="联系电话"
    )

    contact_title: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="联系人职务"
    )

    # 走访信息
    last_visit_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="最后走访日期"
    )

    last_visit_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="最后走访内容"
    )

    next_visit_plan: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="下次走访计划"
    )

    next_visit_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="计划走访日期"
    )

    visit_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="走访次数"
    )

    # 合作信息
    cooperation_start_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="合作开始日期"
    )

    cooperation_end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="合作结束日期"
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