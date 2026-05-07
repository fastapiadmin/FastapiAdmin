"""
全国高中学校库 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema


class SchoolLibraryCreateSchema(BaseModel):
    """新增学校库模型"""

    name: str = Field(..., description="学校名称", min_length=2, max_length=200)
    school_code: str | None = Field(default=None, description="学校编码", max_length=50)
    school_type: str | None = Field(default=None, description="学校类型", max_length=50)
    province: str | None = Field(default=None, description="省份", max_length=50)
    city: str | None = Field(default=None, description="城市", max_length=50)
    district: str | None = Field(default=None, description="区县", max_length=50)
    address: str | None = Field(default=None, description="地址", max_length=500)
    contact_phone: str | None = Field(default=None, description="联系电话", max_length=20)
    student_scale: int | None = Field(default=None, description="学生规模")
    is_key_school: str | None = Field(default=None, description="是否重点校")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """验证学校名称"""
        v = v.strip()
        if not v:
            raise ValueError("学校名称不能为空")
        return v


class SchoolLibraryUpdateSchema(SchoolLibraryCreateSchema):
    """更新学校库模型"""

    pass


class SchoolLibraryOutSchema(SchoolLibraryCreateSchema, BaseSchema, UserBySchema):
    """学校库响应模型"""

    model_config = ConfigDict(from_attributes=True)

    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class SchoolLibraryQuerySchema(BaseModel):
    """学校库查询参数模型"""

    def __init__(
        self,
        name: str | None = Query(None, description="学校名称"),
        school_type: str | None = Query(None, description="学校类型"),
        province: str | None = Query(None, description="省份"),
        city: str | None = Query(None, description="城市"),
        is_key_school: str | None = Query(None, description="是否重点校"),
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
        if is_key_school:
            self.is_key_school = (QueueEnum.eq.value, is_key_school)
