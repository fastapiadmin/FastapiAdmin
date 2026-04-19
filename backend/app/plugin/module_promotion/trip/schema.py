"""
行程报备 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class TripCreateSchema(BaseModel):
    """新增行程报备模型"""

    activity_id: int | None = Field(default=None, description="关联活动ID")
    activity_name: str | None = Field(default=None, description="关联活动名称", max_length=200)

    team_id: int | None = Field(default=None, description="招生组ID")
    team_name: str | None = Field(default=None, description="招生组名称", max_length=200)

    personnel_id: int | None = Field(default=None, description="行程人员ID")
    personnel_name: str | None = Field(default=None, description="行程人员姓名", max_length=100)

    departure_date: DateStr = Field(..., description="出发日期")
    departure_time: str | None = Field(default=None, description="出发时间", max_length=10)
    return_date: DateStr | None = Field(default=None, description="返回日期")
    return_time: str | None = Field(default=None, description="返回时间", max_length=10)

    departure_province: str | None = Field(default=None, description="出发省份", max_length=50)
    departure_city: str | None = Field(default=None, description="出发城市", max_length=50)
    departure_address: str | None = Field(default=None, description="出发详细地址", max_length=500)

    destination_province: str | None = Field(default=None, description="目的省份", max_length=50)
    destination_city: str | None = Field(default=None, description="目的城市", max_length=50)
    destination_address: str | None = Field(default=None, description="目的详细地址", max_length=500)

    transportation_type: str | None = Field(default=None, description="交通类型")
    transportation_no: str | None = Field(default=None, description="航班/车次号", max_length=100)

    enable_location_sharing: bool = Field(default=False, description="启用位置共享")

    trip_purpose: str | None = Field(default=None, description="行程目的")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")


class TripUpdateSchema(TripCreateSchema):
    """更新行程报备模型"""
    pass


class TripOutSchema(TripCreateSchema, BaseSchema, UserBySchema):
    """行程报备响应模型"""

    model_config = ConfigDict(from_attributes=True)

    trip_no: str | None = Field(default=None, description="行程单号")
    trip_status: str | None = Field(default=None, description="行程状态")
    last_location_time: DateTimeStr | None = Field(default=None, description="最后位置更新时间")
    last_latitude: float | None = Field(default=None, description="最后位置纬度")
    last_longitude: float | None = Field(default=None, description="最后位置经度")
    last_location_address: str | None = Field(default=None, description="最后位置地址")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class TripQuerySchema(BaseModel):
    """行程报备查询参数模型"""

    def __init__(
        self,
        trip_no: str | None = Query(None, description="行程单号"),
        activity_id: int | None = Query(None, description="关联活动ID"),
        team_id: int | None = Query(None, description="招生组ID"),
        personnel_id: int | None = Query(None, description="行程人员ID"),
        personnel_name: str | None = Query(None, description="行程人员姓名"),
        departure_province: str | None = Query(None, description="出发省份"),
        departure_city: str | None = Query(None, description="出发城市"),
        destination_province: str | None = Query(None, description="目的省份"),
        destination_city: str | None = Query(None, description="目的城市"),
        trip_status: str | None = Query(None, description="行程状态"),
        departure_date_begin: DateStr | None = Query(None, description="出发日期范围-开始"),
        departure_date_end: DateStr | None = Query(None, description="出发日期范围-结束"),
    ) -> None:
        from app.common.enums import QueueEnum

        if trip_no:
            self.trip_no = (QueueEnum.like.value, trip_no)
        if activity_id is not None:
            self.activity_id = (QueueEnum.eq.value, activity_id)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if personnel_id is not None:
            self.personnel_id = (QueueEnum.eq.value, personnel_id)
        if personnel_name:
            self.personnel_name = (QueueEnum.like.value, personnel_name)
        if departure_province:
            self.departure_province = (QueueEnum.eq.value, departure_province)
        if departure_city:
            self.departure_city = (QueueEnum.eq.value, departure_city)
        if destination_province:
            self.destination_province = (QueueEnum.eq.value, destination_province)
        if destination_city:
            self.destination_city = (QueueEnum.eq.value, destination_city)
        if trip_status:
            self.trip_status = (QueueEnum.eq.value, trip_status)
        if departure_date_begin and departure_date_end:
            self.departure_date = (QueueEnum.between.value, (departure_date_begin, departure_date_end))