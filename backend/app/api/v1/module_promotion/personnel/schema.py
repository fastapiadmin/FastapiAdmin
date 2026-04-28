"""
人员管理 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class PersonnelCreateSchema(BaseModel):
    """新增招生人员模型"""

    name: str = Field(..., description="人员姓名", min_length=2, max_length=100)
    user_id: int | None = Field(default=None, description="关联用户ID")
    phone: str | None = Field(default=None, description="手机号", max_length=20)
    email: str | None = Field(default=None, description="邮箱", max_length=100)
    team_id: int | None = Field(default=None, description="招生组ID")
    role: str | None = Field(default=None, description="角色", max_length=50)
    invitation_status: str | None = Field(default=None, description="邀请状态")
    join_time: DateTimeStr | None = Field(default=None, description="加入时间")
    exit_time: DateTimeStr | None = Field(default=None, description="离开时间")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """验证人员姓名"""
        v = v.strip()
        if not v:
            raise ValueError("人员姓名不能为空")
        return v


class PersonnelUpdateSchema(PersonnelCreateSchema):
    """更新招生人员模型"""

    pass


class PersonnelOutSchema(PersonnelCreateSchema, BaseSchema, UserBySchema):
    """招生人员响应模型"""

    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(default=None, description="状态")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class PersonnelQuerySchema(BaseModel):
    """招生人员查询参数模型"""

    def __init__(
        self,
        name: str | None = Query(None, description="人员姓名"),
        user_id: int | None = Query(None, description="用户ID"),
        team_id: int | None = Query(None, description="招生组ID"),
        role: str | None = Query(None, description="角色"),
        status: str | None = Query(None, description="状态"),
        invitation_status: str | None = Query(None, description="邀请状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if name:
            self.name = (QueueEnum.like.value, name)
        if user_id is not None:
            self.user_id = (QueueEnum.eq.value, user_id)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if role:
            self.role = (QueueEnum.eq.value, role)
        if status:
            self.status = (QueueEnum.eq.value, status)
        if invitation_status:
            self.invitation_status = (QueueEnum.eq.value, invitation_status)
