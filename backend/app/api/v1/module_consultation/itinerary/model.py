"""
行程方案管理 - 数据模型
"""
from datetime import date, datetime

from sqlalchemy import (
    BIGINT,
    Boolean,
    Date,
    DateTime,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ItineraryModel(ModelMixin, UserMixin):
    """
    行程方案表

    存储生成的咨询会行程方案
    """

    __tablename__: str = "consultation_itinerary"
    __table_args__: dict[str, str] = {"comment": "行程方案表"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    consultation_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="咨询会ID")
    team_id: Mapped[int | None] = mapped_column(BIGINT, comment="招生组ID")

    itinerary_name: Mapped[str | None] = mapped_column(String(200), comment="行程方案名称")
    start_date: Mapped[date] = mapped_column(Date, nullable=False, comment="开始日期")
    end_date: Mapped[date] = mapped_column(Date, comment="结束日期")

    departure_city: Mapped[str | None] = mapped_column(String(50), comment="出发城市")
    destination_city: Mapped[str | None] = mapped_column(String(50), comment="目的城市")
    transportation: Mapped[str | None] = mapped_column(String(50), comment="交通方式")
    departure_time: Mapped[datetime | None] = mapped_column(DateTime, comment="出发时间")
    arrival_time: Mapped[datetime | None] = mapped_column(DateTime, comment="到达时间")
    transportation_no: Mapped[str | None] = mapped_column(String(100), comment="车次/航班号")

    hotel_name: Mapped[str | None] = mapped_column(String(200), comment="酒店名称")
    hotel_address: Mapped[str | None] = mapped_column(String(500), comment="酒店地址")
    check_in_date: Mapped[date | None] = mapped_column(Date, comment="入住日期")
    check_out_date: Mapped[date | None] = mapped_column(Date, comment="退房日期")
    room_number: Mapped[str | None] = mapped_column(String(50), comment="房间号")

    itinerary_status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False, comment="状态(draft/confirmed/executed/archived)")
    is_synced: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否已同步到日历")
