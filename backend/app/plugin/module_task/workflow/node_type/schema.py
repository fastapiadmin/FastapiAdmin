from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class WorkflowNodeTypeCreateSchema(BaseModel):
    """创建编排节点类型"""

    name: str = Field(..., max_length=128, description="显示名称")
    code: str = Field(..., max_length=64, description="节点编码")
    category: str = Field(
        default="action", max_length=32, description="trigger/action/condition/control"
    )
    func: str = Field(..., description="代码块，须定义 handler")
    args: str | None = Field(default=None, description="默认位置参数")
    kwargs: str | None = Field(default=None, description="默认 kwargs JSON")
    sort_order: int = Field(default=0, ge=0, description="排序")
    is_active: bool = Field(default=True, description="是否启用")

    @field_validator("category")
    @classmethod
    def _cat(cls, v: str) -> str:
        allowed = {"trigger", "action", "condition", "control"}
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


class WorkflowNodeTypeOutSchema(WorkflowNodeTypeCreateSchema, BaseSchema, UserBySchema):
    """输出（含审计与用户信息）"""

    model_config = ConfigDict(from_attributes=True)


class WorkflowNodeTypeQueryParam:
    """查询"""

    def __init__(
        self,
        name: str | None = Query(None, description="名称"),
        code: str | None = Query(None, description="编码"),
        category: str | None = Query(None, description="分类"),
        is_active: bool | None = Query(None, description="是否启用"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        updated_time: list[DateTimeStr] | None = Query(
            None,
            description="更新时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:
        self.name = (QueueEnum.like.value, name)
        self.code = (QueueEnum.like.value, code)
        self.category = (QueueEnum.eq.value, category)
        self.is_active = (QueueEnum.eq.value, is_active)
        self.created_id = (QueueEnum.eq.value, created_id)
        self.updated_id = (QueueEnum.eq.value, updated_id)
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = (QueueEnum.between.value, (updated_time[0], updated_time[1]))
