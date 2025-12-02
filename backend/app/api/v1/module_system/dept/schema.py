# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema


class DeptCreateSchema(BaseModel):
    """部门创建模型"""
    name: str = Field(..., max_length=40, description="部门名称")
    order: int = Field(default=1, ge=0, description="显示顺序")
    code: str | None = Field(default=None, max_length=60, description="部门编码")
    leader: str | None = Field(default=None, max_length=20, description="部门负责人")
    phone: str | None = Field(default=None, max_length=11, description="手机")
    email: str | None = Field(default=None, max_length=64, description="邮箱")
    parent_id: int | None = Field(default=None, ge=0, description="父部门ID")
    status: str = Field(default="0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="备注说明")

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("部门名称不能为空")
        value = value.replace(" ", "")
        return value

    @field_validator('code')
    @classmethod
    def validate_code(cls, value: str | None):
        if value is None:
            return value
        v = value.strip()
        if v == "":
            return None
        import re
        if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', v):
            raise ValueError("部门编码必须以字母开头，且仅包含字母/数字/下划线")
        return v


class DeptUpdateSchema(DeptCreateSchema):
    """部门更新模型"""
    ...


class DeptOutSchema(DeptCreateSchema, BaseSchema):
    """部门响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    parent_name: str | None = Field(default=None, max_length=64, description="父部门名称")


class DeptQueryParam:
    """部门管理查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="部门名称"),
        status: str | None = Query(None, description="部门状态(True正常 False停用)"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        
        # 模糊查询字段
        self.name = ("like", name)

        # 精确查询字段
        self.status = status

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))