# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema, TenantSchema, CustomerSchema


class CustomerCreateSchema(BaseModel):
    """新增模型"""
    name: str = Field(..., max_length=64, description='客户名称')
    code: Optional[str] = Field(default=None, max_length=20, description='客户编码')    
    status: str = Field(True, description="是否启用(True:启用 False:禁用)")
    description: Optional[str] = Field(default=None, max_length=255, description="描述")

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


class CustomerUpdateSchema(CustomerCreateSchema):
    """更新模型"""
    ...


class CustomerOutSchema(CustomerCreateSchema, BaseSchema, UserBySchema, TenantSchema, CustomerSchema):
    """响应模型"""
    model_config = ConfigDict(from_attributes=True)


class CustomerQueryParam:
    """客户查询参数"""

    def __init__(
        self,
        name: Optional[str] = Query(None, description="客户名称"),
        status: Optional[str] = Query(None, description="状态用(True:启用 False:禁用)"),
        created_id: Optional[int] = Query(None, description="创建人"),
        created_time: Optional[list[DateTimeStr]] = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        
        # 模糊查询字段
        self.name = ("like", name)

        # 精确查询字段
        self.created_id = created_id
        self.status = status

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
