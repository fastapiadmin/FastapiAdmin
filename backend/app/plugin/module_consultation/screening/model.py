"""
咨询会筛选匹配 - 数据模型
"""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    BIGINT,
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
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
    
    # 基本信息
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="筛选名称")
    
    # 筛选条件
    province: Mapped[Optional[str]] = mapped_column(String(50), comment="省份筛选")
    city: Mapped[Optional[str]] = mapped_column(String(50), comment="城市筛选")
    start_date_begin: Mapped[Optional[date]] = mapped_column(Date, comment="开始日期范围-开始")
    start_date_end: Mapped[Optional[date]] = mapped_column(Date, comment="开始日期范围-结束")
    organizer_type: Mapped[Optional[str]] = mapped_column(String(50), comment="主办方类型")
    university_count_min: Mapped[Optional[int]] = mapped_column(Integer, comment="高校数量最小值")
    university_count_max: Mapped[Optional[int]] = mapped_column(Integer, comment="高校数量最大值")
    booth_fee_min: Mapped[Optional[float]] = mapped_column(Float, comment="展位费最小值")
    booth_fee_max: Mapped[Optional[float]] = mapped_column(Float, comment="展位费最大值")
    estimated_visitors_min: Mapped[Optional[int]] = mapped_column(Integer, comment="预计人数最小值")
    estimated_visitors_max: Mapped[Optional[int]] = mapped_column(Integer, comment="预计人数最大值")
    compliance_score_min: Mapped[Optional[int]] = mapped_column(Integer, comment="合规评分最小值")
    compliance_score_max: Mapped[Optional[int]] = mapped_column(Integer, comment="合规评分最大值")
    compliance_level: Mapped[Optional[str]] = mapped_column(String(20), comment="合规等级")
    source_type: Mapped[Optional[str]] = mapped_column(String(20), comment="信息来源")
    status: Mapped[Optional[str]] = mapped_column(String(20), comment="状态")
    
    # 排序和分页
    order_by: Mapped[Optional[str]] = mapped_column(String(50), comment="排序字段")
    order_direction: Mapped[Optional[str]] = mapped_column(String(10), comment="排序方向(asc/desc)")
    
    # 是否默认
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否默认筛选")
