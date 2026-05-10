"""
咨询会信息聚合 - 数据模型
"""

from datetime import date, datetime
from enum import Enum

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


class InfoSource(str, Enum):
    """信息来源枚举"""

    CRAWLER = "crawler"  # 全网抓取
    UPLOAD = "upload"  # 第三方上传
    MANUAL = "manual"  # 手动录入
    HIGH_SCHOOL = "high_school"  # 高中录入
    UNIVERSITY = "university"  # 高校录入


class OrganizerNature(str, Enum):
    """主办机构性质枚举"""

    OFFICIAL_SINGLE = "official_single"  # 单一省、市、区级官方机构
    HIGH_SCHOOL_SINGLE = "high_school_single"  # 单一高中
    UNIVERSITY_SINGLE = "university_single"  # 单一高校
    THIRD_PARTY_SINGLE = "third_party_single"  # 单一第三方机构
    HIGH_SCHOOL_UNION = "high_school_union"  # 多所高中联合、无第三方机构
    HIGH_SCHOOL_UNION_WITH_THIRD = "high_school_union_with_third"  # 多所高中联合、有第三方机构
    THIRD_PARTY_MULTIPLE = "third_party_multiple"  # 多家第三方机构


class InfoStatus(str, Enum):
    """信息状态枚举"""

    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 已审核
    REJECTED = "rejected"  # 已拒绝
    EXPIRED = "expired"  # 已过期
    ARCHIVED = "archived"  # 已归档


class ConsultationInfoModel(ModelMixin, UserMixin):
    """
    咨询会信息表

    存储从全网抓取或第三方上传的招生咨询会信息
    """

    __tablename__: str = "consultation_info"
    __table_args__: dict[str, str] = {"comment": "咨询会信息表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 基本信息
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="咨询会标题")

    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="咨询会描述")

    # 主办方信息
    organizer: Mapped[str] = mapped_column(String(200), nullable=False, comment="主办方")

    organizer_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="主办方类型(教育部门/高校/中学/机构)"
    )

    organizer_nature: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="主办机构性质(用于合规评分)"
    )

    # 主办方详细信息
    organizer_detail: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="主办方详细信息(机构类型、级别等)"
    )

    has_third_party: Mapped[bool] = mapped_column(
        default=False, nullable=False, comment="是否有第三方机构参与"
    )

    third_party_info: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="第三方机构信息"
    )

    # 时间和地点
    start_date: Mapped[date] = mapped_column(Date, nullable=False, comment="开始日期")

    end_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="结束日期")

    start_time: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="开始时间")

    end_time: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="结束时间")

    province: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="省份")

    city: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="城市")

    district: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="区县")

    address: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="详细地址")

    longitude: Mapped[float | None] = mapped_column(Float, nullable=True, comment="经度")

    latitude: Mapped[float | None] = mapped_column(Float, nullable=True, comment="纬度")

    venue_name: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="场馆名称")

    # 参与高校信息
    participating_universities: Mapped[list | None] = mapped_column(
        JSON, nullable=True, comment="参与高校列表"
    )

    university_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="参与高校数量"
    )

    # 规模和费用
    estimated_visitors: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="预计参观人数"
    )

    booth_fee: Mapped[float | None] = mapped_column(Float, nullable=True, comment="展位费用")

    fee_description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="费用说明")

    co_organizers: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="协办方列表")

    # 来源和状态
    source_type: Mapped[str] = mapped_column(
        String(20),
        default=InfoSource.CRAWLER.value,
        nullable=False,
        comment="信息来源(crawler/upload/manual)",
    )

    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True, comment="来源链接")

    status: Mapped[str] = mapped_column(
        String(20),
        default=InfoStatus.PENDING.value,
        nullable=False,
        comment="状态(pending/approved/rejected/expired)",
    )

    review_comment: Mapped[str | None] = mapped_column(Text, nullable=True, comment="审核意见")

    reviewed_by: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="审核人ID")

    reviewed_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="审核时间"
    )

    # 合规评分
    compliance_score: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="合规评分(0-10)"
    )

    compliance_level: Mapped[str | None] = mapped_column(
        String(10), nullable=True, comment="合规等级(A/B/C/D)"
    )

    risk_factors: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="风险因素列表")

    # 报名信息
    registration_email: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="报名接收邮箱"
    )

    # 归档信息
    is_archived: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否归档"
    )

    archived_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="归档时间"
    )

    archived_by: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="归档人ID")

    # 去重信息
    is_duplicate: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否为重复记录"
    )

    duplicate_of_id: Mapped[int | None] = mapped_column(
        BIGINT, nullable=True, comment="关联的原始记录ID"
    )

    # 搜索关键词(用于模糊检索和去重)
    search_keywords: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="搜索关键词"
    )

    # 抓取来源信息
    crawl_url: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="抓取来源URL")

    crawl_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="抓取时间")

    external_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="外部系统ID(用于去重)"
    )
