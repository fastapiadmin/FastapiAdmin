from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class WorkflowNodeTypeModel(ModelMixin, UserMixin):
    """节点类型：用于 Vue Flow 左侧 palette 与执行引擎解析。"""

    __tablename__: str = "task_workflow_node_type"
    __table_args__: dict[str, str] = {"comment": "工作流节点类型（非定时任务节点）"}

    name: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="节点类型名称")
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, comment="节点编码，对应画布 node.type")
    category: Mapped[str] = mapped_column(String(32), nullable=False, default="action", comment="分类: trigger/action/condition/control")
    func: Mapped[str] = mapped_column(Text, nullable=False, comment="Python 代码块，须定义 handler(*args,**kwargs)")
    args: Mapped[str | None] = mapped_column(Text, nullable=True, comment="默认位置参数，逗号分隔")
    kwargs: Mapped[str | None] = mapped_column(Text, nullable=True, comment="默认关键字参数 JSON")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="排序")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="是否启用")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:启动 1:停用)")
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")
