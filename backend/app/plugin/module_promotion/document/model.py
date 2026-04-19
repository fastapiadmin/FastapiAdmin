"""
活动撰写 - 数据模型
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    BIGINT,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class DocumentStatus(str, Enum):
    """文档状态枚举"""
    DRAFT = "draft"         # 草稿
    PUBLISHED = "published"   # 已发布
    ARCHIVED = "archived"     # 已归档


class DocumentType(str, Enum):
    """文档类型枚举"""
    NEWS = "news"           # 新闻
    ANNOUNCEMENT = "announcement"   # 公告
    ARTICLE = "article"     # 文章
    PROMOTION = "promotion" # 宣传稿
    REPORT = "report"       # 报告
    OTHER = "other"         # 其他


class PromotionDocumentModel(ModelMixin, UserMixin):
    """
    活动撰写表

    存储招生宣传活动中的活动撰写信息
    """

    __tablename__: str = "promotion_document"
    __table_args__: dict[str, str] = {"comment": "活动撰写表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 文档基本信息
    document_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="文档编号"
    )

    # 关联活动
    activity_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="关联活动ID"
    )

    activity_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="关联活动名称"
    )

    # 文档基本信息
    document_title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="文档标题"
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        default=DocumentType.OTHER.value,
        nullable=False,
        comment="文档类型(news/announcement/article/promotion/report/other)"
    )

    # 文档内容
    document_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="文档内容"
    )

    # 摘要
    document_summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="文档摘要"
    )

    # 关键词
    keywords: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="关键词"
    )

    # 封面图片
    cover_image: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="封面图片URL"
    )

    # 作者信息
    author_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="作者ID"
    )

    author_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="作者姓名"
    )

    # 招生组
    team_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        nullable=True,
        comment="招生组ID"
    )

    team_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="招生组名称"
    )

    # 文档状态
    document_status: Mapped[str] = mapped_column(
        String(20),
        default=DocumentStatus.DRAFT.value,
        nullable=False,
        comment="文档状态(draft/published/archived)"
    )

    # 发布时间
    publish_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="发布时间"
    )

    # 阅读量
    view_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="阅读量"
    )

    # 是否置顶
    is_top: Mapped[bool] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="是否置顶"
    )

    # 是否推荐
    is_featured: Mapped[bool] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="是否推荐"
    )

    # 附件
    attachment_urls: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="附件URL(JSON数组)"
    )

    attachment_names: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="附件名称(JSON数组)"
    )

    # 备注
    remark: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="备注"
    )

    # 排序
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="显示排序"
    )