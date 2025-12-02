# -*- coding: utf-8 -*-

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from urllib.parse import urlparse

from app.core.validator import DateTimeStr, mobile_validator
from app.core.base_schema import BaseSchema, CommonSchema, UserBySchema
from app.core.validator import DateTimeStr
from app.api.v1.module_system.menu.schema import MenuOutSchema
from app.api.v1.module_system.role.schema import RoleOutSchema


class CurrentUserUpdateSchema(BaseModel):
    """基础用户信息"""
    name: str | None = Field(default=None, max_length=32, description="名称")
    mobile: str | None = Field(default=None, description="手机号")
    email: EmailStr | None = Field(default=None, description="邮箱")
    gender: str | None = Field(default=None, description="性别")
    avatar: str | None = Field(default=None, description="头像")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str | None):
        return mobile_validator(value)

    @field_validator("avatar")
    @classmethod
    def validate_avatar(cls, value: str | None):
        if not value:
            return value
        parsed = urlparse(value)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return value
        raise ValueError("头像地址需为有效的HTTP/HTTPS URL")


class UserRegisterSchema(BaseModel):
    """注册"""
    name: str | None = Field(default=None, max_length=32, description="名称")
    mobile: str | None = Field(default=None, description="手机号")
    username: str = Field(..., max_length=32, description="账号")
    password: str = Field(..., max_length=128, description="密码哈希值")
    role_ids: list[int] | None = Field(default=[1], description='角色ID')
    created_id: int | None = Field(default=1, description='创建人ID')
    description: str | None = Field(default=None, max_length=255, description="备注")
    
    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str | None):
        return mobile_validator(value)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        v = value.strip()
        if not v:
            raise ValueError("账号不能为空")
        # 字母开头，允许字母数字_.-
        import re
        if not re.match(r"^[A-Za-z][A-Za-z0-9_.-]{2,31}$", v):
            raise ValueError("账号需字母开头，3-32位，仅含字母/数字/_ . -")
        return v


class UserForgetPasswordSchema(BaseModel):
    """忘记密码"""
    username: str = Field(..., max_length=32, description="用户名")
    new_password: str = Field(..., max_length=128, description="新密码")
    mobile: str | None = Field(default=None, description="手机号")
    
    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str | None):
        return mobile_validator(value)


class UserChangePasswordSchema(BaseModel):
    """修改密码"""
    old_password: str = Field(..., max_length=128, description="旧密码")
    new_password: str = Field(..., max_length=128, description="新密码")


class ResetPasswordSchema(BaseModel):
    """重置密码"""
    id: int = Field(..., description="主键ID")
    password: str = Field(..., min_length=6, max_length=128, description="新密码")


class UserCreateSchema(CurrentUserUpdateSchema):
    """新增"""
    model_config = ConfigDict(from_attributes=True)
    
    username: str | None = Field(default=None, max_length=32, description="用户名")
    password: str | None = Field(default=None, max_length=128, description="密码哈希值")
    status: str = Field(default="0", description="是否可用")
    description: str | None = Field(default=None, max_length=255, description="备注")
    is_superuser: bool | None = Field(default=False, description="是否超管")
    dept_id: int | None = Field(default=None, description='部门ID')
    role_ids: list[int] | None = Field(default=[], description='角色ID')
    position_ids: list[int] | None = Field(default=[], description='岗位ID')

class UserUpdateSchema(UserCreateSchema):
    """更新"""
    model_config = ConfigDict(from_attributes=True)

    last_login: DateTimeStr | None = Field(default=None, description="最后登录时间")


class UserOutSchema(UserUpdateSchema, BaseSchema, UserBySchema):
    """响应"""
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    gitee_login: str | None = Field(default=None, max_length=32, description="Gitee登录")
    github_login: str | None = Field(default=None, max_length=32, description="Github登录")
    wx_login: str | None = Field(default=None, max_length=32, description="微信登录")
    qq_login: str | None = Field(default=None, max_length=32, description="QQ登录")
    dept_name: str | None = Field(default=None, description='部门名称')
    dept: CommonSchema | None = Field(default=None, description='部门')
    positions: list[CommonSchema] | None = Field(default=[], description='岗位')
    roles: list[RoleOutSchema] | None = Field(default=[], description='角色')
    menus: list[MenuOutSchema] | None = Field(default=[], description='菜单')

class UserQueryParam:
    """用户管理查询参数"""

    def __init__(
        self,
        username: str | None = Query(None, description="用户名"),
        name: str | None = Query(None, description="名称"),
        mobile: str | None = Query(None, description="手机号", pattern=r'^1[3-9]\d{9}$'),
        email: str | None = Query(None, description="邮箱", pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'), 
        dept_id: int | None = Query(None, description="部门ID"),
        status: str | None = Query(None, description="是否可用"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:
        
        # 模糊查询字段
        self.username = ("like", username)
        self.name = ("like", name)
        self.mobile = ("like", mobile)
        self.email = ("like", email)

        # 精确查询字段
        self.dept_id = dept_id
        self.created_id = created_id
        self.updated_id = updated_id
        self.status = status
        
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
        