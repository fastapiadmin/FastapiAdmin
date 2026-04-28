"""
活动打卡 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class CheckinCreateSchema(BaseModel):
    """新增活动打卡模型"""

    activity_id: int | None = Field(default=None, description="活动ID")
    personnel_id: int | None = Field(default=None, description="人员ID")
    checkin_time: DateTimeStr | None = Field(default=None, description="打卡时间")
    checkin_type: str | None = Field(default=None, description="打卡类型")
    location: str | None = Field(default=None, description="位置")
    longitude: float | None = Field(default=None, description="经度")
    latitude: float | None = Field(default=None, description="纬度")
    photo_urls: dict | None = Field(default=None, description="照片URLs")
    remarks: str | None = Field(default=None, description="备注")


class CheckinUpdateSchema(CheckinCreateSchema):
    """更新活动打卡模型"""

    pass


class CheckinOutSchema(CheckinCreateSchema, BaseSchema, UserBySchema):
    """活动打卡响应模型"""

    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(default=None, description="状态")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class CheckinQuerySchema(BaseModel):
    """活动打卡查询参数模型"""

    def __init__(
        self,
        activity_id: int | None = Query(None, description="活动ID"),
        personnel_id: int | None = Query(None, description="人员ID"),
        checkin_type: str | None = Query(None, description="打卡类型"),
    ) -> None:
        from app.common.enums import QueueEnum

        if activity_id is not None:
            self.activity_id = (QueueEnum.eq.value, activity_id)
        if personnel_id is not None:
            self.personnel_id = (QueueEnum.eq.value, personnel_id)
        if checkin_type:
            self.checkin_type = (QueueEnum.eq.value, checkin_type)
