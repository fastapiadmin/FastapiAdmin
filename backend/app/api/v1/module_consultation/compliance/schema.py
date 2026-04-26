"""
合规诊断 - 数据验证Schema
"""
from datetime import datetime

from pydantic import ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class ComplianceDiagnosisCreateSchema(BaseSchema):
    """新增诊断记录模型"""

    consultation_id: int = Field(..., description="咨询会ID")
    compliance_score: int = Field(..., ge=0, le=100, description="合规评分(0-100)")
    compliance_level: str = Field(..., description="合规等级(low/medium/high)")
    risk_factors: list[str] | None = Field(default=None, description="风险因素")
    diagnosis_details: dict | None = Field(default=None, description="诊断详情")
    improvement_suggestions: list[str] | None = Field(default=None, description="改进建议")
    is_high_risk: bool = Field(default=False, description="是否高风险")
    risk_warning: str | None = Field(default=None, description="风险警告")


class ComplianceDiagnosisUpdateSchema(ComplianceDiagnosisCreateSchema):
    """更新诊断记录模型"""
    pass


class ComplianceDiagnosisOutSchema(ComplianceDiagnosisCreateSchema, BaseSchema, UserBySchema):
    """诊断记录响应模型"""

    model_config = ConfigDict(from_attributes=True)

    diagnosis_time: datetime = Field(..., description="诊断时间")
    is_latest: bool = Field(default=True, description="是否最新诊断")


class ComplianceDiagnosisQuerySchema(BaseSchema):
    """诊断记录查询参数"""

    consultation_id: int | None = Field(default=None, description="咨询会ID")
    compliance_level: str | None = Field(default=None, description="合规等级")
    is_high_risk: bool | None = Field(default=None, description="是否高风险")
    start_date: list[DateTimeStr] | None = Field(default=None, description="诊断时间范围")
    end_date: list[DateTimeStr] | None = Field(default=None, description="诊断时间范围")


class ComplianceRuleCreateSchema(BaseSchema):
    """新增合规规则模型"""

    name: str = Field(..., description="规则名称", min_length=2, max_length=100)
    description: str | None = Field(default=None, description="规则描述")
    rule_type: str = Field(..., description="规则类型")
    rule_condition: dict = Field(..., description="规则条件")
    rule_weight: int = Field(default=10, ge=1, le=100, description="规则权重")
    risk_level: str = Field(..., description="风险等级(low/medium/high)")
    is_active: bool = Field(default=True, description="是否启用")
    order: int = Field(default=0, description="排序")


class ComplianceRuleUpdateSchema(ComplianceRuleCreateSchema):
    """更新合规规则模型"""
    pass


class ComplianceRuleOutSchema(ComplianceRuleCreateSchema, BaseSchema, UserBySchema):
    """合规规则响应模型"""

    model_config = ConfigDict(from_attributes=True)


class ComplianceRuleQuerySchema(BaseSchema):
    """合规规则查询参数"""

    name: str | None = Field(default=None, description="规则名称")
    rule_type: str | None = Field(default=None, description="规则类型")
    risk_level: str | None = Field(default=None, description="风险等级")
    is_active: bool | None = Field(default=None, description="是否启用")


class ComplianceCheckSchema(BaseSchema):
    """合规检查请求模型"""

    consultation_id: int = Field(..., description="咨询会ID")


class ComplianceCheckResultSchema(BaseSchema):
    """合规检查结果模型"""

    consultation_id: int = Field(..., description="咨询会ID")
    compliance_score: int = Field(..., description="合规评分")
    compliance_level: str = Field(..., description="合规等级")
    risk_factors: list[str] = Field(default_factory=list, description="风险因素")
    improvement_suggestions: list[str] = Field(default_factory=list, description="改进建议")
    is_high_risk: bool = Field(default=False, description="是否高风险")
    passed_rules: list[str] = Field(default_factory=list, description="通过的规则")
    failed_rules: list[str] = Field(default_factory=list, description="未通过的规则")
