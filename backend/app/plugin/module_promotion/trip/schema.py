"""
行程报备 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class TripCreateSchema(BaseModel):
    """新增行程报备模型"""

    personnel_id: int | None = Field(default=None, description="人员ID")
    trip_name: str | None = Field(default=None, description="行程名称")
    departure_location: str | None = Field(default=None, description="出发地")
    destination: str | None = Field(default=None, description="目的地")
    plan_start_time: DateTimeStr | None = Field(default=None, description="计划开始时间")
    plan_end_time: DateTimeStr | None = Field(default=None, description="计划结束时间")
    transportation: str | None = Field(default=None, description="交通方式")
    report_status: str | None = Field(default=None, description="报备状态")
    location_sharing: int | None = Field(default=None, description="位置共享")


class TripUpdateSchema(TripCreateSchema):
    """更新行程报备模型"""
    pass


class TripOutSchema(TripCreateSchema, BaseSchema, UserBySchema):
    """行程报备响应模型"""

    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(default=None, description="状态")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class TripQuerySchema(BaseModel):
    """行程报备查询参数模型"""

    def __init__(
        self,
        personnel_id: int | None = Query(None, description="人员ID"),
        trip_name: str | None = Query(None, description="行程名称"),
        report_status: str | None = Query(None, description="报备状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if personnel_id is not None:
            self.personnel_id = (QueueEnum.eq.value, personnel_id)
        if trip_name:
            self.trip_name = (QueueEnum.like.value, trip_name)
        if report_status:
            self.report_status = (QueueEnum.eq.value, report_status)
