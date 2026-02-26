from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr, datetime_validator


class NodeCreateSchema(BaseModel):
    """
    节点创建/编辑时只设置节点基本信息，节点参数在执行时设置
    """

    name: str = Field(..., max_length=64, description="任务名称")
    func: str | None = Field(default=None, description="代码块")
    args: str | None = Field(default=None, description="位置参数")
    kwargs: str | None = Field(default=None, description="关键字参数")
    coalesce: bool | None = Field(default=False, description="是否合并运行:是否在多个运行时间到期时仅运行作业一次")
    max_instances: int | None = Field(default=1, ge=1, description="最大实例数:允许的最大并发执行实例数")
    jobstore: str | None = Field(default="default", max_length=64, description="任务存储")
    executor: str | None = Field(default="default", max_length=64, description="任务执行器:将运行此作业的执行程序的名称",)
    start_date: str | None = Field(default=None, description="开始时间")
    end_date: str | None = Field(default=None, description="结束时间")
    code: str | None = Field(default=None, description="节点编码")

    @model_validator(mode="after")
    def _validate_func(self):
        if not self.func or not self.func.strip():
            raise ValueError("必须提供代码块(func)")
        return self


class NodeUpdateSchema(NodeCreateSchema):
    """节点更新模型"""


class NodeOutSchema(NodeCreateSchema, BaseSchema, UserBySchema):
    """节点响应模型"""

    trigger: str | None = Field(default=None, description="触发器")
    trigger_args: str | None = Field(default=None, description="触发器参数")

    model_config = ConfigDict(from_attributes=True)


class NodeQueryParam:
    """节点查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="节点名称"),
        status: str | None = Query(None, description="状态: 启动,停止"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        updated_time: list[DateTimeStr] | None = Query(
            None,
            description="更新时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:

        self.name = (QueueEnum.like.value, name)
        self.created_id = (QueueEnum.eq.value, created_id)
        self.updated_id = (QueueEnum.eq.value, updated_id)
        self.status = (QueueEnum.eq.value, status)

        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = (QueueEnum.between.value, (updated_time[0], updated_time[1]))


class NodeExecuteSchema(BaseModel):
    """节点执行参数"""

    trigger: str = Field(default="now", description="触发方式: now/cron/interval/date")
    trigger_args: str | None = Field(default=None, description="触发器参数")
    start_date: str | None = Field(default=None, description="开始时间")
    end_date: str | None = Field(default=None, description="结束时间")

    @field_validator("trigger")
    @classmethod
    def _validate_trigger(cls, v: str) -> str:
        allowed = {"now", "cron", "interval", "date"}
        v = v.strip()
        if v not in allowed:
            raise ValueError("触发器必须为 now/cron/interval/date")
        return v

    @model_validator(mode="after")
    def _validate_trigger_args(self):
        """非立即执行时必须提供触发器参数"""
        if self.trigger != "now" and not self.trigger_args:
            raise ValueError("非立即执行时必须提供触发器参数")
        return self

    @model_validator(mode="after")
    def _validate_dates(self):
        """跨字段校验：结束时间不得早于开始时间。"""
        if self.start_date and self.end_date:
            try:
                start = datetime_validator(self.start_date)
                end = datetime_validator(self.end_date)
            except Exception:
                raise ValueError("时间格式必须为 YYYY-MM-DD HH:MM:SS")
            if end < start:
                raise ValueError("结束时间不能早于开始时间")
        return self
