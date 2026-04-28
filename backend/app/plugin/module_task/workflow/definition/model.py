from sqlalchemy import JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class WorkflowModel(ModelMixin, UserMixin):
    """
    工作流定义：Vue Flow 画布序列化 + Prefect 运行时执行
    """

    __tablename__: str = "task_workflow"
    __table_args__ = (
        UniqueConstraint("code", name="uq_task_workflow_code"),
        {"comment": "工作流定义表"},
    )
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(128), nullable=False, comment="流程名称")
    code: Mapped[str] = mapped_column(String(64), nullable=False, comment="流程编码")
    workflow_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        comment="流程状态: draft/published/archived",
    )
    nodes: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="Vue Flow nodes JSON")
    edges: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="Vue Flow edges JSON")
