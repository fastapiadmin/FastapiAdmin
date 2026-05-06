"""
总结上传 - 数据模型
"""

from enum import Enum

from sqlalchemy import BIGINT, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SummaryStatus(str, Enum):
    """总结状态枚举，控制总结的提交和审批流程"""

    DRAFT = "draft"  # 草稿（可编辑）
    SUBMITTED = "submitted"  # 已提交（待审批）
    APPROVED = "approved"  # 已通过（不可删除）
    REJECTED = "rejected"  # 已拒绝（可编辑后重新提交）


class PromotionSummaryModel(ModelMixin, UserMixin):
    """
    总结上传表

    存储招生宣传活动中的活动总结信息
    """

    __tablename__: str = "promotion_summary"
    __table_args__: dict[str, str] = {"comment": "总结上传表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]
    __mapper_args__: dict[str, list[str]] = {
        "exclude_properties": ["description", "summary_status"]
    }

    activity_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="活动ID")

    summary_type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="总结类型")

    title: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="标题")

    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment="内容")

    photo_urls: Mapped[JSON | None] = mapped_column(JSON, nullable=True, comment="照片URLs")

    attachment_urls: Mapped[JSON | None] = mapped_column(JSON, nullable=True, comment="附件URLs")

    summary_status: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="总结状态"
    )
