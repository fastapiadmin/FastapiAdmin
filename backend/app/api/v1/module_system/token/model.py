# -*- coding: utf-8 -*-

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, TenantMixin, UserMixin


class TokenModel(ModelMixin, TenantMixin, UserMixin):
    """
    令牌表
    """
    __tablename__: str = 'sys_token'
    __table_args__: dict[str, str] = ({'comment': '令牌表'})
    __loader_options__: list[str] = ["created_by", "updated_by", "tenant"]

    name: Mapped[str | None] = mapped_column(String(64), nullable=True, default='', comment='名称')
