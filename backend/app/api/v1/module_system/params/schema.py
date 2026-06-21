import re
from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam, TenantByQueryParam, UserByQueryParam
from app.core.base_schema import BaseSchema, TenantBySchema, UserBySchema


class ParamsCreateSchema(BaseModel):
    """
    参数创建模型
    """

    config_name: str = Field(..., min_length=1, max_length=64, description="参数名称")
    config_key: str = Field(..., min_length=1, max_length=500, description="参数键名（小写字母开头，仅允许字母数字_.-）")
    config_value: str | None = Field(default=None, max_length=500, description="参数键值")
    config_type: bool = Field(default=False, description="是否系统内置(True:是 False:否)")
    status: int = Field(default=0, ge=0, le=1, description="状态(0:正常 1:停用)")
    description: str | None = Field(default=None, max_length=500, description="参数描述")

    @field_validator("config_key")
    @classmethod
    def _validate_config_key(cls, v: str) -> str:
        """校验参数键名：小写字母开头，仅含字母/数字/_ . -"""
        v = v.strip().lower()
        if not re.match(r"^[a-z][a-z0-9_.-]*$", v):
            raise ValueError("参数键名必须以小写字母开头，仅允许小写字母、数字、_ . -")
        return v

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int) -> int:
        """校验状态：仅支持 0(正常) 或 1(停用)"""
        if v not in {0, 1}:
            raise ValueError("状态仅支持 0(正常) 或 1(停用)")
        return v


class ParamsUpdateSchema(ParamsCreateSchema):
    """
    参数更新模型
    """


class ParamsOutSchema(ParamsCreateSchema, BaseSchema, UserBySchema, TenantBySchema):
    """
    参数响应模型
    """

    model_config = ConfigDict(from_attributes=True)


@dataclass
class ParamsQueryParam(BaseQueryParam, UserByQueryParam, TenantByQueryParam):
    """
    参数管理查询参数

    支持：
    - 时间范围（BaseQueryParam）
    - 创建人/更新人筛选（UserByQueryParam）
    - 租户筛选（TenantByQueryParam）
    - 业务字段：参数名称、参数键名、是否系统内置
    """

    config_name: str | None = Query(None, description="参数名称")
    config_key: str | None = Query(None, description="参数键名")
    config_type: bool | None = Query(None, description="是否系统内置(True:是 False:否)")

    def __post_init__(self) -> None:
        if self.config_name:
            self.config_name = (QueueEnum.like.value, self.config_name)
        if self.config_key:
            self.config_key = (QueueEnum.like.value, self.config_key)
        if self.config_type is not None:
            self.config_type = (QueueEnum.eq.value, self.config_type)
