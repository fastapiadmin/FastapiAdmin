import enum

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class NodeCategoryEnum(enum.Enum):
    """节点分类枚举"""

    TRIGGER = "trigger"
    ACTION = "action"
    CONDITION = "condition"
    CONTROL = "control"
    INTEGRATION = "integration"
    CUSTOM = "custom"


class NodeModel(ModelMixin, UserMixin):
    """
    节点类型模型 - 动态定义节点类型
    """

    __tablename__: str = "task_node"
    __table_args__: dict[str, str] = {"comment": "节点类型表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, comment="节点类型名称")
    code: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, comment="节点类型编码")
    category: Mapped[str] = mapped_column(
        String(32), default=NodeCategoryEnum.ACTION.value, comment="节点分类"
    )
    config_schema: Mapped[dict] = mapped_column(JSON, nullable=False, comment="配置表单Schema(JSON Schema)")
    input_schema: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="输入数据Schema")
    output_schema: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="输出数据Schema")
    handler: Mapped[str] = mapped_column(String(256), nullable=False, comment="处理器路径")
    description: Mapped[str | None] = mapped_column(String(512), nullable=True, comment="描述")
    meta_data: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="元数据")
