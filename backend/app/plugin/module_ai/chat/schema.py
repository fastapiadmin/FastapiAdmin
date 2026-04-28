from dataclasses import dataclass
from typing import Any

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.validator import DateTimeStr


class ChatQuerySchema(BaseModel):
    """WebSocket聊天查询模型"""

    message: str = Field(..., description="消息内容")
    session_id: str | None = Field(None, description="会话ID")
    files: list[dict[str, Any]] | None = Field(None, description="文件信息")


class ChatSessionCreateSchema(BaseModel):
    """创建会话模型"""

    title: str = Field(..., description="会话标题")


class ChatSessionUpdateSchema(BaseModel):
    """更新会话模型"""

    title: str = Field(..., description="会话标题")


class ChatSessionMessageSchema(BaseModel):
    """会话消息模型"""

    id: str = Field(..., description="消息ID")
    role: str = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")
    created_at: int | None = Field(None, description="创建时间(Unix时间戳)")

    model_config = ConfigDict(from_attributes=True)


@dataclass
class ChatSessionQueryParam:
    """会话查询参数"""

    def __init__(
        self,
        title: str | None = Query(None, description="会话标题"),
        created_at: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        updated_at: list[DateTimeStr] | None = Query(
            None,
            description="更新时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
    ) -> None:
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at


class AiChatRequestSchema(BaseModel):
    """AI 对话请求模型（非流式）"""

    message: str = Field(..., description="用户消息内容")
    session_id: str | None = Field(None, description="会话ID，不传则创建新会话")


class AiChatResponseSchema(BaseModel):
    """AI 对话响应模型（非流式）"""

    response: str = Field(..., description="AI 回复内容")
    session_id: str = Field(..., description="会话ID")
    function_calls: list[dict[str, Any]] | None = Field(None, description="函数调用信息")
    action: dict[str, Any] | None = Field(None, description="建议执行的操作")
