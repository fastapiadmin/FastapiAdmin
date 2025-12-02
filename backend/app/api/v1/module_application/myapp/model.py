# -*- coding: utf-8 -*-

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ApplicationModel(ModelMixin, UserMixin):
    """
    应用系统表
    """
    __tablename__: str = 'app_myapp'
    __table_args__: dict[str, str] = ({'comment': '应用系统表'})
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment='应用名称')
    access_url: Mapped[str] = mapped_column(String(500), nullable=False, comment='访问地址')
    icon_url: Mapped[str | None] = mapped_column(String(300), nullable=True, comment='应用图标URL')
