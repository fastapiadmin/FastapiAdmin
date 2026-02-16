from dataclasses import dataclass
from datetime import datetime

from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
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
    version: str = Field(default="1.0.0", description="版本号")
    category: str | None = Field(default=None, description="流程分类")
    tags: list[str] | None = Field(default=None, description="标签列表")
    is_template: bool = Field(default=False, description="是否为模板")
    template_id: int | None = Field(default=None, description="模板ID")
    meta_data: dict | None = Field(default=None, description="元数据(JSON格式)")
    canvas_state: dict | None = Field(default=None, description="画布状态(缩放、平移等)")
    thumbnail: str | None = Field(default=None, description="流程缩略图(Base64)")
    statistics: dict | None = Field(default=None, description="流程统计信息")

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
        if self.is_template and self.template_id:
            raise ValueError("模板不能引用其他模板")
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
    version: str | None = Field(default=None, description="版本号")
    category: str | None = Field(default=None, description="流程分类")
    tags: list[str] | None = Field(default=None, description="标签列表")
    is_template: bool | None = Field(default=None, description="是否为模板")
    template_id: int | None = Field(default=None, description="模板ID")
    published_at: str | None = Field(default=None, description="发布时间")
    published_by: int | None = Field(default=None, description="发布人ID")
    meta_data: dict | None = Field(default=None, description="元数据(JSON格式)")
    canvas_state: dict | None = Field(default=None, description="画布状态(缩放、平移等)")
    thumbnail: str | None = Field(default=None, description="流程缩略图(Base64)")
    statistics: dict | None = Field(default=None, description="流程统计信息")

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
        if self.is_template and self.template_id:
            raise ValueError("模板不能引用其他模板")
        if self.description and len(self.description) > 1000:
            raise ValueError("流程描述长度不能超过1000个字符")
        return self


class WorkflowOutSchema(WorkflowUpdateSchema, BaseSchema, UserBySchema):
    """工作流响应模型"""

    model_config = ConfigDict(from_attributes=True)


class WorkflowPublishSchema(BaseModel):
    """发布工作流模型"""

    version: str | None = Field(default=None, description="版本号")


class WorkflowValidateSchema(BaseModel):
    """验证工作流模型"""

    nodes: list = Field(..., description="节点数据(JSON格式)")
    edges: list = Field(..., description="连线数据(JSON格式)")


class WorkflowValidateResultSchema(BaseModel):
    """工作流验证结果模型"""

    is_valid: bool = Field(..., description="是否有效")
    errors: list[str] = Field(default_factory=list, description="错误列表")
    warnings: list[str] = Field(default_factory=list, description="警告列表")
    stats: dict = Field(default_factory=dict, description="统计信息")


@dataclass
class WorkflowQueryParam:
    """工作流查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="流程名称"),
        code: str | None = Query(None, description="流程编码"),
        status: str | None = Query(None, description="流程状态"),
        category: str | None = Query(None, description="流程分类"),
        is_template: bool | None = Query(None, description="是否为模板"),
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
        if category:
            self.category = (QueueEnum.eq.value, category)
        if is_template is not None:
            self.is_template = (QueueEnum.eq.value, is_template)
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

    task_run_id: int = Field(..., description="任务运行记录ID")
    workflow_id: int = Field(..., description="工作流ID")
    workflow_name: str = Field(..., description="工作流名称")
    status: str = Field(..., description="执行状态")
    message: str = Field(..., description="执行消息")


class WorkflowRunCreateSchema(BaseModel):
    """创建工作流运行记录模型"""
    workflow_id: int = Field(..., description="工作流ID")
    workflow_name: str = Field(..., description="工作流名称")
    workflow_version: str = Field(default="1.0.0", description="工作流版本")
    business_key: str | None = Field(default=None, description="业务键")
    initiator: int | None = Field(default=None, description="发起人ID")
    initiator_name: str | None = Field(default=None, description="发起人姓名")
    variables: dict = Field(default_factory=dict, description="流程变量(JSON格式)")
    job_id: int | None = Field(default=None, description="关联的定时任务ID")


class WorkflowRunUpdateSchema(BaseModel):
    """更新工作流运行记录模型"""
    status: str | None = Field(default=None, description="运行状态")
    error_message: str | None = Field(default=None, description="错误信息")
    start_time: datetime | None = Field(default=None, description="开始时间")
    end_time: datetime | None = Field(default=None, description="结束时间")
    duration: int | None = Field(default=None, description="执行时长(秒)")
    retry_count: int | None = Field(default=None, description="重试次数")
    max_retry: int | None = Field(default=None, description="最大重试次数")
    meta_data: dict | None = Field(default=None, description="元数据(JSON格式)")


class WorkflowRunOutSchema(WorkflowRunCreateSchema, WorkflowRunUpdateSchema, BaseSchema, UserBySchema):
    """工作流运行记录响应模型"""

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('start_time', 'end_time')
    def serialize_datetime(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")


class WorkflowRunLogCreateSchema(BaseModel):
    """创建工作流运行日志模型"""
    task_run_id: int = Field(..., description="工作流运行记录ID")
    level: str = Field(default="info", description="日志级别")
    node_id: str | None = Field(default=None, description="节点ID")
    node_name: str | None = Field(default=None, description="节点名称")
    message: str = Field(..., description="日志消息")
    data: dict | None = Field(default=None, description="日志数据(JSON格式)")


class WorkflowRunLogOutSchema(BaseModel):
    """工作流运行日志响应模型"""
    id: int
    task_run_id: int
    level: str
    node_id: str | None
    node_name: str | None
    message: str
    data: dict | None
    created_time: str
    created_by: dict | None

    model_config = ConfigDict(from_attributes=True)


@dataclass
class WorkflowRunQueryParam:
    """工作流运行记录查询参数"""
    def __init__(
        self,
        workflow_id: int | None = Query(None, description="工作流ID"),
        workflow_name: str | None = Query(None, description="工作流名称"),
        status: str | None = Query(None, description="运行状态"),
        business_key: str | None = Query(None, description="业务键"),
        initiator: int | None = Query(None, description="发起人"),
        job_id: int | None = Query(None, description="定时任务ID"),
        created_time: list[str] | None = Query(None, description="创建时间范围"),
        updated_time: list[str] | None = Query(None, description="更新时间范围"),
    ) -> None:
        if workflow_id:
            self.workflow_id = (QueueEnum.eq.value, workflow_id)
        if workflow_name:
            self.workflow_name = (QueueEnum.like.value, workflow_name)
        if status:
            self.status = (QueueEnum.eq.value, status)
        if business_key:
            self.business_key = (QueueEnum.like.value, business_key)
        if initiator:
            self.initiator = (QueueEnum.eq.value, initiator)
        if job_id:
            self.job_id = (QueueEnum.eq.value, job_id)
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = (QueueEnum.between.value, (updated_time[0], updated_time[1]))


@dataclass
class WorkflowRunLogQueryParam:
    """工作流运行日志查询参数"""
    def __init__(
        self,
        task_run_id: int | None = Query(None, description="工作流运行记录ID"),
        level: str | None = Query(None, description="日志级别"),
        node_id: str | None = Query(None, description="节点ID"),
        node_name: str | None = Query(None, description="节点名称"),
        created_time: list[str] | None = Query(None, description="创建时间范围"),
    ) -> None:
        if task_run_id:
            self.task_run_id = (QueueEnum.eq.value, task_run_id)
        if level:
            self.level = (QueueEnum.eq.value, level)
        if node_id:
            self.node_id = (QueueEnum.like.value, node_id)
        if node_name:
            self.node_name = (QueueEnum.like.value, node_name)
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
