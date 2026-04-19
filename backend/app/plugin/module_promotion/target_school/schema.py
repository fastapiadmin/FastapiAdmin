"""
目标学校管理 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class TargetSchoolCreateSchema(BaseModel):
    """新增目标学校模型"""

    school_name: str = Field(..., description="学校名称", min_length=2, max_length=200)
    school_code: str | None = Field(default=None, description="学校代码", max_length=50)
    school_type: str | None = Field(default=None, description="学校类型")

    province: str | None = Field(default=None, description="省份", max_length=50)
    city: str | None = Field(default=None, description="城市", max_length=50)
    district: str | None = Field(default=None, description="区县", max_length=50)
    address: str | None = Field(default=None, description="详细地址", max_length=500)

    team_id: int | None = Field(default=None, description="招生组ID")
    team_name: str | None = Field(default=None, description="招生组名称", max_length=200)

    personnel_id: int | None = Field(default=None, description="负责人ID")
    personnel_name: str | None = Field(default=None, description="负责人姓名", max_length=100)

    priority: str = Field(default="medium", description="优先级")
    follow_status: str = Field(default="new", description="跟进状态")

    student_count: int | None = Field(default=None, description="学生数量")
    graduate_count: int | None = Field(default=None, description="毕业生数量")
    admission_rate: float | None = Field(default=None, description="升学率")

    contact_person: str | None = Field(default=None, description="联系人", max_length=100)
    contact_phone: str | None = Field(default=None, description="联系电话", max_length=20)
    contact_title: str | None = Field(default=None, description="联系人职务", max_length=100)

    last_visit_date: DateStr | None = Field(default=None, description="最后走访日期")
    last_visit_content: str | None = Field(default=None, description="最后走访内容")
    next_visit_plan: str | None = Field(default=None, description="下次走访计划")
    next_visit_date: DateStr | None = Field(default=None, description="计划走访日期")
    visit_count: int = Field(default=0, description="走访次数")

    cooperation_start_date: DateStr | None = Field(default=None, description="合作开始日期")
    cooperation_end_date: DateStr | None = Field(default=None, description="合作结束日期")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")

    @field_validator("school_name")
    @classmethod
    def validate_school_name(cls, v: str) -> str:
        """验证学校名称"""
        v = v.strip()
        if not v:
            raise ValueError("学校名称不能为空")
        return v


class TargetSchoolUpdateSchema(TargetSchoolCreateSchema):
    """更新目标学校模型"""
    pass


class TargetSchoolOutSchema(TargetSchoolCreateSchema, BaseSchema, UserBySchema):
    """目标学校响应模型"""

    model_config = ConfigDict(from_attributes=True)

    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class TargetSchoolQuerySchema(BaseModel):
    """目标学校查询参数模型"""

    def __init__(
        self,
        school_name: str | None = Query(None, description="学校名称"),
        school_code: str | None = Query(None, description="学校代码"),
        school_type: str | None = Query(None, description="学校类型"),
        team_id: int | None = Query(None, description="招生组ID"),
        team_name: str | None = Query(None, description="招生组名称"),
        province: str | None = Query(None, description="省份"),
        city: str | None = Query(None, description="城市"),
        priority: str | None = Query(None, description="优先级"),
        follow_status: str | None = Query(None, description="跟进状态"),
        personnel_id: int | None = Query(None, description="负责人ID"),
        personnel_name: str | None = Query(None, description="负责人姓名"),
    ) -> None:
        from app.common.enums import QueueEnum

        if school_name:
            self.school_name = (QueueEnum.like.value, school_name)
        if school_code:
            self.school_code = (QueueEnum.eq.value, school_code)
        if school_type:
            self.school_type = (QueueEnum.eq.value, school_type)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if team_name:
            self.team_name = (QueueEnum.like.value, team_name)
        if province:
            self.province = (QueueEnum.eq.value, province)
        if city:
            self.city = (QueueEnum.eq.value, city)
        if priority:
            self.priority = (QueueEnum.eq.value, priority)
        if follow_status:
            self.follow_status = (QueueEnum.eq.value, follow_status)
        if personnel_id is not None:
            self.personnel_id = (QueueEnum.eq.value, personnel_id)
        if personnel_name:
            self.personnel_name = (QueueEnum.like.value, personnel_name)