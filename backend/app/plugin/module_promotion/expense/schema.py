"""
费用报销 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class ExpenseCreateSchema(BaseModel):
    """新增费用报销模型"""

    activity_id: int | None = Field(default=None, description="关联活动ID")
    activity_name: str | None = Field(default=None, description="关联活动名称", max_length=200)

    trip_id: int | None = Field(default=None, description="关联行程ID")
    trip_no: str | None = Field(default=None, description="行程单号", max_length=50)

    team_id: int | None = Field(default=None, description="招生组ID")
    team_name: str | None = Field(default=None, description="招生组名称", max_length=200)

    applicant_id: int | None = Field(default=None, description="申请人ID")
    applicant_name: str | None = Field(default=None, description="申请人姓名", max_length=100)

    expense_type: str = Field(default="other", description="费用类型")
    expense_amount: float = Field(default=0.0, ge=0, description="报销金额")

    expense_date: DateStr = Field(..., description="费用日期")
    expense_description: str | None = Field(default=None, description="费用说明")
    invoice_count: int = Field(default=0, ge=0, description="发票数量")
    has_invoice: bool = Field(default=False, description="是否有发票")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")

    @field_validator("expense_amount")
    @classmethod
    def validate_expense_amount(cls, v: float) -> float:
        """验证报销金额"""
        if v < 0:
            raise ValueError("报销金额不能为负数")
        return v


class ExpenseUpdateSchema(ExpenseCreateSchema):
    """更新费用报销模型"""
    pass


class ExpenseOutSchema(ExpenseCreateSchema, BaseSchema, UserBySchema):
    """费用报销响应模型"""

    model_config = ConfigDict(from_attributes=True)

    expense_no: str | None = Field(default=None, description="报销单号")
    approval_status: str | None = Field(default=None, description="审批状态")
    approval_comment: str | None = Field(default=None, description="审批意见")
    approver_id: int | None = Field(default=None, description="审批人ID")
    approver_name: str | None = Field(default=None, description="审批人姓名")
    approval_time: DateTimeStr | None = Field(default=None, description="审批时间")
    reimburse_time: DateTimeStr | None = Field(default=None, description="报销时间")
    reimbursement_account: str | None = Field(default=None, description="报销账户")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class ExpenseQuerySchema(BaseModel):
    """费用报销查询参数模型"""

    def __init__(
        self,
        expense_no: str | None = Query(None, description="报销单号"),
        expense_type: str | None = Query(None, description="费用类型"),
        activity_id: int | None = Query(None, description="关联活动ID"),
        team_id: int | None = Query(None, description="招生组ID"),
        applicant_id: int | None = Query(None, description="申请人ID"),
        applicant_name: str | None = Query(None, description="申请人姓名"),
        approval_status: str | None = Query(None, description="审批状态"),
        expense_date_begin: DateStr | None = Query(None, description="费用日期范围-开始"),
        expense_date_end: DateStr | None = Query(None, description="费用日期范围-结束"),
    ) -> None:
        from app.common.enums import QueueEnum

        if expense_no:
            self.expense_no = (QueueEnum.like.value, expense_no)
        if expense_type:
            self.expense_type = (QueueEnum.eq.value, expense_type)
        if activity_id is not None:
            self.activity_id = (QueueEnum.eq.value, activity_id)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if applicant_id is not None:
            self.applicant_id = (QueueEnum.eq.value, applicant_id)
        if applicant_name:
            self.applicant_name = (QueueEnum.like.value, applicant_name)
        if approval_status:
            self.approval_status = (QueueEnum.eq.value, approval_status)
        if expense_date_begin and expense_date_end:
            self.expense_date = (QueueEnum.between.value, (expense_date_begin, expense_date_end))