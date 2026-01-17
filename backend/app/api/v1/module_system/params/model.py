from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin


class ParamsModel(ModelMixin):
    """
    参数配置表
    """

    __tablename__: str = "sys_param"
    __table_args__: dict[str, str] = {"comment": "系统参数表"}
    __loader_options__: list[str] = []

    config_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="参数名称")
    config_key: Mapped[str] = mapped_column(String(500), nullable=False, comment="参数键名")
    config_value: Mapped[str | None] = mapped_column(String(500), comment="参数键值")
    config_type: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=True,
        comment="系统内置(True:是 False:否)",
    )
