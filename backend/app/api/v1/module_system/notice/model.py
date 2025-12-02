# -*- coding: utf-8 -*-

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class NoticeModel(ModelMixin, UserMixin):
    """
    通知公告表
    """
    __tablename__: str = "sys_notice"
    __table_args__: dict[str, str] = ({'comment': '通知公告表'})
    __loader_options__: list[str] = ["created_by", "updated_by"]

    notice_title: Mapped[str] = mapped_column(String(50), nullable=False, comment='公告标题')
    notice_type: Mapped[str] = mapped_column(String(50), nullable=False, comment='公告类型(1通知 2公告)')
    notice_content: Mapped[str | None] = mapped_column(Text, nullable=True, comment='公告内容')
