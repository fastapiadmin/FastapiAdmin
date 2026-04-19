"""
表彰评优 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class EvaluationCreateSchema(BaseModel):
    """新增表彰评优模型"""

    evaluation_name: str | None = Field(default=None, description="表彰名称")
    evaluation_type: str | None = Field(default=None, description="表彰类型")
    evaluation_period: str | None = Field(default=None, description="评选周期")
    target_type: str | None = Field(default=None, description="目标类型")
    target_id: int | None = Field(default=None, description="目标ID")
    achievement_score: int | None = Field(default=None, description="成绩得分")
    ranking: int | None = Field(default=None, description="排名")
    award_level: str | None = Field(default=None, description="获奖级别")
    award_content: str | None = Field(default=None, description="获奖内容")
    evaluation_time: DateTimeStr | None = Field(default=None, description="评选时间")


class EvaluationUpdateSchema(EvaluationCreateSchema):
    """更新表彰评优模型"""
    pass


class EvaluationOutSchema(EvaluationCreateSchema, BaseSchema, UserBySchema):
    """表彰评优响应模型"""

    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(default=None, description="状态")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class EvaluationQuerySchema(BaseModel):
    """表彰评优查询参数模型"""

    def __init__(
        self,
        evaluation_name: str | None = Query(None, description="表彰名称"),
        evaluation_type: str | None = Query(None, description="表彰类型"),
        target_type: str | None = Query(None, description="目标类型"),
        target_id: int | None = Query(None, description="目标ID"),
    ) -> None:
        from app.common.enums import QueueEnum

        if evaluation_name:
            self.evaluation_name = (QueueEnum.like.value, evaluation_name)
        if evaluation_type:
            self.evaluation_type = (QueueEnum.eq.value, evaluation_type)
        if target_type:
            self.target_type = (QueueEnum.eq.value, target_type)
        if target_id is not None:
            self.target_id = (QueueEnum.eq.value, target_id)
