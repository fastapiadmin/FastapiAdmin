"""
审批记录 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class ApprovalRecordCreateSchema(BaseModel):
    """新增审批记录模型"""

    activity_apply_id: int = Field(..., description="活动申请ID")
    approval_level: int = Field(..., description="审批级别")
    approval_action: str = Field(..., description="审批动作(approved/rejected)")
    approver_id: int | None = Field(default=None, description="审批人ID")
    approver_name: str | None = Field(default=None, description="审批人姓名")
    approval_comment: str | None = Field(default=None, description="审批意见")
    approval_time: DateTimeStr | None = Field(default=None, description="审批时间")


class ApprovalRecordUpdateSchema(ApprovalRecordCreateSchema):
    """更新审批记录模型"""

    pass


class ApprovalRecordOutSchema(ApprovalRecordCreateSchema, BaseSchema, UserBySchema):
    """审批记录响应模型"""

    model_config = ConfigDict(from_attributes=True)


class ApprovalRecordQuerySchema(BaseModel):
    """审批记录查询参数模型"""

    def __init__(
        self,
        activity_apply_id: int | None = Query(None, description="活动申请ID"),
        approval_level: int | None = Query(None, description="审批级别"),
        approval_action: str | None = Query(None, description="审批动作"),
    ) -> None:
        from app.common.enums import QueueEnum

        if activity_apply_id is not None:
            self.activity_apply_id = (QueueEnum.eq.value, activity_apply_id)
        if approval_level is not None:
            self.approval_level = (QueueEnum.eq.value, approval_level)
        if approval_action:
            self.approval_action = (QueueEnum.eq.value, approval_action)
