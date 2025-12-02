# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema


class NoticeCreateSchema(BaseModel):
    """公告通知创建模型"""
    notice_title: str = Field(..., max_length=50, description='公告标题')
    notice_type: str = Field(..., description='公告类型（1通知 2公告）')
    notice_content: str = Field(..., description='公告内容')
    status: str = Field(default="0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="描述")

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
        return self


class NoticeUpdateSchema(NoticeCreateSchema):
    """公告通知更新模型"""
    ...


class NoticeOutSchema(NoticeCreateSchema, BaseSchema, UserBySchema):
    """公告通知响应模型"""
    model_config = ConfigDict(from_attributes=True)


class NoticeQueryParam:
    """公告通知查询参数"""

    def __init__(
        self,
        notice_title: str | None = Query(None, description="公告标题"),
        notice_type: str | None = Query(None, description="公告类型"),
        status: str | None = Query(None, description="是否可用"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:
        
        # 模糊查询字段
        self.notice_title = ("like", notice_title)

        # 精确查询字段
        self.created_id = created_id
        self.updated_id = updated_id
        self.status = status
        self.notice_type = notice_type

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
        
