from sqlalchemy import JSON, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, TenantMixin, UserMixin


class WorkflowModel(ModelMixin, TenantMixin, UserMixin):
    """
    工作流定义：Vue Flow 画布序列化 + 拓扑分层并行执行
    """

    __tablename__: str = "task_workflow"
    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_task_workflow_code"),
        {"comment": "工作流定义表"},
    )
    __loader_options__: list[str] = ["created_by", "updated_by", "deleted_by", "tenant_by"]

    name: Mapped[str] = mapped_column(String(128), nullable=False, comment="流程名称")
    code: Mapped[str] = mapped_column(String(64), nullable=False, comment="流程编码")
    nodes: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="VueFlow节点")
    edges: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="VueFlow连接线")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:草稿 1:已发布 2:已归档)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")
