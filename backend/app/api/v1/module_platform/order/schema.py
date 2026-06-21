from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam
from app.core.base_schema import BaseSchema, TenantBySchema


class OrderCreateInternalSchema(BaseModel):
    """订单创建（内部 CRUD 用，包含所有业务字段）"""

    order_no: str = Field(..., description="订单号")
    tenant_id: int = Field(..., description="租户ID")
    package_id: int | None = Field(default=None, description="套餐ID")
    plugin_id: int | None = Field(default=None, description="插件ID")
    order_type: str = Field(..., description="订单类型")
    amount: int = Field(..., description="订单金额(分)")
    period_count: int = Field(default=1, description="时长(月)")
    pay_method: str | None = Field(default=None, description="支付方式")
    pay_time: datetime | None = Field(default=None, description="支付时间")
    expire_time: datetime = Field(..., description="过期时间")
    status: int = Field(default=0, description="订单状态")
    description: str | None = Field(default=None, description="备注")


class OrderUpdateInternalSchema(BaseModel):
    """订单更新（内部 CRUD 用）"""

    status: int | None = Field(default=None, description="订单状态")
    pay_method: str | None = Field(default=None, description="支付方式")
    pay_time: datetime | None = Field(default=None, description="支付时间")
    description: str | None = Field(default=None, description="备注")


class PaymentRecordCreateSchema(BaseModel):
    """支付记录创建"""

    order_id: int = Field(..., description="订单ID")
    transaction_id: str | None = Field(default=None, description="交易流水号")
    pay_method: str = Field(..., description="支付方式")
    amount: int = Field(..., description="支付金额(分)")
    status: int = Field(default=1, description="支付状态")
    raw_response: str | None = Field(default=None, description="原始响应")
    pay_time: datetime | None = Field(default=None, description="支付时间")
    description: str | None = Field(default=None, description="备注")


class RefundCreateSchema(BaseModel):
    """退款记录创建"""

    order_id: int = Field(..., description="订单ID")
    refund_no: str = Field(..., description="退款单号")
    amount: int = Field(..., description="退款金额(分)")
    reason: str = Field(..., description="退款原因")
    refund_transaction_id: str | None = Field(default=None, description="退款交易流水号")
    reviewer_id: int | None = Field(default=None, description="审核人ID")
    review_time: datetime | None = Field(default=None, description="审核时间")
    reject_reason: str | None = Field(default=None, description="驳回原因")
    status: int = Field(default=1, description="退款状态")
    description: str | None = Field(default=None, description="备注")


class RefundUpdateSchema(BaseModel):
    """退款记录更新"""

    status: int | None = Field(default=None, description="退款状态")
    reviewer_id: int | None = Field(default=None, description="审核人ID")
    review_time: datetime | None = Field(default=None, description="审核时间")
    reject_reason: str | None = Field(default=None, description="驳回原因")
    refund_transaction_id: str | None = Field(default=None, description="退款交易流水号")
    description: str | None = Field(default=None, description="备注")


class OrderCreateSchema(BaseModel):
    """创建订单（套餐或插件）"""

    tenant_id: int = Field(..., ge=1, description="租户ID")
    package_id: int | None = Field(default=None, ge=1, description="套餐ID（套餐订单必填）")
    plugin_id: int | None = Field(default=None, ge=1, description="插件ID（插件订单必填）")
    order_type: Literal["new", "renew", "upgrade", "downgrade", "plugin"] = Field(
        ...,
        description="订单类型(new:新购 renew:续费 upgrade:升级 downgrade:降级 plugin:插件)",
    )
    pay_method: Literal["alipay", "wxpay", "free"] | None = Field(default=None, description="支付方式(留空=自动)")

    @field_validator("tenant_id")
    @classmethod
    def positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("必须为正整数")
        return v

    @model_validator(mode="after")
    def check_target(self) -> None:
        if self.order_type == "plugin":
            if not self.plugin_id or self.plugin_id <= 0:
                raise ValueError("插件订单必须指定 plugin_id")
        else:
            if not self.package_id or self.package_id <= 0:
                raise ValueError("套餐订单必须指定 package_id")


class OrderOutSchema(BaseSchema, TenantBySchema):
    """订单输出"""

    model_config = ConfigDict(from_attributes=True)

    order_no: str = Field(..., description="订单号")
    package_id: int | None = Field(default=None, description="套餐ID")
    plugin_id: int | None = Field(default=None, description="插件ID")
    order_type: str = Field(..., description="订单类型")
    amount: int = Field(..., description="订单金额(分)")
    period_count: int = Field(..., description="时长(月)")
    pay_method: str | None = Field(default=None, description="支付方式")
    pay_time: datetime | None = Field(default=None, description="支付时间")
    expire_time: datetime = Field(..., description="过期时间")
    status: int = Field(..., description="订单状态(0:待支付 1:已支付 2:已取消 3:已退款)")
    description: str | None = Field(default=None, description="备注")


@dataclass
class OrderQueryParam(BaseQueryParam):
    """订单查询参数"""

    tenant_id: int | None = Query(None, description="租户ID")
    status: int | None = Query(None, description="订单状态(0:待支付 1:已支付 2:已取消 3:已退款)")
    order_type: str | None = Query(None, description="订单类型")
    order_no: str | None = Query(None, description="订单号")

    def __post_init__(self) -> None:
        if self.tenant_id is not None:
            self.tenant_id = (QueueEnum.eq.value, self.tenant_id)
        if self.status is not None:
            self.status = (QueueEnum.eq.value, self.status)
        if self.order_type:
            self.order_type = (QueueEnum.eq.value, self.order_type)
        if self.order_no:
            self.order_no = (QueueEnum.like.value, self.order_no)


class PaymentCallbackSchema(BaseModel):
    """支付回调数据"""

    transaction_id: str | None = Field(default=None, description="交易流水号")
    amount: int = Field(..., description="支付金额(分)")
    order_id: int | None = Field(default=None, description="订单ID")
    raw_data: dict | None = Field(default=None, description="原始数据")


class PaymentRecordOutSchema(BaseSchema, TenantBySchema):
    """支付记录输出"""

    model_config = ConfigDict(from_attributes=True)

    order_id: int = Field(..., description="订单ID")
    transaction_id: str | None = Field(default=None, description="交易流水号")
    pay_method: str = Field(..., description="支付方式")
    amount: int = Field(..., description="支付金额(分)")
    pay_time: datetime | None = Field(default=None, description="支付时间")
    status: int = Field(..., description="支付状态")
    description: str | None = Field(default=None, description="备注")


class PaymentCreateOut(BaseModel):
    """创建支付结果"""

    pay_url: str = Field(..., description="支付链接")
    qr_code_url: str = Field(..., description="二维码链接")
    trade_no: str = Field(..., description="交易流水号")
    order_id: int = Field(..., description="订单ID")
    order_no: str = Field(..., description="订单号")
    amount: int = Field(..., description="支付金额(分)")


class PaymentStatusOut(BaseModel):
    """支付状态查询结果"""

    exists: bool = Field(..., description="是否存在")
    order_id: int | None = Field(default=None, description="订单ID")
    status: int | None = Field(default=None, description="支付状态")
    paid: bool = Field(default=False, description="是否已支付")
    pay_method: str | None = Field(default=None, description="支付方式")
    pay_time: str | None = Field(default=None, description="支付时间")


class OrderStatusMessage(BaseModel):
    """订单/退款操作结果消息"""

    id: int = Field(..., description="订单/退款ID")
    status: int = Field(..., description="状态")
    message: str = Field(..., description="消息")


class RefundApplySchema(BaseModel):
    """退款申请"""

    reason: str = Field(..., min_length=1, max_length=500, description="退款原因")


class RefundReviewSchema(BaseModel):
    """退款审核"""

    reject_reason: str | None = Field(default=None, max_length=500, description="驳回原因(审核通过时可不填)")


class RefundOutSchema(BaseSchema, TenantBySchema):
    """退款记录输出"""

    model_config = ConfigDict(from_attributes=True)

    order_id: int = Field(..., description="订单ID")
    refund_no: str = Field(..., description="退款单号")
    amount: int = Field(..., description="退款金额(分)")
    reason: str = Field(..., description="退款原因")
    refund_transaction_id: str | None = Field(default=None, description="退款交易流水号")
    reviewer_id: int | None = Field(default=None, description="审核人ID")
    review_time: datetime | None = Field(default=None, description="审核时间")
    reject_reason: str | None = Field(default=None, description="驳回原因")
    status: int = Field(..., description="退款状态")
    description: str | None = Field(default=None, description="备注")
