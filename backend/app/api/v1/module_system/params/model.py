from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, TenantMixin, UserMixin


class ParamsModel(ModelMixin, TenantMixin, UserMixin):
    """
    系统参数表

    用于存储全局系统配置（如 retention_days、smtp 主机等）。
    平台参数（tenant_id=1）对所有租户共享；租户级参数仅本租户可见。
    """

    __tablename__: str = "sys_param"
    __table_args__: dict[str, str] = {"comment": "系统参数表"}
    __loader_options__: list[str] = [
        "created_by",
        "updated_by",
        "deleted_by",
        "tenant_by",
    ]

    config_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="参数名称")
    config_key: Mapped[str] = mapped_column(String(500), nullable=False, comment="参数键名")
    config_value: Mapped[str | None] = mapped_column(String(500), comment="参数键值")
    config_type: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True, comment="系统内置(True:是 False:否)", index=True)
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:启动 1:停用)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")
