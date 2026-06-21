from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam, TenantByQueryParam, UserByQueryParam
from app.core.base_schema import BaseSchema, TenantBySchema, UserBySchema


class PositionCreateSchema(BaseModel):
    """岗位创建模型"""

    name: str = Field(..., min_length=1, max_length=64, description="岗位名称")
    code: str = Field(..., min_length=1, max_length=64, description="岗位编码")
    order: int = Field(default=1, ge=0, description="显示排序")
    status: int = Field(default=0, ge=0, le=1, description="状态(0:启动 1:停用)")
    description: str | None = Field(default=None, max_length=255, description="描述")

    @field_validator("name")
    @classmethod
    def _validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("岗位名称不能为空")
        return v

    @field_validator("code")
    @classmethod
    def _validate_code(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("岗位编码不能为空")
        return v

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int) -> int:
        if v not in {0, 1}:
            raise ValueError("状态仅支持 0(正常) 或 1(禁用)")
        return v


class PositionUpdateSchema(PositionCreateSchema):
    """岗位更新模型"""


class PositionOutSchema(PositionCreateSchema, BaseSchema, UserBySchema, TenantBySchema):
    """岗位信息响应模型"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class PositionQueryParam(BaseQueryParam, UserByQueryParam, TenantByQueryParam):
    """岗位管理查询参数"""

    name: str | None = Query(None, description="岗位名称")

    def __post_init__(self) -> None:
        self.name = (QueueEnum.like.value, self.name)
