import re
from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam, TenantByQueryParam, UserByQueryParam
from app.core.base_schema import BaseSchema, TenantBySchema, UserBySchema


class WorkflowNodeTypeCreateSchema(BaseModel):
    """创建编排节点类型"""

    name: str = Field(..., max_length=128, description="显示名称")
    code: str = Field(..., max_length=64, description="节点编码")
    category: str = Field(default="action", max_length=32, description="trigger/action/condition/control")
    func: str = Field(..., description="代码块，须定义 handler")
    args: str | None = Field(default=None, description="默认位置参数")
    kwargs: str | None = Field(default=None, description="默认 kwargs JSON")
    sort_order: int = Field(default=0, ge=0, description="排序")
    is_active: bool = Field(default=True, description="是否启用")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1 or len(v) > 128:
            raise ValueError("显示名称长度必须在1-128个字符之间")
        return v

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 64:
            raise ValueError("节点编码长度必须在2-64个字符之间")
        if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", v):
            raise ValueError("节点编码必须以字母开头，仅允许字母、数字、下划线")
        return v

    @field_validator("category")
    @classmethod
    def _cat(cls, v: str) -> str:
        allowed = {"trigger", "action", "condition", "control"}
        v = v.strip()
        if v not in allowed:
            raise ValueError(f"category 须为: {allowed}")
        return v

    @model_validator(mode="after")
    def _func_nonempty(self):
        if not self.func or not str(self.func).strip():
            raise ValueError("必须提供 func 代码块")
        return self


class WorkflowNodeTypeUpdateSchema(WorkflowNodeTypeCreateSchema):
    """更新编排节点类型"""


class WorkflowNodeTypeOutSchema(WorkflowNodeTypeCreateSchema, BaseSchema, UserBySchema, TenantBySchema):
    """输出（含审计与用户信息）"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class WorkflowNodeTypeQueryParam(BaseQueryParam, UserByQueryParam, TenantByQueryParam):
    """查询"""

    name: str | None = Query(None, description="名称")
    code: str | None = Query(None, description="编码")
    category: str | None = Query(None, description="分类")
    is_active: bool | None = Query(None, description="是否启用")

    def __post_init__(self) -> None:
        self.name = (QueueEnum.like.value, self.name) if self.name else None
        self.code = (QueueEnum.like.value, self.code) if self.code else None
        self.category = (QueueEnum.eq.value, self.category) if self.category else None
        self.is_active = (QueueEnum.eq.value, self.is_active) if self.is_active is not None else None
