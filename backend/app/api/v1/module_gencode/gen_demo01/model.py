# -*- coding: utf-8 -*-

from sqlalchemy import Text, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class GenDemo01Model(ModelMixin, UserMixin):
    """
    示例表
    """
    __tablename__: str = 'gen_demo01'
    __table_args__: dict[str, str] = {'comment': '示例'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String, nullable=True, comment='名称')

