# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class GenDemo01CreateSchema(BaseModel):
    """
    示例新增模型
    """
    name: str = Field(default=..., description='名称')
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class GenDemo01UpdateSchema(GenDemo01CreateSchema):
    """
    示例更新模型
    """
    ...


class GenDemo01OutSchema(GenDemo01CreateSchema, BaseSchema, UserBySchema):
    """
    示例响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class GenDemo01QueryParam:
    """示例查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="名称"),
        status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        
    ) -> None:
        
        # 模糊查询字段
        self.name = ("like", name)
        # 模糊查询字段
        self.status = ("like", status)
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
