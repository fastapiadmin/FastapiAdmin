"""
总结上传 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class SummaryCreateSchema(BaseModel):
    """新增总结上传模型"""

    activity_id: int | None = Field(default=None, description="活动ID")
    summary_type: str | None = Field(default=None, description="总结类型")
    title: str | None = Field(default=None, description="标题")
    content: str | None = Field(default=None, description="内容")
    photo_urls: dict | None = Field(default=None, description="照片URLs")
    attachment_urls: dict | None = Field(default=None, description="附件URLs")
    upload_by: int | None = Field(default=None, description="上传人ID")
    upload_time: DateTimeStr | None = Field(default=None, description="上传时间")
    is_archived: int | None = Field(default=None, description="是否归档")
    recruitment_results: str | None = Field(default=None, description="招生成果")
    travel_expense: float | None = Field(default=None, description="差旅费用")


class SummaryUpdateSchema(SummaryCreateSchema):
    """更新总结上传模型"""

    pass


class SummaryOutSchema(SummaryCreateSchema, BaseSchema, UserBySchema):
    """总结上传响应模型"""

    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(default=None, description="状态")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class SummaryQuerySchema(BaseModel):
    """总结上传查询参数模型"""

    def __init__(
        self,
        activity_id: int | None = Query(None, description="活动ID"),
        summary_type: str | None = Query(None, description="总结类型"),
    ) -> None:
        from app.common.enums import QueueEnum

        if activity_id is not None:
            self.activity_id = (QueueEnum.eq.value, activity_id)
        if summary_type:
            self.summary_type = (QueueEnum.eq.value, summary_type)
