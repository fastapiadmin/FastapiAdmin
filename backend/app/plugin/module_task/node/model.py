import enum

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class NodeCategoryEnum(enum.Enum):
    """节点分类枚举"""

    TRIGGER = "trigger"
    ACTION = "action"
    CONDITION = "condition"
    CONTROL = "control"


class NodeModel(ModelMixin, UserMixin):
    """
    节点类型模型 - 动态定义节点类型
    """

    __tablename__: str = "task_node"
    __table_args__: dict[str, str] = {"comment": "节点类型表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="节点名称")
    code: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, comment="节点编码")
    category: Mapped[str] = mapped_column(String(32), default=NodeCategoryEnum.ACTION.value, comment="节点分类")
    jobstore: Mapped[str | None] = mapped_column(String(64), nullable=True, default="default", comment="存储器")
    executor: Mapped[str | None] = mapped_column(String(64), nullable=True, default="default", comment="执行器")
    trigger: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="触发器")
    trigger_args: Mapped[str | None] = mapped_column(Text, nullable=True, comment="触发器参数")
    func: Mapped[str | None] = mapped_column(Text, nullable=True, comment="代码块")
    args: Mapped[str | None] = mapped_column(Text, nullable=True, comment="位置参数")
    kwargs: Mapped[str | None] = mapped_column(Text, nullable=True, comment="关键字参数")
    coalesce: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False, comment="是否合并运行")
    max_instances: Mapped[int] = mapped_column(Integer, nullable=True, default=1, comment="最大实例数")
    start_date: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="开始时间")
    end_date: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="结束时间")
