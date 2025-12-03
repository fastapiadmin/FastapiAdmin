# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema


class DemoCreateSchema(BaseModel):
    """新增模型"""
    name: str = Field(..., min_length=2, max_length=50, description='名称')
    status: str = Field(default="0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="描述")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """验证名称字段的格式和内容"""
        # 去除首尾空格
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
        if len(self.name) < 2 or len(self.name) > 50:
            raise ValueError('名称长度必须在2-50个字符之间')
        # 格式校验：名称只能包含字母、数字、下划线和中划线
        if not self.name.isalnum() and not all(c in '-_' for c in self.name):
            raise ValueError('名称只能包含字母、数字、下划线和中划线')
        
        return self


class DemoUpdateSchema(DemoCreateSchema):
    """更新模型"""
    ...


class DemoOutSchema(DemoCreateSchema, BaseSchema, UserBySchema):
    """响应模型"""
    model_config = ConfigDict(from_attributes=True)


class DemoQueryParam:
    """示例查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="名称"),
        status: str | None = Query(None, description="是否启用"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:
        
        # 模糊查询字段
        self.name = ("like", name)

        # 精确查询字段
        self.created_id = created_id
        self.updated_id = updated_id
        self.status = status

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
