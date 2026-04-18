"""
合规诊断 - 数据模型
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


class ComplianceDiagnosisModel(ModelMixin, UserMixin):
    """
    合规诊断记录表
    
    存储咨询会合规诊断结果
    """
    
    __tablename__: str = "consultation_compliance_diagnosis"
    __table_args__: dict[str, str] = {"comment": "合规诊断记录表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]
    
    # 关联信息
    consultation_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="咨询会ID")
    
    # 诊断信息
    diagnosis_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="诊断时间")
    
    # 合规评分
    compliance_score: Mapped[int] = mapped_column(Integer, nullable=False, comment="合规评分(0-100)")
    compliance_level: Mapped[str] = mapped_column(String(20), nullable=False, comment="合规等级(low/medium/high)")
    
    # 风险因素
    risk_factors: Mapped[Optional[list]] = mapped_column(JSON, comment="风险因素列表")
    
    # 诊断详情
    diagnosis_details: Mapped[Optional[dict]] = mapped_column(JSON, comment="诊断详情")
    
    # 改进建议
    improvement_suggestions: Mapped[Optional[list]] = mapped_column(JSON, comment="改进建议列表")
    
    # 诊断结果
    is_high_risk: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否高风险")
    risk_warning: Mapped[Optional[str]] = mapped_column(Text, comment="风险警告")
    
    # 历史记录
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="是否最新诊断")


class ComplianceRuleModel(ModelMixin, UserMixin):
    """
    合规规则表
    
    存储合规诊断规则
    """
    
    __tablename__: str = "consultation_compliance_rule"
    __table_args__: dict[str, str] = {"comment": "合规规则表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]
    
    # 规则信息
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="规则名称")
    description: Mapped[Optional[str]] = mapped_column(Text, comment="规则描述")
    
    # 规则配置
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="规则类型(organizer/location/scale/fee/other)")
    rule_condition: Mapped[dict] = mapped_column(JSON, nullable=False, comment="规则条件")
    rule_weight: Mapped[int] = mapped_column(Integer, default=10, nullable=False, comment="规则权重(1-100)")
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False, comment="风险等级(low/medium/high)")
    
    # 状态
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="是否启用")
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")
