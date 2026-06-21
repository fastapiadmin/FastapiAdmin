from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam
from app.core.base_schema import BaseSchema
from app.core.validator import DateTimeStr, email_validator, mobile_validator


class TenantCreateSchema(BaseModel):
    """新增租户"""

    name: str = Field(..., min_length=1, max_length=100, description="租户名称")
    code: str = Field(..., min_length=2, max_length=100, description="租户编码")
    status: int = Field(default=0, ge=0, le=1, description="状态(0:启动 1:停用)")
    description: str | None = Field(default=None, description="描述")
    start_time: DateTimeStr | None = Field(default=None, description="开始时间")
    end_time: DateTimeStr | None = Field(default=None, description="结束时间")
    contact_name: str | None = Field(default=None, max_length=64, description="联系人姓名")
    contact_phone: str | None = Field(default=None, max_length=20, description="联系人电话")
    contact_email: str | None = Field(default=None, max_length=128, description="联系人邮箱")
    address: str | None = Field(default=None, max_length=255, description="地址")
    domain: str | None = Field(default=None, max_length=255, description="域名")
    logo_url: str | None = Field(default=None, max_length=500, description="Logo URL")
    sort: int = Field(default=0, ge=0, description="排序")
    package_id: int | None = Field(default=None, gt=0, description="关联套餐ID")
    version: str | None = Field(default=None, max_length=20, description="版本号")
    favicon: str | None = Field(default=None, max_length=500, description="favicon地址")
    login_bg: str | None = Field(default=None, max_length=500, description="登录背景地址")
    copyright: str | None = Field(default=None, max_length=255, description="版权信息")
    keep_record: str | None = Field(default=None, max_length=100, description="备案号")
    help_doc: str | None = Field(default=None, max_length=500, description="帮助文档地址")
    privacy: str | None = Field(default=None, max_length=500, description="隐私政策地址")
    clause: str | None = Field(default=None, max_length=500, description="服务条款地址")
    git_code: str | None = Field(default=None, max_length=500, description="源码地址")

    @field_validator("name")
    @classmethod
    def _validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("租户名称不能为空")
        return v

    @field_validator("code")
    @classmethod
    def _validate_code(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("租户编码不能为空")
        if not v.isalnum():
            raise ValueError("租户编码仅允许字母和数字")
        return v

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int) -> int:
        if v not in {0, 1}:
            raise ValueError("状态仅支持 0(正常) 或 1(禁用)")
        return v

    @field_validator("contact_phone")
    @classmethod
    def _validate_contact_phone(cls, v: str | None) -> str | None:
        return mobile_validator(v)

    @field_validator("contact_email")
    @classmethod
    def _validate_contact_email(cls, v: str | None) -> str | None:
        if not v:
            return v
        return email_validator(v)

    @model_validator(mode="after")
    def _validate_time_range(self):
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValueError("结束时间不能早于开始时间")
        return self


class TenantUpdateSchema(TenantCreateSchema):
    """更新租户"""

    name: str | None = Field(default=None, max_length=100, description="租户名称")  # type: ignore[assignment]
    code: str | None = Field(default=None, max_length=100, description="租户编码")  # type: ignore[assignment]
    status: int | None = Field(default=None, ge=0, le=1, description="状态(0:启动 1:停用)")
    description: str | None = Field(default=None, description="描述")
    start_time: DateTimeStr | None = Field(default=None, description="开始时间")
    end_time: DateTimeStr | None = Field(default=None, description="结束时间")
    contact_name: str | None = Field(default=None, max_length=64, description="联系人姓名")
    contact_phone: str | None = Field(default=None, max_length=20, description="联系人电话")
    contact_email: str | None = Field(default=None, max_length=128, description="联系人邮箱")
    address: str | None = Field(default=None, max_length=255, description="地址")
    domain: str | None = Field(default=None, max_length=255, description="域名")
    logo_url: str | None = Field(default=None, max_length=500, description="Logo URL")
    sort: int | None = Field(default=None, ge=0, description="排序")
    package_id: int | None = Field(default=None, gt=0, description="关联套餐ID")
    version: str | None = Field(default=None, max_length=20, description="版本号")
    favicon: str | None = Field(default=None, max_length=500, description="favicon地址")
    login_bg: str | None = Field(default=None, max_length=500, description="登录背景地址")
    copyright: str | None = Field(default=None, max_length=255, description="版权信息")
    keep_record: str | None = Field(default=None, max_length=100, description="备案号")
    help_doc: str | None = Field(default=None, max_length=500, description="帮助文档地址")
    privacy: str | None = Field(default=None, max_length=500, description="隐私政策地址")
    clause: str | None = Field(default=None, max_length=500, description="服务条款地址")
    git_code: str | None = Field(default=None, max_length=500, description="源码地址")

    @field_validator("code")
    @classmethod
    def _validate_code(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v.isalnum():
            raise ValueError("租户编码仅允许字母和数字")
        return v

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int | None) -> int | None:
        if v is None:
            return v
        if v not in {0, 1}:
            raise ValueError("状态仅支持 0(正常) 或 1(禁用)")
        return v

    @field_validator("contact_phone")
    @classmethod
    def _validate_contact_phone(cls, v: str | None) -> str | None:
        return mobile_validator(v)

    @field_validator("contact_email")
    @classmethod
    def _validate_contact_email(cls, v: str | None) -> str | None:
        if not v:
            return v
        return email_validator(v)

    @model_validator(mode="after")
    def _validate_time_range(self):
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValueError("结束时间不能早于开始时间")
        return self


class TenantOutSchema(TenantCreateSchema, BaseSchema):
    """租户响应"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class TenantQueryParam(BaseQueryParam):
    """租户查询参数"""

    name: str | None = Query(None, description="租户名称")
    code: str | None = Query(None, description="租户编码")

    def __post_init__(self) -> None:
        if self.name:
            self.name = (QueueEnum.like.value, self.name)
        if self.code:
            self.code = (QueueEnum.like.value, self.code)


class TenantUserAddSchema(BaseModel):
    """向租户添加用户"""

    user_id: int = Field(..., gt=0, description="用户ID")
    role: str = Field(default="member", max_length=20, description="租户内角色(owner/admin/member)")
    is_default: int = Field(default=0, ge=0, le=1, description="是否默认租户(0:否 1:是)")

    @field_validator("role")
    @classmethod
    def _validate_role(cls, v: str) -> str:
        if v not in {"owner", "admin", "member"}:
            raise ValueError("租户角色仅支持 owner(拥有者)、admin(管理员)、member(成员)")
        return v

    @field_validator("is_default")
    @classmethod
    def _validate_is_default(cls, v: int) -> int:
        if v not in {0, 1}:
            raise ValueError("是否默认仅支持 0(否) 或 1(是)")
        return v


class TenantUserOutSchema(BaseModel):
    """租户用户响应"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="关联ID")
    user_id: int = Field(..., description="用户ID")
    tenant_id: int = Field(..., description="租户ID")
    role: str = Field(..., description="租户内角色")
    is_default: int = Field(..., description="是否默认租户")
    create_time: DateTimeStr | None = Field(default=None, description="创建时间")
    username: str = Field(default="", description="用户名")
    name: str = Field(default="", description="用户姓名")


class TenantConfigItem(BaseModel):
    """租户配置项"""

    key: str = Field(..., description="配置键")
    value: str | None = Field(default=None, description="配置值")


class TenantConfigOutSchema(BaseModel):
    """租户配置响应"""

    model_config = ConfigDict(from_attributes=True)

    config_key: str = Field(..., description="配置键")
    config_value: str | None = Field(default=None, description="配置值")


class TenantRenewSchema(BaseModel):
    """租户续期"""

    end_time: DateTimeStr = Field(..., description="新的结束时间")

    @model_validator(mode="after")
    def _validate_end_time(self):
        from datetime import datetime

        if self.end_time <= datetime.now():
            raise ValueError("续期时间必须晚于当前时间")
        return self


class PackageChangePreviewOut(BaseModel):
    """套餐变更影响预览响应"""

    new_package_id: int = Field(..., description="新套餐ID")
    new_package_name: str = Field(default="", description="新套餐名称")
    affected_roles: list[dict] = Field(default_factory=list, description="受影响的角色列表（名称、用户数）")
    removed_menus: list[dict] = Field(default_factory=list, description="将被移除的菜单清单（名称、路径）")
    added_menus: list[dict] = Field(default_factory=list, description="新增的菜单清单（名称、路径）")
    quota_changes: dict = Field(default_factory=dict, description="配额变化对比")
    total_affected_users: int = Field(default=0, description="受影响用户数总计")
