"""
总结上传 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr, DateStr


class SummaryCreateSchema(BaseModel):
    """新增总结上传模型"""

    activity_id: int | None = Field(default=None, description="关联活动ID")
    activity_name: str | None = Field(default=None, description="关联活动名称", max_length=200)

    trip_id: int | None = Field(default=None, description="关联行程ID")
    trip_no: str | None = Field(default=None, description="行程单号", max_length=50)

    personnel_id: int | None = Field(default=None, description="招生人员ID")
    personnel_name: str | None = Field(default=None, description="招生人员姓名", max_length=100)

    team_id: int | None = Field(default=None, description="招生组ID")
    team_name: str | None = Field(default=None, description="招生组名称", max_length=200)

    summary_title: str | None = Field(default=None, description="总结标题", max_length=500)
    summary_content: str | None = Field(default=None, description="总结内容")

    attachment_urls: list[str] | None = Field(default=None, description="附件URL列表")
    attachment_names: list[str] | None = Field(default=None, description="附件名称列表")

    visitor_count: int | None = Field(default=None, ge=0, description="来访人数")
    consultation_count: int | None = Field(default=None, ge=0, description="咨询人数")
    registration_count: int | None = Field(default=None, ge=0, description="报名人数")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")


class SummaryUpdateSchema(SummaryCreateSchema):
    """更新总结上传模型"""
    pass


class SummaryOutSchema(SummaryCreateSchema, BaseSchema, UserBySchema):
    """总结上传响应模型"""

    model_config = ConfigDict(from_attributes=True)

    summary_no: str | None = Field(default=None, description="总结单号")
    summary_status: str | None = Field(default=None, description="总结状态")
    submit_time: DateTimeStr | None = Field(default=None, description="提交时间")
    approval_comment: str | None = Field(default=None, description="审批意见")
    approver_id: int | None = Field(default=None, description="审批人ID")
    approver_name: str | None = Field(default=None, description="审批人姓名")
    approval_time: DateTimeStr | None = Field(default=None, description="审批时间")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class SummaryQuerySchema(BaseModel):
    """总结上传查询参数模型"""

    def __init__(
        self,
        summary_no: str | None = Query(None, description="总结单号"),
        activity_id: int | None = Query(None, description="关联活动ID"),
        personnel_id: int | None = Query(None, description="招生人员ID"),
        personnel_name: str | None = Query(None, description="招生人员姓名"),
        team_id: int | None = Query(None, description="招生组ID"),
        summary_status: str | None = Query(None, description="总结状态"),
        submit_time_begin: DateStr | None = Query(None, description="提交时间范围-开始"),
        submit_time_end: DateStr | None = Query(None, description="提交时间范围-结束"),
    ) -> None:
        from app.common.enums import QueueEnum

        if summary_no:
            self.summary_no = (QueueEnum.like.value, summary_no)
        if activity_id is not None:
            self.activity_id = (QueueEnum.eq.value, activity_id)
        if personnel_id is not None:
            self.personnel_id = (QueueEnum.eq.value, personnel_id)
        if personnel_name:
            self.personnel_name = (QueueEnum.like.value, personnel_name)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if summary_status:
            self.summary_status = (QueueEnum.eq.value, summary_status)
        if submit_time_begin and submit_time_end:
            self.submit_time = (QueueEnum.between.value, (submit_time_begin, submit_time_end))