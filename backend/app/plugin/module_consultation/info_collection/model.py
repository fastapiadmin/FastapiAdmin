"""
咨询会信息聚合 - 数据模型
"""
from datetime import date, datetime, time
from enum import Enum
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
    Time,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class InfoSource(str, Enum):
    """信息来源枚举"""
    CRAWLER = "crawler"      # 全网抓取
    UPLOAD = "upload"        # 第三方上传
    MANUAL = "manual"        # 手动录入


class InfoStatus(str, Enum):
    """信息状态枚举"""
    PENDING = "pending"      # 待审核
    APPROVED = "approved"    # 已审核
    REJECTED = "rejected"    # 已拒绝
    EXPIRED = "expired"      # 已过期


class ConsultationInfoModel(ModelMixin, UserMixin):
    """
    咨询会信息表
    
    存储从全网抓取或第三方上传的招生咨询会信息
    """
    
    __tablename__: str = "consultation_info"
    __table_args__: dict[str, str] = {"comment": "咨询会信息表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]
    
    # 基本信息
    title: Mapped[str] = mapped_column(
        String(200), 
        nullable=False, 
        comment="咨询会标题"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True, 
        comment="咨询会描述"
    )
    
    # 主办方信息
    organizer: Mapped[str] = mapped_column(
        String(200), 
        nullable=False, 
        comment="主办方"
    )
    
    organizer_type: Mapped[Optional[str]] = mapped_column(
        String(50), 
        nullable=True, 
        comment="主办方类型(教育部门/高校/中学/机构)"
    )
    
    # 时间和地点
    start_date: Mapped[date] = mapped_column(
        Date, 
        nullable=False, 
        comment="开始日期"
    )
    
    end_date: Mapped[Optional[date]] = mapped_column(
        Date, 
        nullable=True, 
        comment="结束日期"
    )
    
    start_time: Mapped[Optional[str]] = mapped_column(
        String(10), 
        nullable=True, 
        comment="开始时间"
    )
    
    end_time: Mapped[Optional[str]] = mapped_column(
        String(10), 
        nullable=True, 
        comment="结束时间"
    )
    
    province: Mapped[Optional[str]] = mapped_column(
        String(50), 
        nullable=True, 
        comment="省份"
    )
    
    city: Mapped[Optional[str]] = mapped_column(
        String(50), 
        nullable=True, 
        comment="城市"
    )
    
    district: Mapped[Optional[str]] = mapped_column(
        String(50), 
        nullable=True, 
        comment="区县"
    )
    
    address: Mapped[Optional[str]] = mapped_column(
        String(500), 
        nullable=True, 
        comment="详细地址"
    )
    
    # 参与高校信息
    participating_universities: Mapped[Optional[list]] = mapped_column(
        JSON, 
        nullable=True, 
        comment="参与高校列表"
    )
    
    university_count: Mapped[int] = mapped_column(
        Integer, 
        default=0, 
        nullable=False, 
        comment="参与高校数量"
    )
    
    # 规模和费用
    estimated_visitors: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        comment="预计参观人数"
    )
    
    booth_fee: Mapped[Optional[float]] = mapped_column(
        Float, 
        nullable=True, 
        comment="展位费用"
    )
    
    # 来源和状态
    source_type: Mapped[str] = mapped_column(
        String(20), 
        default=InfoSource.CRAWLER.value, 
        nullable=False, 
        comment="信息来源(crawler/upload/manual)"
    )
    
    source_url: Mapped[Optional[str]] = mapped_column(
        String(1000), 
        nullable=True, 
        comment="来源链接"
    )
    
    status: Mapped[str] = mapped_column(
        String(20), 
        default=InfoStatus.PENDING.value, 
        nullable=False, 
        comment="状态(pending/approved/rejected/expired)"
    )
    
    review_comment: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True, 
        comment="审核意见"
    )
    
    reviewed_by: Mapped[Optional[int]] = mapped_column(
        BIGINT, 
        nullable=True, 
        comment="审核人ID"
    )
    
    reviewed_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True, 
        comment="审核时间"
    )
    
    # 合规评分
    compliance_score: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        comment="合规评分(0-100)"
    )
    
    compliance_level: Mapped[Optional[str]] = mapped_column(
        String(20), 
        nullable=True, 
        comment="合规等级(low/medium/high)"
    )
    
    risk_factors: Mapped[Optional[list]] = mapped_column(
        JSON, 
        nullable=True, 
        comment="风险因素列表"
    )
    
    # 归档信息
    is_archived: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False, 
        comment="是否归档"
    )
    
    archived_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True, 
        comment="归档时间"
    )
    
    archived_by: Mapped[Optional[int]] = mapped_column(
        BIGINT, 
        nullable=True, 
        comment="归档人ID"
    )
    
    # 搜索关键词（用于全文搜索）
    search_keywords: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True, 
        comment="搜索关键词"
    )
