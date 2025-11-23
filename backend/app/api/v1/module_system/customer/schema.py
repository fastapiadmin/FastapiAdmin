# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.base_schema import BaseSchema


class TenantCreateSchema(BaseModel):
    """新增模型"""
    name: str = Field(..., max_length=64, description='租户名称')
    code: Optional[str] = Field(default=None, max_length=20, description='租户编码')
    status: bool = Field(True, description="是否启用(True:启用 False:禁用)")
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

class TenantUpdateSchema(TenantCreateSchema):
    """更新模型"""
    ...


class TenantOutSchema(TenantCreateSchema, BaseSchema):
    """响应模型"""
    model_config = ConfigDict(from_attributes=True)
