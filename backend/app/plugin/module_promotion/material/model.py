"""
物料管理 - 数据模型
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


class MaterialStatus(str, Enum):
    """物料状态枚举"""
    AVAILABLE = "available"     # 可用
    LOW_STOCK = "low_stock"    # 库存不足
    OUT_OF_STOCK = "out_of_stock"  # 已用完
    DISCONTINUED = "discontinued"  # 已停用


class MaterialType(str, Enum):
    """物料类型枚举"""
    BROCHURE = "brochure"         # 宣传册
    FLYER = "flyer"               # 传单
    POSTER = "poster"             # 海报
    GIFT = "gift"                 # 礼品
    STATIONERY = "stationery"     # 文具
    UNIFORM = "uniform"           # 工作服
    FLAG = "flag"                 # 旗帜
    BANNER = "banner"             # 横幅
    OTHER = "other"               # 其他


class ApplyStatus(str, Enum):
    """申请状态枚举"""
    PENDING = "pending"       # 待审核
    APPROVED = "approved"     # 已批准
    REJECTED = "rejected"     # 已拒绝
    ISSUED = "issued"         # 已发放
    CANCELLED = "cancelled"   # 已取消


class PromotionMaterialModel(ModelMixin, UserMixin):
    """
    物料表

    存储招生宣传活动中的物料信息
    """

    __tablename__: str = "promotion_material"
    __table_args__: dict[str, str] = {"comment": "物料表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 物料基本信息
    material_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="物料名称"
    )

    material_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
        comment="物料编码"
    )

    material_type: Mapped[str] = mapped_column(
        String(50),
        default=MaterialType.OTHER.value,
        nullable=False,
        comment="物料类型(brochure/flyer/poster/gift/stationery/uniform/flag/banner/other)"
    )

    # 规格信息
    specification: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="规格"
    )

    unit: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="单位"
    )

    # 库存信息
    total_stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="总库存"
    )

    available_stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="可用库存"
    )

    reserved_stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="预留库存"
    )

    # 预警信息
    low_stock_threshold: Mapped[int] = mapped_column(
        Integer,
        default=10,
        nullable=False,
        comment="库存预警阈值"
    )

    # 费用信息
    unit_price: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="单价"
    )

    # 物料状态
    status: Mapped[str] = mapped_column(
        String(20),
        default=MaterialStatus.AVAILABLE.value,
        nullable=False,
        comment="状态(available/low_stock/out_of_stock/discontinued)"
    )

    # 物料描述
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="物料描述"
    )

    # 供应商信息
    supplier_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="供应商名称"
    )

    supplier_contact: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="供应商联系人"
    )

    supplier_phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="供应商电话"
    )

    # 图片
    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="物料图片"
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


class PromotionMaterialApplyModel(ModelMixin, UserMixin):
    """
    物料申请表

    存储物料申领记录
    """

    __tablename__: str = "promotion_material_apply"
    __table_args__: dict[str, str] = {"comment": "物料申请表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 申请基本信息
    apply_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="申请单号"
    )

    # 招生组信息
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

    # 申请人信息
    applicant_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="申请人ID"
    )

    applicant_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="申请人姓名"
    )

    # 物料信息
    material_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="物料ID"
    )

    material_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="物料名称"
    )

    material_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="物料类型"
    )

    # 申请数量
    apply_quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="申请数量"
    )

    approved_quantity: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="批准数量"
    )

    issued_quantity: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="已发放数量"
    )

    # 用途
    usage: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="用途说明"
    )

    # 活动信息
    activity_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="关联活动ID"
    )

    activity_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="关联活动名称"
    )

    # 审批信息
    apply_status: Mapped[str] = mapped_column(
        String(20),
        default=ApplyStatus.PENDING.value,
        nullable=False,
        comment="申请状态(pending/approved/rejected/issued/cancelled)"
    )

    approval_comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="审批意见"
    )

    approver_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="审批人ID"
    )

    approver_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="审批人姓名"
    )

    approval_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="审批时间"
    )

    # 发放信息
    issuer_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="发放人ID"
    )

    issuer_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="发放人姓名"
    )

    issue_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="发放时间"
    )

    # 排序
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="显示排序"
    )