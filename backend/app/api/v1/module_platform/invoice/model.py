from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin, TenantMixin, UserMixin

if TYPE_CHECKING:
    from app.api.v1.module_platform.order.model import OrderModel


class InvoiceModel(ModelMixin, TenantMixin, UserMixin):
    """
    平台发票表

    status: 0=待开票 1=已开票 2=开票失败 3=已作废
    """

    __tablename__: str = "platform_invoice"
    __table_args__: dict[str, str] = {"comment": "发票表"}
    __loader_options__: list[str] = ["created_by", "updated_by", "deleted_by", "tenant_by"]

    invoice_no: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, comment="发票号码")
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("platform_order.id"), nullable=False, unique=True, comment="关联订单")
    invoice_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="vat_normal/vat_special")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="发票抬头")
    tax_no: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="纳税人识别号")
    bank_info: Mapped[str | None] = mapped_column(Text, nullable=True, comment="开户行及账号")
    address_info: Mapped[str | None] = mapped_column(Text, nullable=True, comment="注册地址及电话")
    amount: Mapped[int] = mapped_column(Integer, nullable=False, comment="发票金额(分)")
    tax_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="税额(分)")
    pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="发票PDF下载地址")
    oss_license_pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="开源授权函PDF下载地址")
    api_response: Mapped[str | None] = mapped_column(Text, nullable=True, comment="第三方API响应")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:待开票 1:已开票 2:开票失败 3:已作废)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")

    # 关联关系
    order: Mapped["OrderModel"] = relationship("OrderModel", lazy="selectin")
