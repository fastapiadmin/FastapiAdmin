# -*- coding: utf-8 -*-

from typing import Optional, List
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from urllib.parse import urlparse

from app.core.validator import DateTimeStr, mobile_validator
from app.core.base_schema import BaseSchema, CommonSchema, UserBySchema, TenantSchema, CustomerSchema
from app.core.validator import DateTimeStr
from app.api.v1.module_system.role.schema import RoleOutSchema


class CurrentUserUpdateSchema(BaseModel):
    """基础用户信息"""
    name: Optional[str] = Field(default=None, max_length=32, description="名称")
    mobile: Optional[str] = Field(default=None, description="手机号")
    email: Optional[EmailStr] = Field(default=None, description="邮箱")
    gender: Optional[str] = Field(default=None, description="性别")
    avatar: Optional[str] = Field(default=None, description="头像")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: Optional[str]):
        return mobile_validator(value)

    @field_validator("avatar")
    @classmethod
    def validate_avatar(cls, value: Optional[str]):
        if not value:
            return value
        parsed = urlparse(value)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return value
        raise ValueError("头像地址需为有效的HTTP/HTTPS URL")


class UserRegisterSchema(BaseModel):
    """注册"""
    name: Optional[str] = Field(default=None, max_length=32, description="名称")
    mobile: Optional[str] = Field(default=None, description="手机号")
    username: str = Field(..., max_length=32, description="账号")
    password: str = Field(..., max_length=128, description="密码哈希值")
    role_ids: Optional[List[int]] = Field(default=[1], description='角色ID')
    created_id: Optional[int] = Field(default=1, description='创建人ID')
    description: Optional[str] = Field(default=None, max_length=255, description="备注")
    user_type: Optional[str] = Field(default="0", max_length=32, description="用户类型")
    
    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: Optional[str]):
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
    mobile: Optional[str] = Field(default=None, description="手机号")
    
    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: Optional[str]):
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
    
    username: Optional[str] = Field(default=None, max_length=32, description="用户名")
    password: Optional[str] = Field(default=None, max_length=128, description="密码哈希值")
    status: str = Field(default=True, description="是否可用")
    description: Optional[str] = Field(default=None, max_length=255, description="备注")
    user_type: Optional[str] = Field(default="0", max_length=32, description="用户类型")
    
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    role_ids: Optional[List[int]] = Field(default=[], description='角色ID')
    position_ids: Optional[List[int]] = Field(default=[], description='岗位ID')


class UserUpdateSchema(UserCreateSchema):
    """更新"""
    model_config = ConfigDict(from_attributes=True)

    last_login: Optional[DateTimeStr] = Field(default=None, description="最后登录时间")


class UserOutSchema(UserUpdateSchema, BaseSchema, UserBySchema, TenantSchema, CustomerSchema):
    """响应"""
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    is_superuser: bool = Field(default=False, description="是否超管")
    gitee_login: Optional[str] = Field(default=None, max_length=32, description="Gitee登录")
    github_login: Optional[str] = Field(default=None, max_length=32, description="Github登录")
    wx_login: Optional[str] = Field(default=None, max_length=32, description="微信登录")
    qq_login: Optional[str] = Field(default=None, max_length=32, description="QQ登录")
    user_type: Optional[str] = Field(default="0", max_length=32, description="用户类型")
    salt: Optional[str] = Field(default=None, max_length=255, description="加密盐")
    dept_name: Optional[str] = Field(default=None, description='部门名称')
    dept: Optional[CommonSchema] = Field(default=None, description='部门')
    roles: Optional[List[RoleOutSchema]] = Field(default=[], description='角色')
    positions: Optional[List[CommonSchema]] = Field(default=[], description='岗位')


class UserQueryParam:
    """用户管理查询参数"""

    def __init__(
        self,
        username: Optional[str] = Query(None, description="用户名"),
        name: Optional[str] = Query(None, description="名称"),
        mobile: Optional[str] = Query(None, description="手机号", pattern=r'^1[3-9]\d{9}$'),
        email: Optional[str] = Query(None, description="邮箱", pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'), 
        dept_id: Optional[int] = Query(None, description="部门ID"),
        status: Optional[str] = Query(None, description="是否可用"),
        created_time: Optional[list[DateTimeStr]] = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        created_id: Optional[int] = Query(None, description="创建人"),
    ) -> None:
        
        # 模糊查询字段
        self.username = ("like", username)
        self.name = ("like", name)
        self.mobile = ("like", mobile)
        self.email = ("like", email)

        # 精确查询字段
        self.dept_id = dept_id
        self.created_id = created_id
        self.status = status
        
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
