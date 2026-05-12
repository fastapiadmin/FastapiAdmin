"""
高校信息管理 - 数据模型
"""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class UniversityModel(ModelMixin, UserMixin):
    """
    高校信息表

    存储参与咨询会的高校基本信息
    """

    __tablename__: str = "consultation_university"
    __table_args__: dict[str, str] = {"comment": "高校信息表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 基本信息
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="高校名称")
    code: Mapped[str | None] = mapped_column(String(50), unique=True, comment="高校代码")
    abbreviation: Mapped[str | None] = mapped_column(String(50), comment="高校简称")

    # 联系信息
    contact_person: Mapped[str | None] = mapped_column(String(100), comment="联系人")
    contact_phone: Mapped[str | None] = mapped_column(String(20), comment="联系电话")
    contact_email: Mapped[str | None] = mapped_column(String(100), comment="联系邮箱")

    # 地址信息
    province: Mapped[str | None] = mapped_column(String(50), comment="省份")
    city: Mapped[str | None] = mapped_column(String(50), comment="城市")
    address: Mapped[str | None] = mapped_column(String(500), comment="详细地址")

    # 其他信息
    description: Mapped[str | None] = mapped_column(Text, comment="高校简介")
    website: Mapped[str | None] = mapped_column(String(200), comment="官网链接")
    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False,
        comment="状态(active/inactive)",
    )
