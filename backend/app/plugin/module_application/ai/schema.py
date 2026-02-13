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


class ChatMessageCreateSchema(BaseModel):
    """新增聊天消息"""

    session_id: int = Field(..., description="会话ID")
    type: str = Field(..., description="消息类型: user/assistant")
    content: str = Field(..., description="消息内容")
    timestamp: int = Field(..., description="时间戳")
    files: list[dict] | None = Field(None, description="关联的文件信息")


class ChatMessageUpdateSchema(BaseModel):
    """更新聊天消息"""

    session_id: int | None = Field(None, description="会话ID")
    type: str | None = Field(None, description="消息类型: user/assistant")
    content: str | None = Field(None, description="消息内容")
    timestamp: int | None = Field(None, description="时间戳")
    files: list[dict] | None = Field(None, description="关联的文件信息")


class ChatMessageOutSchema(ChatMessageCreateSchema, BaseSchema):
    """聊天消息响应模型"""

    model_config = ConfigDict(from_attributes=True)


class ChatQuerySchema(BaseModel):
    """WebSocket聊天查询模型"""

    message: str = Field(..., description="消息内容")
    session_id: int | None = Field(None, description="会话ID")
    files: list[dict] | None = Field(None, description="文件信息")


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


@dataclass
class ChatMessageQueryParam:
    """聊天消息查询参数"""

    def __init__(
        self,
        session_id: int | None = Query(None, description="会话ID"),
        type: str | None = Query(None, description="消息类型"),
        content: str | None = Query(None, description="消息内容"),
        created_time: list[str] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
    ) -> None:
        self.session_id = (QueueEnum.eq.value, session_id) if session_id else None
        self.type = (QueueEnum.eq.value, type) if type else None
        self.content = (QueueEnum.like.value, f"%{content}%") if content else None

        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
