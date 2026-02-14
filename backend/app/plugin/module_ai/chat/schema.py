from pydantic import BaseModel, Field


class ChatQuerySchema(BaseModel):
    """WebSocket聊天查询模型"""

    message: str = Field(..., description="消息内容")
    session_id: int | None = Field(None, description="会话ID")
    files: list[dict] | None = Field(None, description="文件信息")
