import re

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class OperationLogCreateSchema(BaseModel):
    """日志创建模型"""

    type: int | None = Field(default=None, description="日志类型(1登录日志 2操作日志)")
    request_path: str | None = Field(default=None, description="请求路径")
    request_method: str | None = Field(default=None, description="请求方法")
    request_payload: str | None = Field(default=None, description="请求负载")
    request_ip: str | None = Field(default=None, description="请求 IP 地址")
    login_location: str | None = Field(default=None, description="登录位置")
    request_os: str | None = Field(default=None, description="请求操作系统")
    request_browser: str | None = Field(default=None, description="请求浏览器")
    response_code: int | None = Field(default=None, description="响应状态码")
    response_json: str | None = Field(default=None, description="响应 JSON 数据")
    process_time: str | None = Field(default=None, description="处理时间")
    status: str = Field(default="0", description="是否成功")
    description: str | None = Field(default=None, max_length=255, description="描述")
    created_id: int | None = Field(default=None, description="创建人ID")
    updated_id: int | None = Field(default=None, description="更新人ID")

    @field_validator("type")
    @classmethod
    def _validate_type(cls, value: int):
        if value is None:
            return value
        if value not in {1, 2}:
            raise ValueError("日志类型仅支持 1(登录) 或 2(操作)")
        return value

    @field_validator("request_method")
    @classmethod
    def _validate_method(cls, value: str):
        if value is None:
            return value
        allowed = {"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"}
        if value.upper() not in allowed:
            raise ValueError(f"请求方法必须为 {', '.join(sorted(allowed))}")
        return value.upper()

    @field_validator("request_ip")
    @classmethod
    def _validate_ip(cls, value: str | None):
        if value is None or value == "":
            return value
        ipv4 = r"^(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}$"
        ipv6 = r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$"
        if not re.match(ipv4, value) and not re.match(ipv6, value):
            raise ValueError("请求IP必须为有效的IPv4或IPv6地址")
        return value


class OperationLogOutSchema(OperationLogCreateSchema, BaseSchema, UserBySchema):
    """日志响应模型"""

    model_config = ConfigDict(from_attributes=True)


class OperationLogQueryParam:
    """操作日志查询参数"""

    def __init__(
        self,
        type: int | None = Query(None, description="日志类型(1:登录日志, 2:操作日志)"),
        request_path: str | None = Query(None, description="请求路径"),
        request_method: str | None = Query(None, description="请求方法"),
        request_ip: str | None = Query(None, description="请求IP"),
        response_code: int | None = Query(None, description="响应状态码"),
        description: str | None = Query(None, description="描述"),
        status: str | None = Query(None, description="是否启用"),
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
        self.request_path = ("like", f"%{request_path}%") if request_path else None
        # 精确查询字段
        self.request_method = request_method
        self.request_ip = request_ip
        self.response_code = response_code
        self.type = type
        # 模糊查询字段
        if description:
            self.description = ("like", description)

        # 精确查询字段
        if status:
            self.status = ("eq", status)

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))

        # 关联查询字段
        if created_id:
            self.created_id = ("eq", created_id)
        if updated_id:
            self.updated_id = ("eq", updated_id)
