"""
咨询会筛选匹配 - 数据模型
"""

from datetime import date

from sqlalchemy import (
    Boolean,
    Date,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ScreeningFilterModel(ModelMixin, UserMixin):
    """
    咨询会筛选条件表

    存储用户保存的筛选条件
    """

    __tablename__: str = "consultation_screening_filter"
    __table_args__: dict[str, str] = {"comment": "咨询会筛选条件表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]
    __mapper_args__: dict[str, list[str]] = {
        "exclude_properties": ["description", "sort_by", "sort_order", "page_size", "is_default"]
    }

    # 基本信息
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="筛选名称")

    # 筛选条件
    province: Mapped[str | None] = mapped_column(String(50), comment="省份筛选")
    city: Mapped[str | None] = mapped_column(String(50), comment="城市筛选")
    start_date_begin: Mapped[date | None] = mapped_column(Date, comment="开始日期范围-开始")
    start_date_end: Mapped[date | None] = mapped_column(Date, comment="开始日期范围-结束")
    organizer_type: Mapped[str | None] = mapped_column(String(50), comment="主办方类型")
    university_count_min: Mapped[int | None] = mapped_column(Integer, comment="高校数量最小值")
    university_count_max: Mapped[int | None] = mapped_column(Integer, comment="高校数量最大值")
    booth_fee_min: Mapped[float | None] = mapped_column(Float, comment="展位费最小值")
    booth_fee_max: Mapped[float | None] = mapped_column(Float, comment="展位费最大值")
    estimated_visitors_min: Mapped[int | None] = mapped_column(Integer, comment="预计人数最小值")
    estimated_visitors_max: Mapped[int | None] = mapped_column(Integer, comment="预计人数最大值")
    compliance_score_min: Mapped[int | None] = mapped_column(Integer, comment="合规评分最小值")
    compliance_score_max: Mapped[int | None] = mapped_column(Integer, comment="合规评分最大值")
    compliance_level: Mapped[str | None] = mapped_column(String(20), comment="合规等级")
    source_type: Mapped[str | None] = mapped_column(String(20), comment="信息来源")
    status: Mapped[str | None] = mapped_column(String(20), comment="状态")

    # 排序和分页
    sort_by: Mapped[str] = mapped_column(
        String(50), default="start_date", nullable=False, comment="排序字段"
    )
    sort_order: Mapped[str] = mapped_column(
        String(10), default="desc", nullable=False, comment="排序方向"
    )
    page_size: Mapped[int] = mapped_column(Integer, default=20, nullable=False, comment="每页条数")

    # 默认筛选
    is_default: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否默认筛选"
    )


class ScreeningResultModel(ModelMixin, UserMixin):
    """
    咨询会筛选结果表

    存储筛选结果和匹配度
    """

    __tablename__: str = "consultation_screening_result"
    __table_args__: dict[str, str] = {"comment": "咨询会筛选结果表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 关联信息
    filter_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="筛选条件ID")
    consultation_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="咨询会ID")

    # 匹配度
    match_score: Mapped[float] = mapped_column(Float, nullable=False, comment="匹配度分数(0-100)")
    match_details: Mapped[str | None] = mapped_column(String(500), comment="匹配详情")

    # 用户操作
    is_favorite: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否收藏"
    )
    is_ignored: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否忽略"
    )
    notes: Mapped[str | None] = mapped_column(String(500), comment="备注")
