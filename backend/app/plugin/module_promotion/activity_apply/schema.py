"""
活动申请审批 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class ActivityApplyCreateSchema(BaseModel):
    """新增活动申请模型"""

    activity_name: str = Field(..., description="活动名称", min_length=2, max_length=200)
    activity_code: str | None = Field(default=None, description="活动编码", max_length=50)
    activity_type: str = Field(default="other", description="活动类型")

    team_id: int | None = Field(default=None, description="招生组ID")
    team_name: str | None = Field(default=None, description="招生组名称", max_length=200)

    applicant_id: int | None = Field(default=None, description="申请人ID")
    applicant_name: str | None = Field(default=None, description="申请人姓名", max_length=100)

    activity_start_date: DateStr = Field(..., description="活动开始日期")
    activity_end_date: DateStr | None = Field(default=None, description="活动结束日期")

    province: str | None = Field(default=None, description="省份", max_length=50)
    city: str | None = Field(default=None, description="城市", max_length=50)
    district: str | None = Field(default=None, description="区县", max_length=50)
    address: str | None = Field(default=None, description="详细地址", max_length=500)

    target_school_id: int | None = Field(default=None, description="目标学校ID")
    target_school_name: str | None = Field(default=None, description="目标学校名称", max_length=200)

    activity_content: str | None = Field(default=None, description="活动内容")
    expected_participants: int | None = Field(default=None, description="预计参与人数")

    budget: float | None = Field(default=None, description="预算金额")
    budget_usage: str | None = Field(default=None, description="预算用途")

    materials_needed: str | None = Field(default=None, description="所需物料")
    personnel_needed: int | None = Field(default=None, description="所需人员数")

    approval_level: int = Field(default=1, description="审批级别")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")

    @field_validator("activity_name")
    @classmethod
    def validate_activity_name(cls, v: str) -> str:
        """验证活动名称"""
        v = v.strip()
        if not v:
            raise ValueError("活动名称不能为空")
        return v

    @field_validator("activity_end_date")
    @classmethod
    def validate_end_date(cls, v, info):
        """验证结束日期"""
        if v and info.data.get("activity_start_date"):
            if v < info.data["activity_start_date"]:
                raise ValueError("结束日期不能早于开始日期")
        return v


class ActivityApplyUpdateSchema(ActivityApplyCreateSchema):
    """更新活动申请模型"""
    pass


class ActivityApplyOutSchema(ActivityApplyCreateSchema, BaseSchema, UserBySchema):
    """活动申请响应模型"""

    model_config = ConfigDict(from_attributes=True)

    approval_status: str | None = Field(default=None, description="审批状态")
    approval_comment: str | None = Field(default=None, description="审批意见")
    approval_by: int | None = Field(default=None, description="审批人ID")
    approval_by_name: str | None = Field(default=None, description="审批人姓名")
    approval_time: DateTimeStr | None = Field(default=None, description="审批时间")
    current_approval_level: int | None = Field(default=None, description="当前审批级别")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class ActivityApplyQuerySchema(BaseModel):
    """活动申请查询参数模型"""

    def __init__(
        self,
        activity_name: str | None = Query(None, description="活动名称"),
        activity_code: str | None = Query(None, description="活动编码"),
        activity_type: str | None = Query(None, description="活动类型"),
        team_id: int | None = Query(None, description="招生组ID"),
        team_name: str | None = Query(None, description="招生组名称"),
        applicant_id: int | None = Query(None, description="申请人ID"),
        applicant_name: str | None = Query(None, description="申请人姓名"),
        province: str | None = Query(None, description="省份"),
        city: str | None = Query(None, description="城市"),
        approval_status: str | None = Query(None, description="审批状态"),
        activity_start_date_begin: DateStr | None = Query(None, description="活动开始日期范围-开始"),
        activity_start_date_end: DateStr | None = Query(None, description="活动开始日期范围-结束"),
    ) -> None:
        from app.common.enums import QueueEnum

        if activity_name:
            self.activity_name = (QueueEnum.like.value, activity_name)
        if activity_code:
            self.activity_code = (QueueEnum.eq.value, activity_code)
        if activity_type:
            self.activity_type = (QueueEnum.eq.value, activity_type)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if team_name:
            self.team_name = (QueueEnum.like.value, team_name)
        if applicant_id is not None:
            self.applicant_id = (QueueEnum.eq.value, applicant_id)
        if applicant_name:
            self.applicant_name = (QueueEnum.like.value, applicant_name)
        if province:
            self.province = (QueueEnum.eq.value, province)
        if city:
            self.city = (QueueEnum.eq.value, city)
        if approval_status:
            self.approval_status = (QueueEnum.eq.value, approval_status)
        if activity_start_date_begin and activity_start_date_end:
            self.activity_start_date = (QueueEnum.between.value, (activity_start_date_begin, activity_start_date_end))