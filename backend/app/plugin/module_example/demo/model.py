import enum
from datetime import date, datetime, time

from sqlalchemy import (
    BIGINT,
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class StatusEnum(enum.Enum):
    """状态枚举"""

    ACTIVE = "active"
    INACTIVE = "inactive"


class DemoModel(ModelMixin, UserMixin):
    """
    示例表 - 涵盖大多数常用数据类型
    """

    __tablename__: str = "gen_demo"
    __table_args__: dict[str, str] = {"comment": "示例表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 字符串类型
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="名称")
    a: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="整数")
    b: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="大整数")
    c: Mapped[float | None] = mapped_column(Float, nullable=True, comment="浮点数")
    d: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="布尔型")
    e: Mapped[date | None] = mapped_column(Date, nullable=True, comment="日期")
    f: Mapped[time | None] = mapped_column(Time, nullable=True, comment="时间")
    g: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="日期时间")
    h: Mapped[str | None] = mapped_column(Text, nullable=True, comment="长文本")
    i: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="元数据(JSON格式)")
