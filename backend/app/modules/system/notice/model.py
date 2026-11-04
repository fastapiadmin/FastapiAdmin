from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class NoticeModel(ModelMixin, UserMixin):
    """通知公告表"""

    __tablename__: str = "sys_notice"
    __table_args__: dict[str, str] = {"comment": "通知公告表"}

    notice_title: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="公告标题")
    notice_type: Mapped[str] = mapped_column(String(1), nullable=False, index=True, comment="公告类型(1通知 2公告)")
    notice_content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="公告内容")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:草稿 1:已发布 2:已归档)")
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")


class NoticeReadModel(ModelMixin):
    """公告已读记录（用户 × 公告 唯一）

    公告是广播内容，本身没有“收件人”；「谁读过」是按人产生的事实，所以单独一张表。
    重复标记由 ``(user_id, notice_id)`` 唯一约束兜底，服务层先查后插，避免无谓报错。
    """

    __tablename__: str = "sys_notice_read"
    __table_args__ = (
        UniqueConstraint("user_id", "notice_id", name="uq_sys_notice_read_user_notice"),
        {"comment": "公告已读记录表"},
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID"
    )
    notice_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_notice.id", ondelete="CASCADE"), nullable=False, index=True, comment="公告ID"
    )
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="已读时间")
