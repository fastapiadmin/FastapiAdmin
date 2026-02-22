import enum

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class WorkflowStatusEnum(enum.Enum):
    """流程状态枚举"""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


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
    nodes: Mapped[list] = mapped_column(JSON, nullable=False, default=list, comment="节点数据(JSON格式)")
    edges: Mapped[list] = mapped_column(JSON, nullable=False, default=list, comment="连线数据(JSON格式)")
