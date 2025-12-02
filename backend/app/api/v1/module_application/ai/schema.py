# -*- coding: utf-8 -*-

from pydantic import ConfigDict, Field, HttpUrl, BaseModel
from fastapi import Query

from app.core.base_schema import BaseSchema
from app.common.enums import McpLLMProvider
from app.core.base_schema import BaseSchema, UserBySchema
from app.common.enums import McpType
from app.core.validator import DateTimeStr


class ChatQuerySchema(BaseModel):
    """聊天查询模型"""
    message: str = Field(..., min_length=1, max_length=4000, description="聊天消息")


class McpCreateSchema(BaseModel):
    """创建 MCP 服务器参数"""
    name: str = Field(..., max_length=64, description='MCP 名称')
    type: McpType = Field(McpType.stdio, description='MCP 类型')
    description: str | None = Field(None, max_length=255, description='MCP 描述')
    url: HttpUrl | None = Field(None, description='远程 SSE 地址')
    command: str | None = Field(None, max_length=255, description='MCP 命令')
    args: str | None = Field(None, max_length=255, description='MCP 命令参数，多个参数用英文逗号隔开')
    env: dict[str, str] | None = Field(None, description='MCP 环境变量')


class McpUpdateSchema(McpCreateSchema):
    """更新 MCP 服务器参数"""
    ...


class McpOutSchema(McpCreateSchema, BaseSchema, UserBySchema):
    """MCP 服务器详情"""
    model_config = ConfigDict(from_attributes=True)


class McpQueryParam:
    """MCP 服务器查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="MCP 名称"),
        type: McpType | None = Query(None, description="MCP 类型"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:
        
        # 模糊查询字段
        self.name = ("like", name) if name else None

        # 精确查询字段
        self.type = type
        self.created_id = created_id
        self.updated_id = updated_id

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))


class McpChatParam(BaseSchema):
    """MCP 聊天参数"""
    pk: list[int] = Field(..., description='MCP ID 列表')
    provider: McpLLMProvider = Field(McpLLMProvider.openai, description='LLM 供应商')
    model: str = Field(..., description='LLM 名称')
    key: str = Field(..., description='LLM API Key')
    base_url: str | None = Field(None, description='自定义 LLM API 地址，必须兼容 openai 供应商')
    prompt: str = Field(..., description='用户提示词')