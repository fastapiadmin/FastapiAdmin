from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam
from app.core.base_schema import BaseSchema


class PackageCreateSchema(BaseModel):
    """新增套餐"""

    name: str = Field(..., min_length=1, max_length=100, description="套餐名称")
    code: str = Field(..., min_length=2, max_length=100, description="套餐编码")
    status: int = Field(default=0, ge=0, le=1, description="状态(0:启动 1:停用)")
    description: str | None = Field(default=None, max_length=255, description="描述")
    sort: int = Field(default=0, ge=0, description="排序")
    price: int = Field(default=0, ge=0, description="价格(分)")
    period: str = Field(default="month", pattern=r"^(month|year)$", description="计费周期")
    trial_days: int = Field(default=0, ge=0, description="免费试用天数")
    max_users: int = Field(default=10, ge=0, description="最大用户数")
    max_roles: int = Field(default=5, ge=0, description="最大角色数")
    max_depts: int = Field(default=10, ge=0, description="最大部门数")
    max_storage_mb: int = Field(default=1024, ge=0, description="最大存储(MB)")
    rate_limit: int = Field(default=60, ge=10, description="API速率限制(请求/10秒)")

    @field_validator("name")
    @classmethod
    def _validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("套餐名称不能为空")
        return v

    @field_validator("code")
    @classmethod
    def _validate_code(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("套餐编码不能为空")
        if not v.isalnum():
            raise ValueError("套餐编码仅允许字母和数字")
        return v

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int) -> int:
        if v not in {0, 1}:
            raise ValueError("状态仅支持 0(正常) 或 1(禁用)")
        return v


class PackageUpdateSchema(PackageCreateSchema):
    """更新套餐"""

    name: str | None = Field(default=None, max_length=100, description="套餐名称")  # type: ignore[assignment]
    code: str | None = Field(default=None, max_length=100, description="套餐编码")  # type: ignore[assignment]
    status: int | None = Field(default=None, ge=0, le=1, description="状态(0:启动 1:停用)")
    sort: int | None = Field(default=None, ge=0, description="排序")
    description: str | None = Field(default=None, max_length=255, description="描述")
    price: int | None = Field(default=None, ge=0, description="价格(分)")
    period: str | None = Field(default=None, pattern=r"^(month|year)$", description="计费周期")
    trial_days: int | None = Field(default=None, ge=0, description="免费试用天数")
    max_users: int | None = Field(default=None, ge=0, description="最大用户数")
    max_roles: int | None = Field(default=None, ge=0, description="最大角色数")
    max_depts: int | None = Field(default=None, ge=0, description="最大部门数")
    max_storage_mb: int | None = Field(default=None, ge=0, description="最大存储(MB)")
    rate_limit: int | None = Field(default=None, ge=10, description="API速率限制(请求/10秒)")

    @field_validator("code")
    @classmethod
    def _validate_code(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v.isalnum():
            raise ValueError("套餐编码仅允许字母和数字")
        return v

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int | None) -> int | None:
        if v is None:
            return v
        if v not in {0, 1}:
            raise ValueError("状态仅支持 0(正常) 或 1(禁用)")
        return v


class PackageOutSchema(PackageCreateSchema, BaseSchema):
    """套餐响应"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class PackageQueryParam(BaseQueryParam):
    """套餐查询参数"""

    name: str | None = Query(None, description="套餐名称")
    code: str | None = Query(None, description="套餐编码")

    def __post_init__(self) -> None:
        if self.name:
            self.name = (QueueEnum.like.value, self.name)
        if self.code:
            self.code = (QueueEnum.like.value, self.code)


class PackageMenuSetSchema(BaseModel):
    """批量设置套餐菜单权限"""

    menu_ids: list[int] = Field(..., description="菜单ID列表")


class PackagePluginSetSchema(BaseModel):
    """批量设置套餐插件"""

    plugin_ids: list[int] = Field(..., description="插件ID列表")
