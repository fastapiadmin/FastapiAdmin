"""
活动打卡 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class CheckinCreateSchema(BaseModel):
    """新增活动打卡模型"""

    activity_id: int | None = Field(default=None, description="关联活动ID")
    activity_name: str | None = Field(default=None, description="关联活动名称", max_length=200)

    trip_id: int | None = Field(default=None, description="关联行程ID")
    trip_no: str | None = Field(default=None, description="行程单号", max_length=50)

    personnel_id: int | None = Field(default=None, description="招生人员ID")
    personnel_name: str | None = Field(default=None, description="招生人员姓名", max_length=100)

    team_id: int | None = Field(default=None, description="招生组ID")
    team_name: str | None = Field(default=None, description="招生组名称", max_length=200)

    checkin_time: DateTimeStr = Field(..., description="打卡时间")

    checkin_location: str | None = Field(default=None, description="打卡地点", max_length=500)
    latitude: float | None = Field(default=None, description="纬度")
    longitude: float | None = Field(default=None, description="经度")

    checkin_type: str = Field(default="location", description="打卡类型")

    checkin_content: str | None = Field(default=None, description="打卡内容")
    checkin_images: str | None = Field(default=None, description="打卡图片(JSON数组)")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")


class CheckinUpdateSchema(CheckinCreateSchema):
    """更新活动打卡模型"""
    pass


class CheckinOutSchema(CheckinCreateSchema, BaseSchema, UserBySchema):
    """活动打卡响应模型"""

    model_config = ConfigDict(from_attributes=True)

    checkin_no: str | None = Field(default=None, description="打卡单号")
    checkin_status: str | None = Field(default=None, description="打卡状态")
    validated_by: int | None = Field(default=None, description="验证人ID")
    validated_by_name: str | None = Field(default=None, description="验证人姓名")
    validated_time: DateTimeStr | None = Field(default=None, description="验证时间")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class CheckinQuerySchema(BaseModel):
    """活动打卡查询参数模型"""

    def __init__(
        self,
        checkin_no: str | None = Query(None, description="打卡单号"),
        activity_id: int | None = Query(None, description="关联活动ID"),
        trip_id: int | None = Query(None, description="关联行程ID"),
        personnel_id: int | None = Query(None, description="招生人员ID"),
        personnel_name: str | None = Query(None, description="招生人员姓名"),
        team_id: int | None = Query(None, description="招生组ID"),
        checkin_status: str | None = Query(None, description="打卡状态"),
        checkin_type: str | None = Query(None, description="打卡类型"),
        checkin_time_begin: DateStr | None = Query(None, description="打卡时间范围-开始"),
        checkin_time_end: DateStr | None = Query(None, description="打卡时间范围-结束"),
    ) -> None:
        from app.common.enums import QueueEnum

        if checkin_no:
            self.checkin_no = (QueueEnum.like.value, checkin_no)
        if activity_id is not None:
            self.activity_id = (QueueEnum.eq.value, activity_id)
        if trip_id is not None:
            self.trip_id = (QueueEnum.eq.value, trip_id)
        if personnel_id is not None:
            self.personnel_id = (QueueEnum.eq.value, personnel_id)
        if personnel_name:
            self.personnel_name = (QueueEnum.like.value, personnel_name)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if checkin_status:
            self.checkin_status = (QueueEnum.eq.value, checkin_status)
        if checkin_type:
            self.checkin_type = (QueueEnum.eq.value, checkin_type)
        if checkin_time_begin and checkin_time_end:
            self.checkin_time = (QueueEnum.between.value, (checkin_time_begin, checkin_time_end))