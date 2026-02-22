from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema


class JobCreateSchema(BaseModel):
    """执行日志创建模型"""

    job_id: str = Field(..., description="任务ID")
    job_name: str | None = Field(default=None, description="任务名称")
    trigger_type: str | None = Field(default=None, description="触发方式")
    status: str = Field(default="pending", description="执行状态")
    next_run_time: str | None = Field(default=None, description="下次执行时间")
    job_state: str | None = Field(default=None, description="任务状态信息")
    result: str | None = Field(default=None, description="执行结果")
    error: str | None = Field(default=None, description="错误信息")


class JobUpdateSchema(BaseModel):
    """执行日志更新模型"""

    status: str | None = Field(default=None, description="执行状态")
    next_run_time: str | None = Field(default=None, description="下次执行时间")
    job_state: str | None = Field(default=None, description="任务状态信息")
    result: str | None = Field(default=None, description="执行结果")
    error: str | None = Field(default=None, description="错误信息")


class JobOutSchema(JobCreateSchema, BaseSchema):
    """执行日志响应模型"""
    
    model_config = ConfigDict(from_attributes=True)
    ...



class JobQueryParam:
    """执行日志查询参数"""

    def __init__(
        self,
        job_id: str | None = Query(None, description="任务ID"),
        job_name: str | None = Query(None, description="任务名称"),
        status: str | None = Query(None, description="执行状态"),
        trigger_type: str | None = Query(None, description="触发方式"),
    ) -> None:
        self.job_id = (QueueEnum.eq.value, job_id)
        self.job_name = (QueueEnum.like.value, job_name)
        self.status = (QueueEnum.eq.value, status)
        self.trigger_type = (QueueEnum.eq.value, trigger_type)
