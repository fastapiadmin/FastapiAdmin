# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema, TenantSchema, CustomerSchema


class NoticeCreateSchema(BaseModel):
    """公告通知创建模型"""
    notice_title: str = Field(..., max_length=50, description='公告标题')
    notice_type: str = Field(..., description='公告类型（1通知 2公告）')
    notice_content: str = Field(..., description='公告内容')
    status: str = Field(default=True, description="是否启用(True:启用 False:禁用)")
    description: Optional[str] = Field(default=None, max_length=255, description="描述")

    @field_validator("notice_type")
    @classmethod
    def _validate_notice_type(cls, value: str):
        if value not in {"1", "2"}:
            raise ValueError("公告类型仅支持 '1'(通知) 或 '2'(公告)")
        return value

    @model_validator(mode='after')
    def _validate_after(self):
        if not self.notice_title.strip():
            raise ValueError("公告标题不能为空")
        if not self.notice_content.strip():
            raise ValueError("公告内容不能为空")
        # 验证时间范围
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValueError("开始时间必须早于结束时间")
        return self


class NoticeUpdateSchema(NoticeCreateSchema):
    """公告通知更新模型"""
    ...


class NoticeOutSchema(NoticeCreateSchema, BaseSchema, UserBySchema, TenantSchema, CustomerSchema):
    """公告通知响应模型"""
    model_config = ConfigDict(from_attributes=True)


class NoticeQueryParam:
    """公告通知查询参数"""

    def __init__(
        self,
        notice_title: Optional[str] = Query(None, description="公告标题"),
        notice_type: Optional[str] = Query(None, description="公告类型"),
        status: Optional[str] = Query(None, description="是否可用"),
        created_id: Optional[int] = Query(None, description="创建人"),
        created_time: Optional[list[DateTimeStr]] = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        
        # 模糊查询字段
        self.notice_title = ("like", notice_title)

        # 精确查询字段
        self.created_id = created_id
        self.status = status
        self.notice_type = notice_type

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
