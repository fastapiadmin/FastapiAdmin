from dataclasses import dataclass

from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class WorkflowCreateSchema(BaseModel):
    """创建工作流模型"""

    name: str = Field(..., description="流程名称", min_length=2, max_length=128)
    code: str = Field(..., description="流程编码", min_length=2, max_length=64)
    status: str = Field(default="draft", description="流程状态(draft:草稿, published:已发布, archived:已归档)")
    description: str | None = Field(default=None, description="流程描述")
    nodes: list = Field(default_factory=list, description="节点数据(JSON格式)")
    edges: list = Field(default_factory=list, description="连线数据(JSON格式)")

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        """验证流程编码格式"""
        v = v.strip()
        if not v:
            raise ValueError("流程编码不能为空")
        if not v.replace("-", "_").replace("_", "").isalnum():
            raise ValueError("流程编码只能包含字母、数字、下划线和中划线")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """验证流程状态"""
        valid_statuses = ["draft", "published", "archived"]
        if v not in valid_statuses:
            raise ValueError(f"流程状态必须为: {', '.join(valid_statuses)}")
        return v

    @model_validator(mode="after")
    def _after_validation(self):
        """核心业务规则校验"""
        if self.description and len(self.description) > 1000:
            raise ValueError("流程描述长度不能超过1000个字符")
        return self


class WorkflowUpdateSchema(BaseModel):
    """更新工作流模型"""

    name: str | None = Field(default=None, description="流程名称", min_length=2, max_length=128)
    code: str | None = Field(default=None, description="流程编码", min_length=2, max_length=64)
    status: str | None = Field(default=None, description="流程状态")
    description: str | None = Field(default=None, description="流程描述")
    nodes: list | None = Field(default=None, description="节点数据(JSON格式)")
    edges: list | None = Field(default=None, description="连线数据(JSON格式)")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        """验证流程状态"""
        if v is not None:
            valid_statuses = ["draft", "published", "archived"]
            if v not in valid_statuses:
                raise ValueError(f"流程状态必须为: {', '.join(valid_statuses)}")
        return v

    @model_validator(mode="after")
    def _after_validation(self):
        """核心业务规则校验"""
        if self.description and len(self.description) > 1000:
            raise ValueError("流程描述长度不能超过1000个字符")
        return self


class WorkflowOutSchema(WorkflowUpdateSchema, BaseSchema, UserBySchema):
    """工作流响应模型"""

    model_config = ConfigDict(from_attributes=True)


class WorkflowPublishSchema(BaseModel):
    """发布工作流模型"""

    pass


@dataclass
class WorkflowQueryParam:
    """工作流查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="流程名称"),
        code: str | None = Query(None, description="流程编码"),
        status: str | None = Query(None, description="流程状态"),
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
        if name:
            self.name = (QueueEnum.like.value, name)
        if code:
            self.code = (QueueEnum.like.value, code)
        if status:
            self.status = (QueueEnum.eq.value, status)
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = (QueueEnum.between.value, (updated_time[0], updated_time[1]))
        if created_id:
            self.created_id = (QueueEnum.eq.value, created_id)
        if updated_id:
            self.updated_id = (QueueEnum.eq.value, updated_id)


class WorkflowExecuteSchema(BaseModel):
    """执行工作流模型"""

    workflow_id: int = Field(..., description="工作流ID")
    variables: dict = Field(default_factory=dict, description="流程变量(JSON格式)")
    business_key: str | None = Field(default=None, description="业务键")
    job_id: int | None = Field(default=None, description="关联的定时任务ID")


class WorkflowExecuteResultSchema(BaseModel):
    """工作流执行结果模型"""

    workflow_id: int = Field(..., description="工作流ID")
    workflow_name: str = Field(..., description="工作流名称")
    status: str = Field(..., description="执行状态")
    start_time: str | None = Field(default=None, description="开始时间")
    end_time: str | None = Field(default=None, description="结束时间")
    variables: dict = Field(default_factory=dict, description="流程变量")
    node_results: dict = Field(default_factory=dict, description="节点执行结果")
