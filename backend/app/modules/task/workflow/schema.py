from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.base_schema import BaseQueryParam, BaseSchema

StepType = Literal["approval", "condition"]
ConditionOperator = Literal["eq", "ne", "gt", "gte", "lt", "lte", "contains"]


class WorkflowStepSchema(BaseModel):
    type: StepType = Field(..., description="步骤类型")
    name: str = Field(..., min_length=1, max_length=64, description="步骤名称")
    assignee_id: int | None = Field(default=None, ge=1, description="审批人ID，空则为发起人")
    field: str | None = Field(default=None, max_length=64, description="条件字段（支持 a.b）")
    operator: ConditionOperator | None = Field(default=None, description="条件运算符")
    value: str | int | float | bool | None = Field(default=None, description="条件比较值")

    @model_validator(mode="after")
    def validate_step(self):
        if self.type == "condition":
            if not self.field or not self.operator:
                raise ValueError("条件步骤必须填写字段与运算符")
        return self


class WorkflowCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    description: str | None = Field(default=None, max_length=500)
    status: int = Field(default=0, ge=0, le=1)
    steps: list[WorkflowStepSchema] = Field(..., min_length=1, max_length=50)

    @model_validator(mode="after")
    def validate_steps(self):
        if not any(step.type == "approval" for step in self.steps):
            raise ValueError("流程至少需要一个审批步骤")
        return self


class WorkflowUpdateSchema(WorkflowCreateSchema):
    pass


class WorkflowRunSchema(BaseModel):
    context: dict = Field(default_factory=dict, description="运行上下文")


class WorkflowActionSchema(BaseModel):
    approved: bool = Field(..., description="是否通过")
    comment: str | None = Field(default=None, max_length=500)


class WorkflowOutSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: str | None = None
    status: int = 0
    steps: list[dict] = Field(default_factory=list)


class WorkflowInstanceOutSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    workflow_id: int
    workflow_name: str
    status: str
    current_index: int
    steps: list[dict] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)
    error: str | None = None


class WorkflowTaskOutSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    instance_id: int
    step_index: int
    step_name: str
    assignee_id: int | None = None
    status: str
    comment: str | None = None
    acted_at: datetime | None = None


class WorkflowQueryParam(BaseQueryParam):
    name: str | None = Field(None, description="流程名称", json_schema_extra={"q": "like"})
    status: int | None = Field(None, ge=0, le=1, json_schema_extra={"q": "eq"})


class WorkflowInstanceQueryParam(BaseQueryParam):
    workflow_id: int | None = Field(None, ge=1, json_schema_extra={"q": "eq"})
    status: str | None = Field(None, json_schema_extra={"q": "eq"})


class WorkflowTaskQueryParam(BaseQueryParam):
    status: str | None = Field(None, json_schema_extra={"q": "eq"})
