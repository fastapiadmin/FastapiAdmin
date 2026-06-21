from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.common.enums import QueueEnum, TicketTypeEnum
from app.core.base_params import BaseQueryParam, TenantByQueryParam, UserByQueryParam
from app.core.base_schema import BaseSchema, CommonSchema, TenantBySchema, UserBySchema


class TicketCreateSchema(BaseModel):
    """创建工单"""

    title: str = Field(..., min_length=1, max_length=200, description="工单标题")
    ticket_content: str = Field(default="", description="工单内容（富文本）")
    summary: str | None = Field(default=None, description="工单内容（纯文本摘要）")
    ticket_type: TicketTypeEnum = Field(default=TicketTypeEnum.SUGGESTION, description="工单类型(suggestion/bug/optimize/other)")
    images: str | None = Field(default=None, description="图片URL列表(JSON数组)")
    description: str | None = Field(default=None, max_length=255, description="工单描述")

    @field_validator("title")
    @classmethod
    def _validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("工单标题不能为空")
        return v


class TicketUpdateSchema(BaseModel):
    """更新工单"""

    title: str | None = Field(default=None, max_length=200, description="工单标题")
    ticket_content: str | None = Field(default=None, description="工单内容（富文本）")
    summary: str | None = Field(default=None, description="工单内容（纯文本摘要）")
    ticket_type: TicketTypeEnum | None = Field(default=None, description="工单类型")
    status: int | None = Field(default=None, ge=0, le=3, description="状态(0:待处理 1:处理中 2:已完成 3:已关闭)")
    reply: str | None = Field(default=None, description="回复内容")
    assigned_id: int | None = Field(default=None, gt=0, description="处理人ID")
    description: str | None = Field(default=None, max_length=255, description="工单描述")

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int | None) -> int | None:
        if v is None:
            return v
        if v not in {0, 1, 2, 3}:
            raise ValueError("工单状态仅支持 0(待处理)、1(处理中)、2(已完成)、3(已关闭)")
        return v


class TicketOutSchema(BaseSchema, UserBySchema, TenantBySchema):
    """工单响应"""

    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., description="工单标题")
    ticket_content: str | None = Field(default=None, description="工单内容")
    summary: str | None = Field(default=None, description="摘要")
    ticket_type: TicketTypeEnum = Field(..., description="工单类型")
    status: int = Field(..., description="状态(0:待处理 1:处理中 2:已完成 3:已关闭)")
    images: str | None = Field(default=None, description="图片")
    reply: str | None = Field(default=None, description="回复内容")
    assigned_id: int | None = Field(default=None, description="指派人ID")
    assigned_by: CommonSchema | None = Field(default=None, description="指派人")


class TicketBatchSchema(BaseModel):
    """批量更新工单"""

    ids: list[int] = Field(..., min_length=1, description="工单ID列表")
    status: int = Field(..., ge=0, le=3, description="状态(0:待处理 1:处理中 2:已完成 3:已关闭)")

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int) -> int:
        if v not in {0, 1, 2, 3}:
            raise ValueError("工单状态仅支持 0(待处理)、1(处理中)、2(已完成)、3(已关闭)")
        return v


@dataclass
class TicketQueryParam(BaseQueryParam, UserByQueryParam, TenantByQueryParam):
    """工单查询参数"""

    title: str | None = None
    ticket_type: str | None = None
    assigned_id: int | None = None

    def __post_init__(self) -> None:
        if self.title:
            self.title = (QueueEnum.like.value, self.title)
        if self.ticket_type:
            self.ticket_type = (QueueEnum.eq.value, self.ticket_type)
        if self.assigned_id:
            self.assigned_id = (QueueEnum.eq.value, self.assigned_id)
