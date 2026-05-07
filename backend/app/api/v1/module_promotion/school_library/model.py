"""
全国高中学校库 - 数据模型
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class PromotionSchoolLibraryModel(ModelMixin, UserMixin):
    """
    全国高中学校库表

    存储全国高中学校基础信息，供目标学校管理参考
    """

    __tablename__: str = "promotion_school_library"
    __table_args__: dict[str, str] = {"comment": "全国高中学校库表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="学校名称")

    school_code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="学校编码")

    school_type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="学校类型")

    province: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="省份")

    city: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="城市")

    district: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="区县")

    address: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="地址")

    contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="联系电话")

    student_scale: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="学生规模")

    is_key_school: Mapped[str | None] = mapped_column(
        String(10), nullable=True, comment="是否重点校"
    )
