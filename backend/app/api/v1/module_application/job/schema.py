# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional
from fastapi import Query

from app.core.base_schema import BaseSchema, UserBySchema, TenantSchema, CustomerSchema
from app.core.validator import DateTimeStr, datetime_validator


class JobCreateSchema(BaseModel):
    """
    定时任务调度表对应pydantic模型
    """
    name: Optional[str] = Field(..., max_length=64, description='任务名称')
    func: str = Field(..., description='任务函数')
    trigger: str = Field(..., description='触发器:控制此作业计划的 trigger 对象')
    args: Optional[str] = Field(default=None, description='位置参数')
    kwargs: Optional[str] = Field(default=None, description='关键字参数')
    coalesce: Optional[bool] = Field(..., description='是否合并运行:是否在多个运行时间到期时仅运行作业一次')
    max_instances: Optional[int] = Field(default=1, ge=1, description='最大实例数:允许的最大并发执行实例数')
    jobstore: Optional[str] = Field(..., max_length=64, description='任务存储')
    executor: Optional[str] = Field(..., max_length=64, description='任务执行器:将运行此作业的执行程序的名称')
    trigger_args: Optional[str] = Field(default=None, description='触发器参数')
    start_date: Optional[str] = Field(default=None, description='开始时间')
    end_date: Optional[str] = Field(default=None, description='结束时间')
    description: Optional[str] = Field(default=None, max_length=255, description='描述')
    status: Optional[str] = Field(default=False, description='任务状态:启动,停止')

    @field_validator('trigger')
    @classmethod
    def _validate_trigger(cls, v: str) -> str:
        allowed = {'cron', 'interval', 'date'}
        v = v.strip()
        if v not in allowed:
            raise ValueError('触发器必须为 cron/interval/date')
        return v

    @model_validator(mode='after')
    def _validate_dates(self):
        """跨字段校验：结束时间不得早于开始时间。"""
        if self.start_date and self.end_date:
            try:
                start = datetime_validator(self.start_date)
                end = datetime_validator(self.end_date)
            except Exception:
                raise ValueError('时间格式必须为 YYYY-MM-DD HH:MM:SS')
            if end < start:
                raise ValueError('结束时间不能早于开始时间')
        return self


class JobUpdateSchema(JobCreateSchema):
    """定时任务更新模型"""
    ...
    

class JobOutSchema(JobCreateSchema, BaseSchema, UserBySchema, TenantSchema, CustomerSchema):
    """定时任务响应模型"""
    model_config = ConfigDict(from_attributes=True)
    ...


class JobLogCreateSchema(BaseModel):
    """
    定时任务调度日志表对应pydantic模型
    """

    model_config = ConfigDict(from_attributes=True)

    job_name: Optional[str] = Field(default=None, description='任务名称')
    job_group: Optional[str] = Field(default=None, description='任务组名')
    job_executor: Optional[str] = Field(default=None, description='任务执行器')
    invoke_target: Optional[str] = Field(default=None, description='调用目标字符串')
    job_args: Optional[str] = Field(default=None, description='位置参数')
    job_kwargs: Optional[str] = Field(default=None, description='关键字参数')
    job_trigger: Optional[str] = Field(default=None, description='任务触发器')
    job_message: Optional[str] = Field(default=None, description='日志信息')
    exception_info: Optional[str] = Field(default=None, description='异常信息')
    status: Optional[str] = Field(default=False, description='任务状态:正常,失败')
    create_time: Optional[DateTimeStr] = Field(default=None, description='创建时间')


class JobLogUpdateSchema(JobLogCreateSchema):
    """定时任务调度日志表更新模型"""
    ...
    id: Optional[int] = Field(default=None, description='任务日志ID')


class JobLogOutSchema(JobLogUpdateSchema, BaseSchema, TenantSchema):
    """定时任务调度日志表响应模型"""
    model_config = ConfigDict(from_attributes=True)
    ...


class JobQueryParam:
    """定时任务查询参数"""

    def __init__(
        self,
        name: Optional[str] = Query(None, description="任务名称"),
        status: Optional[str] = Query(None, description="状态: 启动,停止"),
        creator: Optional[int] = Query(None, description="创建人"),
        created_time: Optional[list[DateTimeStr]] = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        
        # 模糊查询字段
        self.name = ("like", f"%{name}%") if name else None
        
        # 精确查询字段
        self.created_id = creator
        self.status = status
        
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))


class JobLogQueryParam:
    """定时任务查询参数"""

    def __init__(
            self,
            job_id: Optional[int] = Query(None, description="定时任务ID"),
            job_name: Optional[str] = Query(None, description="任务名称"),
            status: Optional[str] = Query(None, description="状态: 正常,失败"),
            created_time: Optional[list[DateTimeStr]] = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 定时任务ID查询
        self.job_id = job_id
        # 模糊查询字段
        self.job_name = ("like", job_name)
        # 精确查询字段
        self.status = status
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
