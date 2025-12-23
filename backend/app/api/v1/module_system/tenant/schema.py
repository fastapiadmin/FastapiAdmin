# -*- coding: utf-8 -*-

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.base_schema import BaseSchema
from app.core.validator import DateTimeStr


class TenantCreateSchema(BaseModel):
    """新增模型"""
    name: str = Field(..., description='租户名称')
    code: str | None = Field(default=None, description='租户编码')
    domain: str | None = Field(default=None, description='租户域名')
    status: str = Field(default="0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, description="描述")
    
    @field_validator('name')    
    @classmethod
    def _validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('名称不能为空')
        return v

    @model_validator(mode='after')
    def _after_validation(self):
        """
        核心业务规则校验
        """
        # 长度校验：名称最小长度
        if len(self.name) < 2 or len(self.name) > 64:
            raise ValueError('名称长度必须在2-50个字符之间')
        # 格式校验：名称只能包含字母、数字、下划线和中划线
        if not self.name.isalnum() and not all(c in '-_' for c in self.name):
            raise ValueError('名称只能包含字母、数字、下划线和中划线')
        
        return self


class TenantUpdateSchema(TenantCreateSchema):
    """更新模型"""
    ...

class TenantOutSchema(TenantCreateSchema, BaseSchema):
    """响应模型"""
    model_config = ConfigDict(from_attributes=True)


class TenantQueryParam:
    """租户查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="名称"),
        description: str | None = Query(None, description="描述"),
        status: str | None = Query(None, description="是否启用"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人")
    ) -> None:
        # 模糊查询字段
        self.name = ("like", name)
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


