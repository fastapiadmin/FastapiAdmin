"""
报名管理 - 数据模型

功能：学生在线报名，审核筛选流程自动化
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    JSON,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class RegistrationStatus(str, Enum):
    """报名状态枚举"""

    DRAFT = "draft"  # 草稿
    SUBMITTED = "submitted"  # 已提交
    REVIEWING = "reviewing"  # 审核中
    APPROVED = "approved"  # 已通过
    REJECTED = "rejected"  # 已拒绝
    CANCELLED = "cancelled"  # 已取消
    WITHDRAWN = "withdrawn"  # 已退出


class CampusReturnRegistrationModel(ModelMixin, UserMixin):
    """
    返校宣讲报名表

    存储学生的报名信息
    """

    __tablename__: str = "campus_return_registration"
    __table_args__: dict[str, str] = {"comment": "返校宣讲报名表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 关联信息
    batch_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="批次ID")
    student_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="学生ID")
    team_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="团队ID")

    # 学生基本信息
    student_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="学生姓名")
    student_number: Mapped[str] = mapped_column(String(50), nullable=False, comment="学号")
    id_card: Mapped[str] = mapped_column(String(20), nullable=True, comment="身份证号")
    phone: Mapped[str] = mapped_column(String(20), nullable=True, comment="联系电话")
    email: Mapped[str] = mapped_column(String(100), nullable=True, comment="电子邮箱")
    major: Mapped[str] = mapped_column(String(100), nullable=True, comment="专业")
    grade: Mapped[str] = mapped_column(String(20), nullable=True, comment="年级")
    college: Mapped[str] = mapped_column(String(100), nullable=True, comment="学院")

    # 高中信息
    high_school_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="高中名称")
    high_school_province: Mapped[str] = mapped_column(
        String(50), nullable=True, comment="高中所在省"
    )
    high_school_city: Mapped[str] = mapped_column(String(50), nullable=True, comment="高中所在市")
    high_school_address: Mapped[str] = mapped_column(String(200), nullable=True, comment="高中地址")
    teacher_name: Mapped[str] = mapped_column(String(50), nullable=True, comment="对接老师姓名")
    teacher_phone: Mapped[str] = mapped_column(String(20), nullable=True, comment="对接老师电话")

    # 家庭信息（用于保险）
    hometown: Mapped[str] = mapped_column(String(200), nullable=True, comment="家庭所在地")

    # 报名状态
    status: Mapped[str] = mapped_column(
        String(20), default=RegistrationStatus.DRAFT.value, comment="报名状态"
    )
    review_comment: Mapped[str | None] = mapped_column(Text, nullable=True, comment="审核意见")
    reviewed_by: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="审核人ID")
    reviewed_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="审核时间"
    )

    # 扩展信息
    motivation: Mapped[str | None] = mapped_column(Text, nullable=True, comment="参加动机")
    experience: Mapped[str | None] = mapped_column(Text, nullable=True, comment="相关经历")
    extra_info: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="扩展信息(JSON)")
