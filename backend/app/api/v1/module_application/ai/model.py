# -*- coding: utf-8 -*-

from sqlalchemy import JSON, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class McpModel(ModelMixin, UserMixin):
    """
    MCP 服务器表
    MCP类型:
    - 0: stdio (标准输入输出)
    - 1: sse (Server-Sent Events)
    """
    __tablename__: str = 'app_ai_mcp'
    __table_args__: dict[str, str] = ({'comment': 'MCP 服务器表'})
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(50), comment='MCP 名称')
    type: Mapped[int] = mapped_column(Integer, default=0, comment='MCP 类型(0:stdio 1:sse)')
    url: Mapped[str | None] = mapped_column(String(255), default=None, comment='远程 SSE 地址')
    command: Mapped[str | None] = mapped_column(String(255), default=None, comment='MCP 命令')
    args: Mapped[str | None] = mapped_column(String(255), default=None, comment='MCP 命令参数')
    env: Mapped[dict[str, str] | None] = mapped_column(JSON(), default=None, comment='MCP 环境变量')
