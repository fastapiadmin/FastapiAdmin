from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema
from app.core.validator import DateTimeStr


class TenantCreateSchema(BaseModel):
    """新增租户"""

    name: str = Field(..., max_length=100, description="租户名称")
    code: str = Field(..., max_length=100, description="租户编码")
    status: str = Field(default="0", description="状态(0:正常 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="描述")
    start_time: DateTimeStr | None = Field(default=None, description="开始时间")
    end_time: DateTimeStr | None = Field(default=None, description="结束时间")

    @field_validator("name")
    @classmethod
    def _validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("名称不能为空")
        return v

    @field_validator("code")
    @classmethod
    def _validate_code(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("编码不能为空")
        if not v.isalnum():
            raise ValueError("编码只能包含字母和数字")
        return v

    @model_validator(mode="after")
    def _validate_time_range(self):
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValueError("结束时间不能早于开始时间")
        return self


class TenantUpdateSchema(BaseModel):
    """更新租户"""

    name: str | None = Field(default=None, max_length=100, description="租户名称")
    code: str | None = Field(default=None, max_length=100, description="租户编码")
    status: str | None = Field(default=None, description="状态(0:正常 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="描述")
    start_time: DateTimeStr | None = Field(default=None, description="开始时间")
    end_time: DateTimeStr | None = Field(default=None, description="结束时间")

    @field_validator("code")
    @classmethod
    def _validate_code(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v.isalnum():
            raise ValueError("编码只能包含字母和数字")
        return v

    @model_validator(mode="after")
    def _validate_time_range(self):
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValueError("结束时间不能早于开始时间")
        return self


class TenantOutSchema(TenantCreateSchema, BaseSchema):
    """租户响应"""

    model_config = ConfigDict(from_attributes=True)


class TenantQueryParam:
    """租户查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="租户名称"),
        code: str | None = Query(None, description="租户编码"),
        status: str | None = Query(None, description="状态"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
    ) -> None:
        if name:
            self.name = (QueueEnum.like.value, name)
        if code:
            self.code = (QueueEnum.like.value, code)
        if status:
            self.status = (QueueEnum.eq.value, status)
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
