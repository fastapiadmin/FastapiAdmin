"""
行程方案管理 - 数据模型
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


class ItineraryModel(ModelMixin, UserMixin):
    """
    行程方案表
    
    存储生成的咨询会行程方案
    """
    
    __tablename__: str = "consultation_itinerary"
    __table_args__: dict[str, str] = {"comment": "行程方案表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]
    
    # 基本信息
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="行程方案名称")
    description: Mapped[Optional[str]] = mapped_column(Text, comment="行程方案描述")
    
    # 关联信息
    university_id: Mapped[Optional[int]] = mapped_column(BIGINT, comment="高校ID")
    team_id: Mapped[Optional[int]] = mapped_column(BIGINT, comment="招生组ID")
    
    # 时间信息
    start_date: Mapped[date] = mapped_column(Date, nullable=False, comment="开始日期")
    end_date: Mapped[date] = mapped_column(Date, nullable=False, comment="结束日期")
    
    # 行程详情
    consultation_ids: Mapped[Optional[list]] = mapped_column(JSON, comment="咨询会ID列表")
    consultation_details: Mapped[Optional[list]] = mapped_column(JSON, comment="咨询会详情列表")
    
    # 交通信息
    transportation_plan: Mapped[Optional[list]] = mapped_column(JSON, comment="交通方案列表")
    
    # 住宿信息
    accommodation_plan: Mapped[Optional[list]] = mapped_column(JSON, comment="住宿方案列表")
    
    # 优化信息
    total_distance: Mapped[Optional[float]] = mapped_column(Float, comment="总距离(公里)")
    estimated_duration: Mapped[Optional[int]] = mapped_column(Integer, comment="预计总时长(小时)")
    estimated_cost: Mapped[Optional[float]] = mapped_column(Float, comment="预计总费用")
    
    # 状态
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False, comment="状态(draft/confirmed/executed/archived)")
    is_synced: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否已同步到日历")
