import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.base_schema import BaseQueryParam, BaseSchema, UserByQueryParam, UserBySchema
from app.core.validator import DateTimeStr


class WorkflowCreateSchema(BaseModel):
    """创建工作流"""

    name: str = Field(..., max_length=128, description="流程名称")
    code: str = Field(..., max_length=64, description="流程编码")
    description: str | None = Field(default=None, description="描述")
    nodes: list | None = Field(default=None, description="Vue Flow nodes")
    edges: list | None = Field(default=None, description="Vue Flow edges")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1 or len(v) > 128:
            raise ValueError("流程名称长度必须在1-128个字符之间")
        return v

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 64:
            raise ValueError("流程编码长度必须在2-64个字符之间")
        if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", v):
            raise ValueError("流程编码必须以字母开头，仅允许字母、数字、下划线")
        return v


class WorkflowUpdateSchema(WorkflowCreateSchema):
    """更新工作流"""

    workflow_status: int | None = Field(default=None, description="0:草稿 / 1:已发布 / 2:已归档")

    @field_validator("workflow_status")
    @classmethod
    def validate_workflow_status(cls, v: int | None) -> int | None:
        if v is None:
            return v
        allowed = {0, 1, 2}
        if v not in allowed:
            raise ValueError(f"流程状态必须为 {sorted(allowed)}")
        return v


class WorkflowOutSchema(BaseSchema, UserBySchema):
    """工作流输出（status 表示流程状态 draft/published/archived，与 ModelMixin.status 区分）"""

    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None, description="主键ID")
    uuid: str | None = Field(default=None, description="UUID")
    description: str | None = Field(default=None, description="描述")
    created_time: DateTimeStr | None = Field(default=None, description="创建时间")
    updated_time: DateTimeStr | None = Field(default=None, description="更新时间")
    name: str = Field(description="流程名称")
    code: str = Field(description="流程编码")
    status: int = Field(description="流程状态 0:草稿 / 1:已发布 / 2:已归档")
    nodes: list | None = Field(default=None, description="节点")
    edges: list | None = Field(default=None, description="连线")

    @model_validator(mode="before")
    @classmethod
    def _map_workflow_status(cls, data: Any) -> Any:
        from .model import WorkflowModel

        if isinstance(data, WorkflowModel):
            return {
                "id": data.id,
                "uuid": data.uuid,
                "description": data.description,
                "created_time": data.created_time,
                "updated_time": data.updated_time,
                "created_id": data.created_id,
                "updated_id": data.updated_id,
                "name": data.name,
                "code": data.code,
                "status": data.status,
                "nodes": data.nodes,
                "edges": data.edges,
            }
        return data


class WorkflowQueryParam(BaseQueryParam, UserByQueryParam):
    """工作流查询"""

    name: str | None = Field(None, description="流程名称", json_schema_extra={"q": "like"})
    code: str | None = Field(None, description="流程编码", json_schema_extra={"q": "eq"})


class WorkflowExecuteSchema(BaseModel):
    """执行工作流"""

    workflow_id: int = Field(..., description="工作流ID")
    variables: dict | None = Field(default=None, description="注入到各节点的 variables 上下文")
    business_key: str | None = Field(default=None, description="业务键")
    job_id: int | None = Field(default=None, description="关联任务ID")


class WorkflowExecuteResultSchema(BaseModel):
    """执行结果"""

    workflow_id: int = Field(..., description="工作流ID")
    workflow_name: str = Field(..., description="工作流名称")
    status: int = Field(description="执行状态 0:失败 / 1:已完成")
    start_time: str | None = Field(default=None, description="开始时间")
    end_time: str | None = Field(default=None, description="结束时间")
    variables: dict | None = Field(default=None, description="变量")
    node_results: dict | None = Field(default=None, description="节点结果")
    error: str | None = Field(default=None, description="错误信息")
