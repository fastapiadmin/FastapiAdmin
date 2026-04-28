"""
活动撰写 - 数据模型
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import BIGINT, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class DocumentStatus(str, Enum):
    """文档状态枚举"""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class PromotionDocumentModel(ModelMixin, UserMixin):
    """
    活动撰写表

    存储招生宣传活动中的活动撰写信息
    """

    __tablename__: str = "promotion_document"
    __table_args__: dict[str, str] = {"comment": "活动撰写表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]
    __mapper_args__: dict[str, list[str]] = {"exclude_properties": ["description"]}

    document_no: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="文档编号")

    activity_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="活动ID")

    activity_name: Mapped[str | None] = mapped_column(
        String(200), nullable=True, comment="活动名称"
    )

    document_title: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="文档标题"
    )

    document_type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="文档类型")

    document_content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="文档内容")

    document_summary: Mapped[str | None] = mapped_column(Text, nullable=True, comment="文档摘要")

    keywords: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="关键词")

    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="封面图片")

    author_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="作者ID")

    author_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="作者姓名")

    team_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="团队ID")

    team_name: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="团队名称")

    document_status: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="文档状态"
    )

    publish_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="发布时间"
    )

    view_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="浏览次数")

    is_top: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="是否置顶")

    is_featured: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="是否精选")

    attachment_urls: Mapped[str | None] = mapped_column(Text, nullable=True, comment="附件URLs")

    attachment_names: Mapped[str | None] = mapped_column(Text, nullable=True, comment="附件名称")

    wechat_formatted_content: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="微信公众号格式化内容"
    )

    ai_generation_status: Mapped[str | None] = mapped_column(
        String(20), default="pending", comment="AI生成状态(pending/generating/success/failed)"
    )

    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    display_order: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="显示排序")
