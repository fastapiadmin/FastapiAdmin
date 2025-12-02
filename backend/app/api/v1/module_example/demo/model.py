# -*- coding: utf-8 -*-

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class DemoModel(ModelMixin, UserMixin):
    """
    示例表
    """
    __tablename__: str = 'gen_demo'
    __table_args__: dict[str, str] = ({'comment': '示例表'})
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(64), nullable=True, default='', comment='名称')
