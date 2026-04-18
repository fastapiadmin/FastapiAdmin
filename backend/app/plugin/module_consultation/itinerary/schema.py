"""
行程方案管理 - 数据验证Schema
"""
from datetime import date, datetime
from typing import Optional

from pydantic import ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class ItineraryCreateSchema(BaseSchema):
    """新增行程方案模型"""

    name: str = Field(..., description="行程方案名称", min_length=2, max_length=200)
    description: Optional[str] = Field(default=None, description="行程方案描述")
    university_id: Optional[int] = Field(default=None, description="高校ID")
    team_id: Optional[int] = Field(default=None, description="招生组ID")
    start_date: DateStr = Field(..., description="开始日期")
    end_date: DateStr = Field(..., description="结束日期")
    consultation_ids: Optional[list[int]] = Field(default=None, description="咨询会ID列表")
    transportation_plan: Optional[list[dict]] = Field(default=None, description="交通方案")
    accommodation_plan: Optional[list[dict]] = Field(default=None, description="住宿方案")
    total_distance: Optional[float] = Field(default=None, description="总距离")
    estimated_duration: Optional[int] = Field(default=None, description="预计时长")
    estimated_cost: Optional[float] = Field(default=None, description="预计费用")


class ItineraryUpdateSchema(ItineraryCreateSchema):
    """更新行程方案模型"""
    pass


class ItineraryOutSchema(ItineraryCreateSchema, BaseSchema, UserBySchema):
    """行程方案响应模型"""

    model_config = ConfigDict(from_attributes=True)

    consultation_details: Optional[list] = Field(default=None, description="咨询会详情")
    status: str = Field(default="draft", description="状态")
    is_synced: bool = Field(default=False, description="是否已同步")


class ItineraryQuerySchema(BaseSchema):
    """行程方案查询参数"""

    name: Optional[str] = Field(default=None, description="行程方案名称")
    university_id: Optional[int] = Field(default=None, description="高校ID")
    team_id: Optional[int] = Field(default=None, description="招生组ID")
    status: Optional[str] = Field(default=None, description="状态")
    start_date_begin: Optional[DateStr] = Field(default=None, description="开始日期-起")
    start_date_end: Optional[DateStr] = Field(default=None, description="开始日期-止")
    end_date_begin: Optional[DateStr] = Field(default=None, description="结束日期-起")
    end_date_end: Optional[DateStr] = Field(default=None, description="结束日期-止")


class ItinerarySyncSchema(BaseSchema):
    """同步到日历模型"""

    calendar_type: str = Field(default="google", description="日历类型(google/outlook/apple)")
