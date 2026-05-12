"""
高校信息管理 - 数据验证Schema
"""

from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema


class UniversityBaseSchema(BaseSchema):
    """高校信息基础模型"""

    name: str = Field(..., description="高校名称", min_length=2, max_length=200)
    code: str | None = Field(default=None, description="高校代码", max_length=50)
    abbreviation: str | None = Field(default=None, description="高校简称", max_length=50)
    contact_person: str | None = Field(default=None, description="联系人", max_length=100)
    contact_phone: str | None = Field(default=None, description="联系电话", max_length=20)
    contact_email: str | None = Field(default=None, description="联系邮箱", max_length=100)
    province: str | None = Field(default=None, description="省份", max_length=50)
    city: str | None = Field(default=None, description="城市", max_length=50)
    address: str | None = Field(default=None, description="详细地址", max_length=500)
    description: str | None = Field(default=None, description="高校简介")
    website: str | None = Field(default=None, description="官网链接", max_length=200)
    status: str | None = Field(default="active", description="状态(active/inactive)")


class UniversityCreateSchema(UniversityBaseSchema):
    """新增高校模型"""

    pass


class UniversityUpdateSchema(UniversityBaseSchema):
    """更新高校模型"""

    pass


class UniversityOutSchema(UniversityBaseSchema, UserBySchema):
    """高校响应模型"""

    model_config = ConfigDict(from_attributes=True)


class UniversityQuerySchema(BaseSchema):
    """高校查询参数"""

    name: str | None = Field(default=None, description="高校名称")
    code: str | None = Field(default=None, description="高校代码")
    province: str | None = Field(default=None, description="省份")
    city: str | None = Field(default=None, description="城市")
    status: str | None = Field(default=None, description="状态")


class UniversitySimpleOutSchema(BaseModel):
    """高校简要信息（用于下拉选择）"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="高校ID")
    name: str = Field(..., description="高校名称")
    code: str | None = Field(default=None, description="高校代码")
