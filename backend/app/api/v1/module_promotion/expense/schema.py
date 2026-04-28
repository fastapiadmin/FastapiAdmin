"""
费用报销 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class ExpenseCreateSchema(BaseModel):
    """新增费用报销模型"""

    expense_no: str | None = Field(default=None, description="报销单号")
    applicant_id: int | None = Field(default=None, description="申请人ID")
    team_id: int | None = Field(default=None, description="招生组ID")
    activity_id: int | None = Field(default=None, description="活动ID")
    expense_type: str | None = Field(default=None, description="费用类型")
    amount: float | None = Field(default=None, description="金额")
    expense_date: DateStr | None = Field(default=None, description="费用日期")
    description: str | None = Field(default=None, description="描述")
    attachments: dict | None = Field(default=None, description="附件")
    approval_status: str | None = Field(default=None, description="审批状态")
    approval_comment: str | None = Field(default=None, description="审批意见")
    approval_time: DateTimeStr | None = Field(default=None, description="审批时间")
    approval_by: int | None = Field(default=None, description="审批人ID")
    reimburse_status: str | None = Field(default=None, description="报销状态")
    reimburse_time: DateTimeStr | None = Field(default=None, description="报销时间")


class ExpenseUpdateSchema(ExpenseCreateSchema):
    """更新费用报销模型"""

    pass


class ExpenseOutSchema(ExpenseCreateSchema, BaseSchema, UserBySchema):
    """费用报销响应模型"""

    model_config = ConfigDict(from_attributes=True)

    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class ExpenseQuerySchema(BaseModel):
    """费用报销查询参数模型"""

    def __init__(
        self,
        expense_no: str | None = Query(None, description="报销单号"),
        applicant_id: int | None = Query(None, description="申请人ID"),
        team_id: int | None = Query(None, description="招生组ID"),
        activity_id: int | None = Query(None, description="活动ID"),
        expense_type: str | None = Query(None, description="费用类型"),
        approval_status: str | None = Query(None, description="审批状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if expense_no:
            self.expense_no = (QueueEnum.like.value, expense_no)
        if applicant_id is not None:
            self.applicant_id = (QueueEnum.eq.value, applicant_id)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if activity_id is not None:
            self.activity_id = (QueueEnum.eq.value, activity_id)
        if expense_type:
            self.expense_type = (QueueEnum.eq.value, expense_type)
        if approval_status:
            self.approval_status = (QueueEnum.eq.value, approval_status)
