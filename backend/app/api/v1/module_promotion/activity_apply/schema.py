"""
活动申请审批 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class ActivityApplyCreateSchema(BaseModel):
    """新增活动申请模型"""

    activity_name: str = Field(..., description="活动名称", min_length=2, max_length=200)
    activity_type: str | None = Field(default=None, description="活动类型")
    team_id: int | None = Field(default=None, description="招生组ID")
    applicant_id: int | None = Field(default=None, description="申请人ID")
    target_school_id: int | None = Field(default=None, description="目标学校ID")
    plan_start_time: DateTimeStr | None = Field(default=None, description="计划开始时间")
    plan_end_time: DateTimeStr | None = Field(default=None, description="计划结束时间")
    plan_location: str | None = Field(default=None, description="计划地点")
    plan_content: str | None = Field(default=None, description="计划内容")
    expected_people: int | None = Field(default=None, description="预期人数")
    budget: float | None = Field(default=None, description="预算")
    approval_status: str | None = Field(default=None, description="审批状态")
    approval_comment: str | None = Field(default=None, description="审批意见")
    approval_time: DateTimeStr | None = Field(default=None, description="审批时间")
    approval_by: int | None = Field(default=None, description="审批人ID")

    @field_validator("activity_name")
    @classmethod
    def validate_activity_name(cls, v: str) -> str:
        """验证活动名称"""
        v = v.strip()
        if not v:
            raise ValueError("活动名称不能为空")
        return v


class ActivityApplyUpdateSchema(ActivityApplyCreateSchema):
    """更新活动申请模型"""

    pass


class ActivityApplyOutSchema(ActivityApplyCreateSchema, BaseSchema, UserBySchema):
    """活动申请响应模型"""

    model_config = ConfigDict(from_attributes=True)

    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class ActivityApplyQuerySchema(BaseModel):
    """活动申请查询参数模型"""

    def __init__(
        self,
        activity_name: str | None = Query(None, description="活动名称"),
        activity_type: str | None = Query(None, description="活动类型"),
        team_id: int | None = Query(None, description="招生组ID"),
        applicant_id: int | None = Query(None, description="申请人ID"),
        target_school_id: int | None = Query(None, description="目标学校ID"),
        approval_status: str | None = Query(None, description="审批状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if activity_name:
            self.activity_name = (QueueEnum.like.value, activity_name)
        if activity_type:
            self.activity_type = (QueueEnum.eq.value, activity_type)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if applicant_id is not None:
            self.applicant_id = (QueueEnum.eq.value, applicant_id)
        if target_school_id is not None:
            self.target_school_id = (QueueEnum.eq.value, target_school_id)
        if approval_status:
            self.approval_status = (QueueEnum.eq.value, approval_status)
