from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ChatSessionModel(ModelMixin, UserMixin):
    """
    聊天会话表
    """

    __tablename__: str = "ai_chat_session"
    __table_args__: dict[str, str] = {"comment": "聊天会话表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="会话标题")
