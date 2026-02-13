from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ChatSessionModel(ModelMixin, UserMixin):
    """
    聊天会话表
    """

    __tablename__: str = "app_ai_chat_session"
    __table_args__: dict[str, str] = {"comment": "聊天会话表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="会话标题")


class ChatMessageModel(ModelMixin):
    """
    聊天消息表
    """

    __tablename__: str = "app_ai_chat_message"
    __table_args__: dict[str, str] = {"comment": "聊天消息表"}

    session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("app_ai_chat_session.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
        comment="会话ID"
    )
    type: Mapped[str] = mapped_column(String(20), nullable=False, comment="消息类型: user/assistant")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="消息内容")
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, comment="时间戳")
    files: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="关联的文件信息")
