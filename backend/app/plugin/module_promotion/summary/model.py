"""
总结上传 - 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BIGINT, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SummaryStatus(str, Enum):
    """总结状态枚举"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class PromotionSummaryModel(ModelMixin, UserMixin):
    """
    总结上传表

    存储招生宣传活动中的活动总结信息
    """

    __tablename__: str = "promotion_summary"
    __table_args__: dict[str, str] = {"comment": "总结上传表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    activity_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="活动ID"
    )

    summary_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="总结类型"
    )

    title: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="标题"
    )

    content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="内容"
    )

    photo_urls: Mapped[Optional[JSON]] = mapped_column(
        JSON,
        nullable=True,
        comment="照片URLs"
    )

    attachment_urls: Mapped[Optional[JSON]] = mapped_column(
        JSON,
        nullable=True,
        comment="附件URLs"
    )

    upload_by: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="上传人ID"
    )

    upload_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="上传时间"
    )

    is_archived: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="是否已归档"
    )
