from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin, TenantMixin

if TYPE_CHECKING:
    from app.api.v1.module_platform.package.model import PackageModel
    from app.api.v1.module_platform.plugin.model import PluginModel
    from app.api.v1.module_system.user.model import UserModel


class OrderModel(ModelMixin, TenantMixin):
    """platform_order — 订单表

    支持两种订单类型：
    - 套餐订单：new/renew/upgrade/downgrade，package_id 必填
    - 插件订单：plugin，plugin_id 必填，package_id 为空

    status: 0=待支付 1=已支付 2=已取消 3=已退款
    """

    __tablename__: str = "platform_order"
    __table_args__: dict[str, str] = {"comment": "订单表"}
    __loader_options__: list[str] = ["tenant_by"]

    order_no: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, comment="订单号")
    package_id: Mapped[int | None] = mapped_column(ForeignKey("platform_package.id"), nullable=True, comment="购买套餐(插件订单为空)")
    plugin_id: Mapped[int | None] = mapped_column(ForeignKey("platform_plugin.id"), nullable=True, comment="购买插件(套餐订单为空)")
    order_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="new/renew/upgrade/downgrade/plugin")
    amount: Mapped[int] = mapped_column(Integer, nullable=False, comment="金额(分)")
    period_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="购买周期数")
    pay_method: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="alipay/wxpay")
    pay_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="支付时间")
    expire_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="订单过期时间(15分钟)")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:待支付 1:已支付 2:已取消 3:已退款)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")

    # 关联关系
    package: Mapped["PackageModel | None"] = relationship("PackageModel", lazy="selectin")
    plugin: Mapped["PluginModel | None"] = relationship("PluginModel", lazy="selectin")


class PaymentRecordModel(ModelMixin, TenantMixin):
    """platform_payment_record — 支付记录表

    status: 0=处理中 1=成功 2=失败
    """

    __tablename__: str = "platform_payment_record"
    __table_args__: dict[str, str] = {"comment": "支付记录表"}
    __loader_options__: list[str] = ["tenant_by"]

    order_id: Mapped[int] = mapped_column(ForeignKey("platform_order.id"), nullable=False, comment="关联订单")
    transaction_id: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True, comment="第三方交易号")
    pay_method: Mapped[str] = mapped_column(String(20), nullable=False, comment="支付方式")
    amount: Mapped[int] = mapped_column(Integer, nullable=False, comment="支付金额(分)")
    raw_response: Mapped[str | None] = mapped_column(Text, nullable=True, comment="原始回调JSON")
    pay_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="支付完成时间")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:处理中 1:成功 2:失败)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")

    # 关联关系
    order: Mapped["OrderModel"] = relationship("OrderModel", lazy="selectin")


class RefundModel(ModelMixin, TenantMixin):
    """platform_refund — 退款表

    status: 1=申请中 2=已退款 3=已驳回 4=已取消
    """

    __tablename__: str = "platform_refund"
    __table_args__: dict[str, str] = {"comment": "退款表"}
    __loader_options__: list[str] = ["tenant_by"]

    order_id: Mapped[int] = mapped_column(ForeignKey("platform_order.id"), nullable=False, unique=True, comment="关联订单")
    refund_no: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, comment="退款单号")
    amount: Mapped[int] = mapped_column(Integer, nullable=False, comment="退款金额(分)")
    reason: Mapped[str] = mapped_column(Text, nullable=False, comment="退款原因")
    refund_transaction_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="退款交易号")
    reviewer_id: Mapped[int | None] = mapped_column(ForeignKey("sys_user.id"), nullable=True, comment="审核人")
    review_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="审核时间")
    reject_reason: Mapped[str | None] = mapped_column(Text, nullable=True, comment="驳回原因")
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="状态(1:申请中 2:已退款 3:已驳回 4:已取消)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")

    # 关联关系
    order: Mapped["OrderModel"] = relationship("OrderModel", lazy="selectin")
    reviewer: Mapped["UserModel | None"] = relationship("UserModel", foreign_keys=[reviewer_id], lazy="selectin")
