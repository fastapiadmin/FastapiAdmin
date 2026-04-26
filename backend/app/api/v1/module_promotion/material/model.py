"""
物料管理 - 数据模型
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import BIGINT, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class MaterialStatus(str, Enum):
    """物料状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class ApplyStatus(str, Enum):
    """申领状态枚举"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ISSUED = "issued"
    CANCELLED = "cancelled"


class PromotionMaterialModel(ModelMixin, UserMixin):
    """
    物料表

    存储招生宣传活动中的物料信息
    """

    __tablename__: str = "promotion_material"
    __mapper_args__: dict[str, list[str]] = {"exclude_properties": ["description"]}
    __table_args__: dict[str, str] = {"comment": "物料表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="物料名称"
    )

    material_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="物料类型"
    )

    specification: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="规格"
    )

    stock_quantity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="库存数量"
    )

    unit: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="单位"
    )

    storage_location: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="存放位置"
    )


class PromotionMaterialApplyModel(ModelMixin, UserMixin):
    """
    物料申领表

    存储招生宣传活动中的物料申领信息
    """

    __tablename__: str = "promotion_material_apply"
    __table_args__: dict[str, str] = {"comment": "物料申领表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    apply_no: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="申领单号"
    )

    material_id: Mapped[int | None] = mapped_column(
        BIGINT,
        nullable=True,
        comment="物料ID"
    )

    apply_quantity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="申请数量"
    )

    use_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="使用日期"
    )

    use_purpose: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="使用目的"
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="备注"
    )

    approved_quantity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="批准数量"
    )

    issued_quantity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="发放数量"
    )

    approval_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="审批意见"
    )
