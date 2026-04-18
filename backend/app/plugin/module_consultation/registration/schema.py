"""
咨询会报名管理 - 数据验证Schema
"""
from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class RegistrationCreateSchema(BaseSchema):
    """新增报名模型"""

    consultation_id: int = Field(..., description="咨询会ID")
    university_id: int = Field(..., description="高校ID")
    university_name: str | None = Field(default=None, description="高校名称")
    contact_person: str | None = Field(default=None, description="联系人")
    contact_phone: str | None = Field(default=None, description="联系电话")
    contact_email: str | None = Field(default=None, description="联系邮箱")
    booth_size: str | None = Field(default=None, description="展位大小")
    remarks: str | None = Field(default=None, description="备注")


class RegistrationUpdateSchema(RegistrationCreateSchema):
    """更新报名模型"""
    pass


class RegistrationOutSchema(RegistrationCreateSchema, BaseSchema, UserBySchema):
    """报名响应模型"""

    model_config = ConfigDict(from_attributes=True)

    booth_number: Optional[str] = Field(default=None, description="展位号")
    booth_fee: Optional[float] = Field(default=None, description="展位费用")
    is_paid: bool = Field(default=False, description="是否已支付")
    payment_time: Optional[datetime] = Field(default=None, description="支付时间")
    registration_status: str = Field(default="pending", description="报名状态")
    registration_time: Optional[datetime] = Field(default=None, description="报名时间")
    approval_time: Optional[datetime] = Field(default=None, description="审核时间")
    approval_by: Optional[int] = Field(default=None, description="审核人ID")
    approval_comment: Optional[str] = Field(default=None, description="审核意见")
    materials_submitted: Optional[list] = Field(default=None, description="已提交材料")
    materials_required: Optional[list] = Field(default=None, description="需要材料")


class RegistrationQuerySchema(BaseSchema):
    """报名查询参数"""

    consultation_id: int | None = Field(default=None, description="咨询会ID")
    university_id: int | None = Field(default=None, description="高校ID")
    university_name: str | None = Field(default=None, description="高校名称")
    contact_person: str | None = Field(default=None, description="联系人")
    contact_phone: str | None = Field(default=None, description="联系电话")
    registration_status: str | None = Field(default=None, description="报名状态")
    start_date: list[DateTimeStr] | None = Field(default=None, description="报名时间范围")
    end_date: list[DateTimeStr] | None = Field(default=None, description="报名时间范围结束")


class RegistrationApproveSchema(BaseSchema):
    """审核通过模型"""

    booth_number: str | None = Field(default=None, description="展位号")
    booth_size: str | None = Field(default=None, description="展位大小")
    booth_fee: float | None = Field(default=None, description="展位费用")
    comment: str | None = Field(default=None, description="审核意见")


class RegistrationRejectSchema(BaseSchema):
    """审核拒绝模型"""

    comment: str = Field(..., description="拒绝原因")


class RegistrationPaySchema(BaseSchema):
    """支付确认模型"""

    payment_time: DateTimeStr = Field(..., description="支付时间")
    comment: str | None = Field(default=None, description="备注")
