from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema, UserBySchema


class ChatSessionCreateSchema(BaseModel):
    """新增聊天会话"""

    title: str = Field(..., description="会话标题")


class ChatSessionUpdateSchema(BaseModel):
    """更新聊天会话"""

    title: str | None = Field(None, description="会话标题")


class ChatSessionOutSchema(ChatSessionCreateSchema, BaseSchema, UserBySchema):
    """聊天会话响应模型"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class ChatSessionQueryParam:
    """聊天会话查询参数"""

    def __init__(
        self,
        title: str | None = Query(None, description="会话标题"),
        status: str | None = Query(None, description="是否启用"),
        created_time: list[str] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        updated_time: list[str] | None = Query(
            None,
            description="更新时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
    ) -> None:
        self.title = (QueueEnum.like.value, f"%{title}%") if title else None
        self.status = (QueueEnum.eq.value, status) if status else None

        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = (QueueEnum.between.value, (updated_time[0], updated_time[1]))
