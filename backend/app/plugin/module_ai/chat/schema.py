from dataclasses import dataclass
from typing import Any

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_params import BaseQueryParam, TenantByQueryParam, UserByQueryParam


class ChatQuerySchema(BaseModel):
    """WebSocket聊天查询模型"""

    message: str = Field(..., min_length=1, description="消息内容")
    session_id: str | None = Field(None, description="会话ID")
    files: list[dict[str, Any]] | None = Field(None, description="文件信息")


class ChatSessionCreateSchema(BaseModel):
    """创建会话模型"""

    title: str = Field(..., min_length=1, max_length=200, description="会话标题")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1 or len(v) > 200:
            raise ValueError("会话标题长度必须在1-200个字符之间")
        return v


class ChatSessionUpdateSchema(BaseModel):
    """更新会话模型"""

    title: str = Field(..., min_length=1, max_length=200, description="会话标题")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1 or len(v) > 200:
            raise ValueError("会话标题长度必须在1-200个字符之间")
        return v


class ChatSessionMessageSchema(BaseModel):
    """会话消息模型"""

    id: str = Field(..., description="消息ID")
    role: str = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")
    created_at: int | None = Field(None, description="创建时间(Unix时间戳)")

    model_config = ConfigDict(from_attributes=True)


@dataclass
class ChatSessionQueryParam(BaseQueryParam, UserByQueryParam, TenantByQueryParam):
    """会话查询参数"""

    title: str | None = Query(None, description="会话标题")


class AiChatRequestSchema(BaseModel):
    """AI 对话请求模型（非流式）"""

    message: str = Field(..., min_length=1, description="用户消息内容")
    session_id: str | None = Field(None, description="会话ID，不传则创建新会话")

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1:
            raise ValueError("用户消息内容不能为空")
        return v


class AiChatResponseSchema(BaseModel):
    """AI 对话响应模型（非流式）"""

    response: str = Field(..., description="AI 回复内容")
    session_id: str = Field(..., description="会话ID")
    function_calls: list[dict[str, Any]] | None = Field(None, description="函数调用信息")
    action: dict[str, Any] | None = Field(None, description="建议执行的操作")
