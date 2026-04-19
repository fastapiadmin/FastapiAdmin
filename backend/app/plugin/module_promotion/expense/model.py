"""
费用报销 - 数据模型
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


class ExpenseStatus(str, Enum):
    """报销状态枚举"""
    PENDING = "pending"       # 待审批
    APPROVED = "approved"     # 已批准
    REJECTED = "rejected"     # 已拒绝
    REIMBURSED = "reimbursed" # 已报销
    CANCELLED = "cancelled"   # 已取消


class ExpenseType(str, Enum):
    """费用类型枚举"""
    TRANSPORTATION = "transportation"   # 交通费
    ACCOMMODATION = "accommodation"     # 住宿费
    MEAL = "meal"                       # 餐费
    COMMUNICATION = "communication"     # 通讯费
    ENTERTAINMENT = "entertainment"     # 招待费
    MATERIAL = "material"               # 物料费
    OTHER = "other"                     # 其他


class PromotionExpenseModel(ModelMixin, UserMixin):
    """
    费用报销表

    存储招生宣传活动中的费用报销信息
    """

    __tablename__: str = "promotion_expense"
    __table_args__: dict[str, str] = {"comment": "费用报销表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 报销基本信息
    expense_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="报销单号"
    )

    # 关联活动
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

    # 关联行程
    trip_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="关联行程ID"
    )

    trip_no: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="行程单号"
    )

    # 招生组和人员
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

    # 费用信息
    expense_type: Mapped[str] = mapped_column(
        String(50),
        default=ExpenseType.OTHER.value,
        nullable=False,
        comment="费用类型(transportation/accommodation/meal/communication/entertainment/material/other)"
    )

    expense_amount: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        comment="报销金额"
    )

    # 费用明细
    expense_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="费用日期"
    )

    expense_description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="费用说明"
    )

    invoice_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="发票数量"
    )

    has_invoice: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="是否有发票"
    )

    # 审批信息
    approval_status: Mapped[str] = mapped_column(
        String(20),
        default=ExpenseStatus.PENDING.value,
        nullable=False,
        comment="审批状态(pending/approved/rejected/reimbursed/cancelled)"
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

    # 报销信息
    reimburse_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="报销时间"
    )

    reimbursement_account: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="报销账户"
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