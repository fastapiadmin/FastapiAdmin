"""
行程方案管理 - 数据验证Schema
"""

from pydantic import ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class ItineraryCreateSchema(BaseSchema):
    """新增行程方案模型"""

    consultation_id: int = Field(..., description="咨询会ID")
    team_id: int | None = Field(default=None, description="招生组ID")
    itinerary_name: str | None = Field(default=None, description="行程方案名称", max_length=200)
    start_date: DateStr = Field(..., description="开始日期")
    end_date: DateStr | None = Field(default=None, description="结束日期")
    departure_city: str | None = Field(default=None, description="出发城市", max_length=50)
    destination_city: str | None = Field(default=None, description="目的城市", max_length=50)
    transportation: str | None = Field(default=None, description="交通方式", max_length=50)
    departure_time: DateTimeStr | None = Field(default=None, description="出发时间")
    arrival_time: DateTimeStr | None = Field(default=None, description="到达时间")
    transportation_no: str | None = Field(default=None, description="车次/航班号", max_length=100)
    hotel_name: str | None = Field(default=None, description="酒店名称", max_length=200)
    hotel_address: str | None = Field(default=None, description="酒店地址", max_length=500)
    check_in_date: DateStr | None = Field(default=None, description="入住日期")
    check_out_date: DateStr | None = Field(default=None, description="退房日期")
    room_number: str | None = Field(default=None, description="房间号", max_length=50)
    board_column: str | None = Field(default="todo", description="看板列(todo/doing/done)")
    task_type: str | None = Field(default="manual", description="任务类型(auto_register/manual)")
    auto_generated: bool = Field(default=False, description="是否自动生成")


class ItineraryUpdateSchema(ItineraryCreateSchema):
    """更新行程方案模型"""

    pass


class ItineraryOutSchema(ItineraryCreateSchema, BaseSchema, UserBySchema):
    """行程方案响应模型"""

    model_config = ConfigDict(from_attributes=True)

    itinerary_status: str = Field(default="draft", description="状态")
    is_synced: bool = Field(default=False, description="是否已同步")
    board_column: str | None = Field(default="todo", description="看板列")
    task_type: str | None = Field(default="manual", description="任务类型")
    auto_generated: bool = Field(default=False, description="是否自动生成")


class ItineraryQuerySchema(BaseSchema):
    """行程方案查询参数"""

    consultation_id: int | None = Field(default=None, description="咨询会ID")
    team_id: int | None = Field(default=None, description="招生组ID")
    itinerary_name: str | None = Field(default=None, description="行程方案名称")
    itinerary_status: str | None = Field(default=None, description="状态")
    board_column: str | None = Field(default=None, description="看板列")
    start_date_begin: DateStr | None = Field(default=None, description="开始日期-起")
    start_date_end: DateStr | None = Field(default=None, description="开始日期-止")


class ItinerarySyncSchema(BaseSchema):
    """同步到日历模型"""

    calendar_type: str = Field(default="google", description="日历类型(google/outlook/apple)")
