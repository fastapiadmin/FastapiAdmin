# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema


class PositionCreateSchema(BaseModel):
    """岗位创建模型"""
    name: str = Field(..., max_length=64, description="岗位名称")
    order: int = Field(default=1, ge=1, description='显示排序')
    status: str = Field(default="0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="描述")

    @field_validator('name')
    @classmethod
    def _validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('岗位名称不能为空')
        return v


class PositionUpdateSchema(PositionCreateSchema):
    """岗位更新模型"""
    ...


class PositionOutSchema(PositionCreateSchema, BaseSchema, UserBySchema):
    """岗位信息响应模型"""
    model_config = ConfigDict(from_attributes=True)
    ...


class PositionQueryParam:
    """岗位管理查询参数"""

    def __init__(
        self,
        name: Optional[str] = Query(None, description="岗位名称"),
        status: Optional[str] = Query(None, description="是否可用"),
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
        