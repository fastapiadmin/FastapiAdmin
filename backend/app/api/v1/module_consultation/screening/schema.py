"""
咨询会筛选匹配 - 数据验证Schema
"""
from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class ScreeningFilterCreateSchema(BaseModel):
    """新增筛选条件模型"""

    name: str = Field(..., description="筛选名称", min_length=2, max_length=100)
    province: str | None = Field(default=None, description="省份筛选")
    city: str | None = Field(default=None, description="城市筛选")
    start_date_begin: DateStr | None = Field(default=None, description="开始日期范围-开始")
    start_date_end: DateStr | None = Field(default=None, description="开始日期范围-结束")
    organizer_type: str | None = Field(default=None, description="主办方类型")
    university_count_min: int | None = Field(default=None, description="高校数量最小值")
    university_count_max: int | None = Field(default=None, description="高校数量最大值")
    booth_fee_min: float | None = Field(default=None, description="展位费最小值")
    booth_fee_max: float | None = Field(default=None, description="展位费最大值")
    estimated_visitors_min: int | None = Field(default=None, description="预计人数最小值")
    estimated_visitors_max: int | None = Field(default=None, description="预计人数最大值")
    compliance_score_min: int | None = Field(default=None, description="合规评分最小值")
    compliance_score_max: int | None = Field(default=None, description="合规评分最大值")
    compliance_level: str | None = Field(default=None, description="合规等级")
    source_type: str | None = Field(default=None, description="信息来源")
    status: str | None = Field(default=None, description="状态")
    order_by: str | None = Field(default="created_time", description="排序字段")
    order_direction: str | None = Field(default="desc", description="排序方向")
    is_default: bool = Field(default=False, description="是否默认筛选")


class ScreeningFilterUpdateSchema(ScreeningFilterCreateSchema):
    """更新筛选条件模型"""
    pass


class ScreeningFilterOutSchema(ScreeningFilterCreateSchema, BaseSchema, UserBySchema):
    """筛选条件响应模型"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class ScreeningFilterQueryParam:
    """筛选条件查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="筛选名称"),
        is_default: bool | None = Query(None, description="是否默认筛选"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
        ),
    ) -> None:
        from app.common.enums import QueueEnum

        if name:
            self.name = (QueueEnum.like.value, name)
        if is_default is not None:
            self.is_default = (QueueEnum.eq.value, is_default)
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
