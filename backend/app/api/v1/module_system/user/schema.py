from urllib.parse import urlparse

from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from app.api.v1.module_system.menu.schema import MenuOutSchema
from app.api.v1.module_system.role.schema import RoleOutSchema
from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema, CommonSchema, TenantBySchema, UserBySchema
from app.core.validator import DateTimeStr, email_validator, mobile_validator


class CurrentUserUpdateSchema(BaseModel):
    """基础用户信息"""

    name: str | None = Field(default=None, description="名称")
    mobile: str | None = Field(default=None, description="手机号")
    email: EmailStr | None = Field(default=None, description="邮箱")
    gender: str | None = Field(default=None, description="性别")
    avatar: str | None = Field(default=None, description="头像")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str | None):
        """
        校验手机号格式（委托到 `mobile_validator`）。

        参数:
        - value (str | None): 手机号。

        返回:
        - str | None: 校验后的手机号。

        异常:
        - CustomException: 手机号格式非法时抛出。
        """
        return mobile_validator(value)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None):
        """
        校验邮箱格式（为空则跳过；否则委托到 `email_validator`）。

        参数:
        - value (str | None): 邮箱。

        返回:
        - str | None: 校验后的邮箱。

        异常:
        - CustomException: 邮箱格式非法时抛出。
        """
        if not value:
            return value
        return email_validator(value)

    @field_validator("avatar")
    @classmethod
    def validate_avatar(cls, value: str | None):
        """
        校验头像地址为合法的 HTTP/HTTPS URL。

        参数:
        - value (str | None): 头像 URL。

        返回:
        - str | None: 校验后的头像 URL。

        异常:
        - ValueError: 头像 URL 非法时抛出。
        """
        if not value:
            return value
        parsed = urlparse(value)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return value
        raise ValueError("头像地址需为有效的HTTP/HTTPS URL")

    @model_validator(mode="after")
    def check_model(self):
        """
        校验基础用户信息的长度约束。

        返回:
        - CurrentUserUpdateSchema: 校验后的同一实例。

        异常:
        - ValueError: 字段长度超限时抛出。
        """
        if self.name and len(self.name) > 32:
            raise ValueError("名称长度不能超过32个字符")
        return self


class UserRegisterSchema(BaseModel):
    """注册"""

    name: str | None = Field(default=None, description="名称")
    mobile: str | None = Field(default=None, description="手机号")
    username: str = Field(..., description="账号")
    password: str = Field(..., description="密码哈希值")
    role_ids: list[int] | None = Field(default=[1], description="角色ID")
    created_id: int | None = Field(default=1, description="创建人ID")
    description: str | None = Field(default=None, max_length=255, description="备注")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str | None):
        """
        校验手机号格式（委托到 `mobile_validator`）。

        参数:
        - value (str | None): 手机号。

        返回:
        - str | None: 校验后的手机号。

        异常:
        - CustomException: 手机号格式非法时抛出。
        """
        return mobile_validator(value)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        """
        校验并规范化账号：字母开头，长度 3-32，仅含字母/数字/_ . -。

        参数:
        - value (str): 账号。

        返回:
        - str: 规范化后的账号。

        异常:
        - ValueError: 账号为空或不满足格式约束时抛出。
        """
        v = value.strip()
        if not v:
            raise ValueError("账号不能为空")
        # 字母开头，允许字母数字_.-
        import re

        if not re.match(r"^[A-Za-z][A-Za-z0-9_.-]{2,31}$", v):
            raise ValueError("账号需字母开头，3-32位，仅含字母/数字/_ . -")
        return v

    @model_validator(mode="after")
    def check_model(self):
        """
        校验注册信息的长度约束。

        返回:
        - UserRegisterSchema: 校验后的同一实例。

        异常:
        - ValueError: 任一字段长度超限时抛出。
        """
        if self.name and len(self.name) > 32:
            raise ValueError("名称长度不能超过32个字符")
        if self.username and len(self.username) > 32:
            raise ValueError("账号长度不能超过32个字符")
        if self.description and len(self.description) > 255:
            raise ValueError("备注长度不能超过255个字符")
        if self.password and len(self.password) > 128:
            raise ValueError("密码长度不能超过128个字符")
        return self


class UserForgetPasswordSchema(BaseModel):
    """忘记密码"""

    username: str = Field(..., max_length=32, description="用户名")
    new_password: str = Field(..., max_length=128, description="新密码")
    mobile: str | None = Field(default=None, description="手机号")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str | None):
        """
        校验手机号格式（委托到 `mobile_validator`）。

        参数:
        - value (str | None): 手机号。

        返回:
        - str | None: 校验后的手机号。

        异常:
        - CustomException: 手机号格式非法时抛出。
        """
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
    dept_id: int | None = Field(default=None, description="部门ID")
    tenant_id: int | None = Field(default=None, description="租户ID，仅平台管理员创建时可指定")
    role_ids: list[int] | None = Field(default=[], description="角色ID")
    position_ids: list[int] | None = Field(default=[], description="岗位ID")


class UserUpdateSchema(UserCreateSchema):
    """更新"""

    model_config = ConfigDict(from_attributes=True)

    last_login: DateTimeStr | None = Field(default=None, description="最后登录时间")


class UserOutSchema(UserUpdateSchema, BaseSchema, UserBySchema, TenantBySchema):
    """响应"""

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    tenant_id: int | None = Field(
        default=None,
        exclude=True,
        description="创建入参使用；列表/详情出参见 tenant",
    )
    gitee_login: str | None = Field(default=None, max_length=32, description="Gitee登录")
    github_login: str | None = Field(default=None, max_length=32, description="Github登录")
    wx_login: str | None = Field(default=None, max_length=32, description="微信登录")
    qq_login: str | None = Field(default=None, max_length=32, description="QQ登录")
    dept_name: str | None = Field(default=None, description="部门名称")
    dept: CommonSchema | None = Field(default=None, description="部门")
    positions: list[CommonSchema] | None = Field(default=[], description="岗位")
    roles: list[RoleOutSchema] | None = Field(default=[], description="角色")
    menus: list[MenuOutSchema] | None = Field(default=[], description="菜单")


class UserQueryParam:
    """用户管理查询参数"""

    def __init__(
        self,
        username: str | None = Query(None, description="用户名"),
        name: str | None = Query(None, description="名称"),
        mobile: str | None = Query(None, description="手机号", pattern=r"^1[3-9]\d{9}$"),
        email: str | None = Query(
            None,
            description="邮箱",
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        ),
        dept_id: int | None = Query(None, description="部门ID"),
        tenant_id: int | None = Query(None, description="租户ID（仅平台管理员可筛选）"),
        status: str | None = Query(None, description="是否可用"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        updated_time: list[DateTimeStr] | None = Query(
            None,
            description="更新时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:

        # 模糊查询字段
        self.username = (QueueEnum.like.value, username)
        self.name = (QueueEnum.like.value, name)
        self.mobile = (QueueEnum.like.value, mobile)
        self.email = (QueueEnum.like.value, email)

        # 精确查询字段
        self.dept_id = (QueueEnum.eq.value, dept_id)
        self.tenant_id = (QueueEnum.eq.value, tenant_id)
        self.created_id = (QueueEnum.eq.value, created_id)
        self.updated_id = (QueueEnum.eq.value, updated_id)
        self.status = (QueueEnum.eq.value, status)

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = (QueueEnum.between.value, (updated_time[0], updated_time[1]))
