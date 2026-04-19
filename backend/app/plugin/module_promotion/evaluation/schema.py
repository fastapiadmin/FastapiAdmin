"""
表彰评优 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr, DateStr


class EvaluationCreateSchema(BaseModel):
    """新增表彰评优模型"""

    activity_id: int | None = Field(default=None, description="关联活动ID")
    activity_name: str | None = Field(default=None, description="关联活动名称", max_length=200)

    evaluation_level: str = Field(default="individual", description="评选级别")
    evaluation_type: str | None = Field(default=None, description="评选类型", max_length=100)
    evaluation_title: str = Field(..., description="表彰标题", max_length=500)

    personnel_id: int | None = Field(default=None, description="被表彰人员ID")
    personnel_name: str | None = Field(default=None, description="被表彰人员姓名", max_length=100)

    team_id: int | None = Field(default=None, description="被表彰团队ID")
    team_name: str | None = Field(default=None, description="被表彰团队名称", max_length=200)

    org_team_id: int | None = Field(default=None, description="所属招生组ID")
    org_team_name: str | None = Field(default=None, description="所属招生组名称", max_length=200)

    award_name: str | None = Field(default=None, description="奖项名称", max_length=200)
    award_level: str | None = Field(default=None, description="奖项级别", max_length=50)

    evaluation_content: str | None = Field(default=None, description="评选内容/先进事迹")

    evidence_urls: list[str] | None = Field(default=None, description="佐证材料URL列表")
    evidence_names: list[str] | None = Field(default=None, description="佐证材料名称列表")

    reward_type: str | None = Field(default=None, description="奖励类型", max_length=100)
    reward_amount: float | None = Field(default=None, ge=0, description="奖励金额")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")


class EvaluationUpdateSchema(EvaluationCreateSchema):
    """更新表彰评优模型"""
    pass


class EvaluationOutSchema(EvaluationCreateSchema, BaseSchema, UserBySchema):
    """表彰评优响应模型"""

    model_config = ConfigDict(from_attributes=True)

    evaluation_no: str | None = Field(default=None, description="表彰单号")
    evaluation_status: str | None = Field(default=None, description="评选状态")
    submit_time: DateTimeStr | None = Field(default=None, description="提交时间")
    submitter_id: int | None = Field(default=None, description="提交人ID")
    submitter_name: str | None = Field(default=None, description="提交人姓名")
    review_comment: str | None = Field(default=None, description="审核意见")
    reviewer_id: int | None = Field(default=None, description="审核人ID")
    reviewer_name: str | None = Field(default=None, description="审核人姓名")
    review_time: DateTimeStr | None = Field(default=None, description="审核时间")
    approval_comment: str | None = Field(default=None, description="批准意见")
    approver_id: int | None = Field(default=None, description="批准人ID")
    approver_name: str | None = Field(default=None, description="批准人姓名")
    approval_time: DateTimeStr | None = Field(default=None, description="批准时间")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class EvaluationQuerySchema(BaseModel):
    """表彰评优查询参数模型"""

    def __init__(
        self,
        evaluation_no: str | None = Query(None, description="表彰单号"),
        evaluation_title: str | None = Query(None, description="表彰标题"),
        evaluation_level: str | None = Query(None, description="评选级别"),
        evaluation_type: str | None = Query(None, description="评选类型"),
        activity_id: int | None = Query(None, description="关联活动ID"),
        personnel_id: int | None = Query(None, description="被表彰人员ID"),
        personnel_name: str | None = Query(None, description="被表彰人员姓名"),
        team_id: int | None = Query(None, description="被表彰团队ID"),
        team_name: str | None = Query(None, description="被表彰团队名称"),
        org_team_id: int | None = Query(None, description="所属招生组ID"),
        evaluation_status: str | None = Query(None, description="评选状态"),
        submit_time_begin: DateStr | None = Query(None, description="提交时间范围-开始"),
        submit_time_end: DateStr | None = Query(None, description="提交时间范围-结束"),
    ) -> None:
        from app.common.enums import QueueEnum

        if evaluation_no:
            self.evaluation_no = (QueueEnum.like.value, evaluation_no)
        if evaluation_title:
            self.evaluation_title = (QueueEnum.like.value, evaluation_title)
        if evaluation_level:
            self.evaluation_level = (QueueEnum.eq.value, evaluation_level)
        if evaluation_type:
            self.evaluation_type = (QueueEnum.eq.value, evaluation_type)
        if activity_id is not None:
            self.activity_id = (QueueEnum.eq.value, activity_id)
        if personnel_id is not None:
            self.personnel_id = (QueueEnum.eq.value, personnel_id)
        if personnel_name:
            self.personnel_name = (QueueEnum.like.value, personnel_name)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if team_name:
            self.team_name = (QueueEnum.like.value, team_name)
        if org_team_id is not None:
            self.org_team_id = (QueueEnum.eq.value, org_team_id)
        if evaluation_status:
            self.evaluation_status = (QueueEnum.eq.value, evaluation_status)
        if submit_time_begin and submit_time_end:
            self.submit_time = (QueueEnum.between.value, (submit_time_begin, submit_time_end))