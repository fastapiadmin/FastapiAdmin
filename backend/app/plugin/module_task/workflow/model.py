import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class StatusEnum(enum.Enum):
    """状态枚举"""

    ACTIVE = "active"
    INACTIVE = "inactive"


class WorkflowStatusEnum(enum.Enum):
    """流程状态枚举"""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class RunStatusEnum(enum.Enum):
    """运行状态枚举"""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TERMINATED = "terminated"


class WorkflowModel(ModelMixin, UserMixin):
    """
    工作流模型 - 通用流程编排引擎
    """

    __tablename__: str = "task_workflow"
    __table_args__: dict[str, str] = {"comment": "工作流表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True, comment="流程名称")
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True, comment="流程编码")
    status: Mapped[str] = mapped_column(String(32), default=WorkflowStatusEnum.DRAFT.value, nullable=False, index=True, comment="流程状态")
    nodes: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict, comment="节点数据(JSON格式)")
    edges: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict, comment="连线数据(JSON格式)")
    version: Mapped[str] = mapped_column(String(32), default="1.0.0", comment="版本号")
    category: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True, comment="流程分类")
    tags: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="标签(JSON数组)")
    is_template: Mapped[bool] = mapped_column(Boolean, default=False, index=True, comment="是否为模板")
    template_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="模板ID")
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True, comment="发布时间")
    published_by: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="发布人ID")
    meta_data: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="元数据(JSON格式)")

    canvas_state: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="画布状态(缩放、平移等)")
    thumbnail: Mapped[str | None] = mapped_column(Text, nullable=True, comment="流程缩略图(Base64)")
    statistics: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="流程统计信息")

    execution_config: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="执行配置(超时、重试等)")
    variables: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="全局变量")
    timeout: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="流程执行超时时间(秒)")


class WorkflowRunModel(ModelMixin, UserMixin):
    """工作流运行记录模型"""
    __tablename__: str = "task_workflow_run"
    __table_args__: dict[str, str] = {"comment": "工作流运行记录表"}

    workflow_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="工作流ID")
    workflow_name: Mapped[str] = mapped_column(String(128), nullable=False, comment="工作流名称")
    workflow_version: Mapped[str] = mapped_column(String(32), default="1.0.0", comment="工作流版本")
    business_key: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="业务键")
    initiator: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="发起人ID")
    initiator_name: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="发起人姓名")
    variables: Mapped[dict] = mapped_column(JSON, default={}, comment="流程变量(JSON格式)")
    status: Mapped[str] = mapped_column(String(32), default=RunStatusEnum.PENDING.value, nullable=False, index=True, comment="运行状态")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True, comment="错误信息")
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="开始时间")
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="结束时间")
    duration: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="执行时长(秒)")
    retry_count: Mapped[int] = mapped_column(Integer, default=0, comment="重试次数")
    max_retry: Mapped[int] = mapped_column(Integer, default=3, comment="最大重试次数")
    job_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="关联的定时任务ID")
    meta_data: Mapped[dict] = mapped_column(JSON, default={}, comment="元数据(JSON格式)")


class WorkflowRunLogModel(ModelMixin, UserMixin):
    """工作流运行日志模型"""
    __tablename__: str = "task_workflow_run_log"
    __table_args__: dict[str, str] = {"comment": "工作流运行日志表"}

    task_run_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="工作流运行记录ID")
    level: Mapped[str] = mapped_column(String(16), default="info", comment="日志级别")
    node_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="节点ID")
    node_name: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="节点名称")
    message: Mapped[str] = mapped_column(Text, nullable=False, comment="日志消息")
    data: Mapped[dict] = mapped_column(JSON, default={}, comment="日志数据(JSON格式)")
