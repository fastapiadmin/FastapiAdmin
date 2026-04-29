"""
批次管理 - Pydantic Schema
"""

from datetime import date, datetime

from pydantic import Field

from app.core.base_schema import BaseSchema
from app.common.response import ResponseSchema


class BatchCreateSchema(BaseSchema):
    """批次创建模型"""

    batch_name: str = Field(..., max_length=100, description="批次名称")
    year: int = Field(..., ge=2020, le=2100, description="年度")
    semester: str = Field(..., max_length=20, description="学期")
    description: str | None = Field(None, description="批次描述")
    recruitment_start: date | None = Field(None, description="招募开始日期")
    recruitment_end: date | None = Field(None, description="招募结束日期")
    activity_start: date | None = Field(None, description="活动开始日期")
    activity_end: date | None = Field(None, description="活动结束日期")
    registration_deadline: date | None = Field(None, description="报名截止日期")
    status: str = Field(default="draft", description="批次状态")
    review_type: str = Field(default="manual", description="审核方式")
    max_teams: int = Field(default=100, ge=1, description="最大团队数")
    min_team_members: int = Field(default=1, ge=1, description="团队最小人数")
    max_team_members: int = Field(default=10, ge=1, description="团队最大人数")
    require_training: bool = Field(default=True, description="是否需要培训")
    require_exam: bool = Field(default=True, description="是否需要考试")
    exam_pass_score: int = Field(default=60, ge=0, le=100, description="考试及格分数")
    require_insurance: bool = Field(default=True, description="是否需要保险")
    require_checkin: bool = Field(default=True, description="是否需要打卡")
    min_checkin_count: int = Field(default=3, ge=0, description="最少打卡次数")
    extra_config: dict | None = Field(None, description="扩展配置")
    is_active: bool = Field(default=True, description="是否激活")


class BatchUpdateSchema(BatchCreateSchema):
    """批次更新模型"""

    pass


class BatchOutSchema(BaseSchema):
    """批次响应模型"""

    id: int
    batch_name: str
    year: int
    semester: str
    description: str | None
    recruitment_start: date | None
    recruitment_end: date | None
    activity_start: date | None
    activity_end: date | None
    registration_deadline: date | None
    status: str
    review_type: str
    max_teams: int
    min_team_members: int
    max_team_members: int
    require_training: bool
    require_exam: bool
    exam_pass_score: int
    require_insurance: bool
    require_checkin: bool
    min_checkin_count: int
    extra_config: dict | None
    is_active: bool
    created_time: datetime | None
    updated_time: datetime | None


class BatchQuerySchema(BaseSchema):
    """批次查询模型"""

    batch_name: str | None = Field(None, description="批次名称")
    year: int | None = Field(None, description="年度")
    semester: str | None = Field(None, description="学期")
    status: str | None = Field(None, description="批次状态")
    is_active: bool | None = Field(None, description="是否激活")


class BatchListResponse(ResponseSchema):
    """批次列表响应"""

    data: list[BatchOutSchema]
    total: int
