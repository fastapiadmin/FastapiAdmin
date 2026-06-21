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

from app.core.base_model import ModelMixin, TenantMixin, UserMixin


class StatusEnum(enum.Enum):
    """状态枚举"""

    ACTIVE = "active"
    INACTIVE = "inactive"


class DemoModel(ModelMixin, TenantMixin, UserMixin):
    """
    示例表 - 涵盖大多数常用数据类型
    """

    __tablename__: str = "example_demo"
    __table_args__: dict[str, str] = {"comment": "示例表"}
    __loader_options__: list[str] = ["created_by", "updated_by", "deleted_by", "tenant_by"]

    # 字符串类型
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="名称")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:启动 1:停用)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")
    int_val: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="整数")
    bigint_val: Mapped[int | None] = mapped_column(BIGINT, nullable=True, comment="大整数")
    float_val: Mapped[float | None] = mapped_column(Float, nullable=True, comment="浮点数")
    bool_val: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="布尔型")
    date_val: Mapped[date | None] = mapped_column(Date, nullable=True, comment="日期")
    time_val: Mapped[time | None] = mapped_column(Time, nullable=True, comment="时间")
    datetime_val: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="日期时间")
    text_val: Mapped[str | None] = mapped_column(Text, nullable=True, comment="长文本")
    json_val: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="元数据(JSON格式)")
