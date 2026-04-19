"""
目标学校管理 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class TargetSchoolCreateSchema(BaseModel):
    """新增目标学校模型"""

    name: str = Field(..., description="学校名称", min_length=2, max_length=200)
    school_type: str | None = Field(default=None, description="学校类型")
    province: str | None = Field(default=None, description="省份")
    city: str | None = Field(default=None, description="城市")
    address: str | None = Field(default=None, description="地址")
    contact_person: str | None = Field(default=None, description="联系人")
    contact_phone: str | None = Field(default=None, description="联系电话")
    student_scale: int | None = Field(default=None, description="学生规模")
    intention_level: str | None = Field(default=None, description="意向级别")
    follow_status: str | None = Field(default=None, description="跟进状态")
    follow_person_id: int | None = Field(default=None, description="跟进人ID")
    last_follow_time: DateTimeStr | None = Field(default=None, description="最后跟进时间")
    remarks: str | None = Field(default=None, description="备注")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
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
        name: str | None = Query(None, description="学校名称"),
        school_type: str | None = Query(None, description="学校类型"),
        province: str | None = Query(None, description="省份"),
        city: str | None = Query(None, description="城市"),
        follow_status: str | None = Query(None, description="跟进状态"),
        follow_person_id: int | None = Query(None, description="跟进人ID"),
    ) -> None:
        from app.common.enums import QueueEnum

        if name:
            self.name = (QueueEnum.like.value, name)
        if school_type:
            self.school_type = (QueueEnum.eq.value, school_type)
        if province:
            self.province = (QueueEnum.eq.value, province)
        if city:
            self.city = (QueueEnum.eq.value, city)
        if follow_status:
            self.follow_status = (QueueEnum.eq.value, follow_status)
        if follow_person_id is not None:
            self.follow_person_id = (QueueEnum.eq.value, follow_person_id)
