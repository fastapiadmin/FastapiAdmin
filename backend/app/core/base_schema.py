import json
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.validator import DateTimeStr


class CommonSchema(BaseModel):
    """通用信息模型"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="编号ID")
    name: str = Field(description="名称")
    status: int = Field(description="状态")


class BaseSchema(BaseModel):
    """通用输出模型，包含基础字段和审计字段"""

    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None, description="主键ID")
    uuid: str | None = Field(default=None, description="UUID")
    created_time: DateTimeStr | None = Field(default=None, description="创建时间")
    updated_time: DateTimeStr | None = Field(default=None, description="更新时间")
    is_deleted: bool = Field(default=False, description="是否已删除")
    deleted_time: DateTimeStr | None = Field(default=None, description="删除时间")


class UserBySchema(BaseModel):
    """通用创建模型，包含基础字段和审计字段"""

    model_config = ConfigDict(from_attributes=True)

    created_id: int | None = Field(default=None, description="创建人ID")
    created_by: CommonSchema | None = Field(default=None, description="创建人信息")
    updated_id: int | None = Field(default=None, description="更新人ID")
    updated_by: CommonSchema | None = Field(default=None, description="更新人信息")
    deleted_id: int | None = Field(default=None, description="删除人ID")
    deleted_by: CommonSchema | None = Field(default=None, description="删除人信息")


class BatchSetAvailable(BaseModel):
    """批量设置可用状态的请求模型"""

    ids: list[int] = Field(default_factory=list, description="ID列表")
    status: int = Field(default=0, ge=0, le=1, description="是否可用")


class UploadResponseSchema(BaseModel):
    """上传响应模型"""

    model_config = ConfigDict(from_attributes=True)

    file_path: str | None = Field(default=None, description="新文件映射路径")
    file_name: str | None = Field(default=None, description="新文件名称")
    origin_name: str | None = Field(default=None, description="原文件名称")
    file_url: str | None = Field(default=None, description="新文件访问地址")


class DownloadFileSchema(BaseModel):
    """下载文件模型"""

    file_path: str = Field(..., description="新文件映射路径")
    file_name: str = Field(..., description="新文件名称")


class SessionInfoSchema(BaseModel):
    """Redis 中存储的会话信息结构

    由 ``AuthService._assemble_session_dict`` 构造，存入 Redis 后被认证、
    在线用户等模块读取。``OnlineOutSchema`` 为此结构的公开子集。
    """

    session_id: str = Field(default="", description="会话ID（Redis key 后缀）")
    user_id: int | None = Field(default=None, description="用户ID")
    is_superuser: bool = Field(default=False, description="是否为超级管理员")
    user_status: int = Field(default=0, description="用户状态")
    name: str | None = Field(default=None, description="用户名称")
    user_name: str | None = Field(default=None, description="用户名")
    dept_id: int | None = Field(default=None, description="部门ID")
    mobile: str | None = Field(default=None, description="手机号")
    email: str | None = Field(default=None, description="邮箱")
    gender: str | None = Field(default=None, description="性别(0:男 1:女 2:未知)")
    avatar: str | None = Field(default=None, description="头像")
    permissions: list[str] = Field(default_factory=list, description="用户权限列表")
    menu_ids: list[int] = Field(default_factory=list, description="菜单ID列表")
    ipaddr: str | None = Field(default=None, description="登陆IP地址")
    login_location: str | None = Field(default=None, description="登录所属地")
    os: str | None = Field(default=None, description="操作系统")
    browser: str | None = Field(default=None, description="浏览器")
    login_time: DateTimeStr | None = Field(default=None, description="登录时间")
    login_type: str | None = Field(default=None, description="登录类型")


class JWTPayloadSchema(BaseModel):
    """JWT载荷模型"""

    sub: str = Field(..., description="用户登录信息")
    is_refresh: bool = Field(default=False, description="是否刷新token")
    exp: datetime | int = Field(..., description="过期时间")

    @model_validator(mode="after")
    def validate_fields(self):
        if not self.sub or len(self.sub.strip()) == 0:
            raise ValueError("会话编号不能为空")
        return self


class JWTOutSchema(BaseModel):
    """JWT响应模型"""

    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(..., min_length=1, description="访问token")
    refresh_token: str = Field(..., min_length=1, description="刷新token")
    token_type: str = Field(default="Bearer", description="token类型")
    expires_in: int = Field(..., gt=0, description="过期时间(秒)")


class PageResultSchema[T](BaseModel):
    """分页查询结果模型"""

    model_config = ConfigDict(from_attributes=True)

    page_no: int | None = Field(default=None, ge=1, description="页码，默认为1")
    page_size: int | None = Field(default=None, ge=1, description="页面大小，默认为10")
    total: int = Field(default=0, ge=0, description="总记录数")
    has_next: bool | None = Field(default=False, description="是否有下一页")
    items: list[T] = Field(default_factory=list, description="分页后的数据列表")


class PaginationQueryParam(BaseModel):
    """分页 —— order_by 以 JSON 字符串传递，避免 Depends() 模式下 list 字段被当 body 验证。"""

    page_no: int = Field(default=1, description="当前页码", ge=1)
    page_size: int = Field(default=10, description="每页数量", ge=1, le=100)
    order_by: Any = Field(
        default=None,
        description="排序字段 JSON 字符串, 格式:[{'field1': 'asc'}, {'field2': 'desc'}]",
    )

    @field_validator("order_by")
    @classmethod
    def validate_order_by(cls, v: Any) -> Any:
        """校验 order_by：None→默认升序，str→json.loads 转 list，list→直接返回，其他→抛异常。"""
        if v is None:
            return [{"id": "asc"}]
        if isinstance(v, str):
            try:
                result = json.loads(v)
                if not isinstance(result, list):
                    raise ValueError("order_by 必须是 JSON 数组字符串，例如 [{\"id\":\"asc\"}]")
                return result
            except json.JSONDecodeError:
                raise ValueError("order_by 字符串无法解析为 JSON，请传入有效的 JSON 数组字符串，例如 [{\"id\":\"asc\"}]")
        if isinstance(v, list):
            return v
        raise ValueError(f"order_by 类型无效: {type(v).__name__}，预期为 JSON 数组字符串或列表")


class BaseQueryParam(BaseModel):
    """created_time + updated_time —— 子类自动继承

    前端传数组格式 ``["start", "end"]``，``search_to_dict`` 自动转为 ``("between", [start, end])``。
    """

    created_time: list[DateTimeStr] | None = Field(None, description="创建时间范围")
    updated_time: list[DateTimeStr] | None = Field(None, description="更新时间范围")


class UserByQueryParam(BaseModel):
    """created_id + updated_id —— 子类自动继承"""

    created_id: int | None = Field(None, description="创建人", json_schema_extra={"q": "eq"})
    updated_id: int | None = Field(None, description="更新人", json_schema_extra={"q": "eq"})


class OptionSchema(BaseModel):
    """通用下拉选项 Schema，返回 [{value, label}]"""

    value: int
    label: str


class CoreUserSchema(BaseModel):
    """核心层用户信息 — AuthSchema 使用，不依赖任何业务模块

    业务模块的 UserOutSchema 应继承此类以确保类型兼容。
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(default=0, description="用户ID")
    username: str | None = Field(default=None, description="用户名")
    name: str | None = Field(default=None, description="名称")
    dept_id: int | None = Field(default=None, description="部门ID")
    is_superuser: bool = Field(default=False, description="是否超管")


class AuthSchema(BaseModel):
    """权限认证模型"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    user: CoreUserSchema = Field(default_factory=CoreUserSchema, description="用户信息", exclude=True)
    permissions: list[str] = Field(default_factory=list, description="用户权限标识列表")
    menu_ids: list[int] = Field(default_factory=list, description="角色授权的菜单ID列表")
