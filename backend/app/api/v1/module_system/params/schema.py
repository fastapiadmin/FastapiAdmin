# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema


class ParamsCreateSchema(BaseModel):
    """配置创建模型"""
    config_name: str = Field(..., max_length=64, description="参数名称")
    config_key: str = Field(..., max_length=500, description="参数键名")
    config_value: str | None = Field(default=None, description="参数键值")
    config_type: bool = Field(default=False, description="系统内置(True:是 False:否)")
    status: str = Field(default="0", description="状态(True:正常 False:停用)")
    description: str | None = Field(default=None, max_length=500, description="描述")

    @field_validator('config_key')
    @classmethod
    def _validate_config_key(cls, v: str) -> str:
        v = v.strip().lower()
        import re
        if not re.match(r'^[a-z][a-z0-9_.-]*$', v):
            raise ValueError('参数键名必须以小写字母开头，仅包含小写字母/数字/_.-')
        return v


class ParamsUpdateSchema(ParamsCreateSchema):
    """配置更新模型"""
    ...


class ParamsOutSchema(ParamsCreateSchema, BaseSchema):
    """配置响应模型"""
    model_config = ConfigDict(from_attributes=True)


class ParamsQueryParam:
    """配置管理查询参数"""

    def __init__(
        self,
        config_name: str | None = Query(None, description="配置名称"),
        config_key: str | None = Query(None, description="配置键名"),
        config_type: bool | None = Query(None, description="系统内置((True:是 False:否))"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:

        # 模糊查询字段
        self.config_name = ("like", config_name)
        self.config_key = ("like", config_key)

        # 精确查询字段
        self.config_type = config_type

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))

