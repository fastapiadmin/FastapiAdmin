from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class Demo01Model(ModelMixin, UserMixin):
    """
    示例表 - 涵盖大多数常用数据类型
    """

    __tablename__: str = "gen_demo01"
    __table_args__: dict[str, str] = {"comment": "示例1表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 字符串类型
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="名称")
