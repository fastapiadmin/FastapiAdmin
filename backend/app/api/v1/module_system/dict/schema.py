# -*- coding: utf-8 -*-

import re
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema


class DictTypeCreateSchema(BaseModel):
    """
    字典类型表对应pydantic模型
    """

    dict_name: str = Field(..., min_length=1, max_length=100, description='字典名称', example='用户状态')
    dict_type: str = Field(..., min_length=1, max_length=100, description='字典类型', example='sys_user_status')
    status: Optional[str] = Field(default=None, description='状态（1正常 0停用）', example=True)
    description: Optional[str] = Field(default=None, max_length=255, description="描述", example="用户账号状态管理")

    @field_validator('dict_name')
    def validate_dict_name(cls, value: str):
        if not value or value.strip() == '':
            raise ValueError('字典名称不能为空')
        return value.strip()

    @field_validator('dict_type')
    def validate_dict_type(cls, value: str):
        if not value or value.strip() == '':
            raise ValueError('字典类型不能为空')
        regexp = r'^[a-z][a-z0-9_]*$'
        if not re.match(regexp, value):
            raise ValueError('字典类型必须以字母开头，且只能为（小写字母，数字，下滑线）')
        return value.strip()


class DictTypeUpdateSchema(DictTypeCreateSchema):
    """字典类型更新模型"""
    ...


class DictTypeOutSchema(DictTypeCreateSchema, BaseSchema):
    """字典类型响应模型"""
    model_config = ConfigDict(from_attributes=True)


class DictTypeQueryParam:
    """字典类型查询参数"""

    def __init__(
        self,
        dict_name: Optional[str] = Query(None, description="字典名称", max_length=100, example="用户"),
        dict_type: Optional[str] = Query(None, description="字典类型", max_length=100, example="sys_user"),
        status: Optional[str] = Query(None, description="状态（1正常 0停用）", example=True),
        created_time: Optional[list[DateTimeStr]] = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.dict_name = ("like", f"%{dict_name.strip()}%") if dict_name and dict_name.strip() else None
        
        # 精确查询字段
        self.dict_type = dict_type.strip() if dict_type else None
        self.status = status
        
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))


class DictDataCreateSchema(BaseModel):
    """
    字典数据表对应pydantic模型
    """
    dict_sort: int = Field(..., ge=1, le=999, description='字典排序', example=1)
    dict_label: str = Field(..., max_length=100, description='字典标签', example='正常')
    dict_value: str = Field(..., max_length=100, description='字典键值', example='0')
    dict_type: str = Field(..., max_length=100, description='字典类型', example='sys_user_status')
    dict_type_id: int = Field(..., description='字典类型ID', example=1)
    css_class: Optional[str] = Field(default=None, max_length=100, description='样式属性（其他样式扩展）', example='label-success')
    list_class: Optional[str] = Field(default=None, description='表格回显样式', example='success')
    is_default: Optional[bool] = Field(default=None, description='是否默认（Y是 N否）', example=True)
    status: Optional[str] = Field(default=None, description='状态（1正常 0停用）', example=True)
    description: Optional[str] = Field(default=None, max_length=255, description="描述", example="正常状态的用户")
    
    @model_validator(mode='after')
    def validate_after(self):
        if not self.dict_label or not self.dict_label.strip():
            raise ValueError('字典标签不能为空')
        if not self.dict_value or not self.dict_value.strip():
            raise ValueError('字典键值不能为空')
        if not self.dict_type or not self.dict_type.strip():
            raise ValueError('字典类型不能为空')
        if not hasattr(self, 'dict_type_id') or self.dict_type_id <= 0:
            raise ValueError('字典类型ID不能为空且必须大于0')
        
        # 确保字符串字段被正确处理
        self.dict_label = self.dict_label.strip()
        self.dict_value = self.dict_value.strip()
        self.dict_type = self.dict_type.strip()
        
        return self


class DictDataUpdateSchema(DictDataCreateSchema):
    """字典数据更新模型"""
    ...


class DictDataOutSchema(DictDataCreateSchema, BaseSchema):
    """字典数据响应模型"""
    model_config = ConfigDict(from_attributes=True)


class DictDataQueryParam:
    """字典数据查询参数"""

    def __init__(
        self,
        dict_label: Optional[str] = Query(None, description="字典标签", max_length=100, example="正常"),
        dict_type: Optional[str] = Query(None, description="字典类型", max_length=100, example="sys_user_status"),
        dict_type_id: Optional[int] = Query(None, description="字典类型ID", example=1),
        status: Optional[str] = Query(None, description="状态（1正常 0停用）", example=True),
        created_time: Optional[list[DateTimeStr]] = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        
        # 模糊查询字段
        self.dict_label = ("like", f"%{dict_label.strip()}%") if dict_label and dict_label.strip() else None
        
        # 精确查询字段
        self.dict_type = dict_type.strip() if dict_type else None
        self.dict_type_id = dict_type_id
        self.status = status
        
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
