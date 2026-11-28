from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import JSONType, ModelMixin, UserMixin


class WorkflowModel(ModelMixin, UserMixin):
    """可执行流程定义：审批 + 条件，按步骤顺序执行。"""

    __tablename__: str = "task_workflow"
    __table_args__: dict[str, str] = {"comment": "流程定义表"}

    name: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="流程名称")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="流程说明")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:启用 1:停用)")
    steps: Mapped[list] = mapped_column(JSONType, nullable=False, default=list, comment="步骤配置")


class WorkflowInstanceModel(ModelMixin, UserMixin):
    """流程实例：保存执行上下文与当前步骤。"""

    __tablename__: str = "task_workflow_instance"
    __table_args__: dict[str, str] = {"comment": "流程实例表"}

    workflow_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="流程ID")
    workflow_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="流程名称快照")
    status: Mapped[str] = mapped_column(String(16), default="running", nullable=False, comment="running/completed/rejected")
    current_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="当前步骤索引")
    steps: Mapped[list] = mapped_column(JSONType, nullable=False, default=list, comment="步骤快照")
    context: Mapped[dict] = mapped_column(JSONType, nullable=False, default=dict, comment="执行上下文")
    error: Mapped[str | None] = mapped_column(Text, nullable=True, comment="失败原因")


class WorkflowTaskModel(ModelMixin, UserMixin):
    """审批任务：审批节点产生，审批后流程继续。"""

    __tablename__: str = "task_workflow_task"
    __table_args__: dict[str, str] = {"comment": "流程审批任务表"}

    instance_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="实例ID")
    step_index: Mapped[int] = mapped_column(Integer, nullable=False, comment="步骤索引")
    step_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="步骤名称")
    assignee_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True, comment="审批人ID")
    status: Mapped[str] = mapped_column(String(16), default="pending", nullable=False, comment="pending/approved/rejected")
    comment: Mapped[str | None] = mapped_column(Text, nullable=True, comment="审批意见")
    acted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="处理时间")
