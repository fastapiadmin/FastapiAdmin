"""
人员管理 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class PersonnelCreateSchema(BaseModel):
    """新增招生人员模型"""

    personnel_name: str = Field(..., description="人员姓名", min_length=2, max_length=100)
    personnel_code: str | None = Field(default=None, description="人员编号", max_length=50)
    personnel_type: str = Field(default="manual", description="人员类型")

    user_id: int | None = Field(default=None, description="关联用户ID")
    phone: str | None = Field(default=None, description="手机号", max_length=20)
    email: str | None = Field(default=None, description="邮箱", max_length=100)

    team_id: int | None = Field(default=None, description="招生组ID")
    team_name: str | None = Field(default=None, description="招生组名称", max_length=200)

    province: str | None = Field(default=None, description="负责省份", max_length=50)
    city: str | None = Field(default=None, description="负责城市", max_length=50)

    position: str | None = Field(default=None, description="职务", max_length=100)

    join_date: DateStr | None = Field(default=None, description="加入日期")
    leave_reason: str | None = Field(default=None, description="离开原因", max_length=500)

    target_schools: int | None = Field(default=None, description="目标学校数量")
    visited_schools: int | None = Field(default=None, description="已访问学校数量")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")

    @field_validator("personnel_name")
    @classmethod
    def validate_personnel_name(cls, v: str) -> str:
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
    leave_date: DateStr | None = Field(default=None, description="离开日期")
    invite_code: str | None = Field(default=None, description="邀请码")
    invite_time: DateTimeStr | None = Field(default=None, description="邀请时间")
    invite_expire_time: DateTimeStr | None = Field(default=None, description="邀请过期时间")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class PersonnelQuerySchema(BaseModel):
    """招生人员查询参数模型"""

    def __init__(
        self,
        personnel_name: str | None = Query(None, description="人员姓名"),
        personnel_code: str | None = Query(None, description="人员编号"),
        personnel_type: str | None = Query(None, description="人员类型"),
        team_id: int | None = Query(None, description="招生组ID"),
        team_name: str | None = Query(None, description="招生组名称"),
        province: str | None = Query(None, description="省份"),
        city: str | None = Query(None, description="城市"),
        status: str | None = Query(None, description="状态"),
        position: str | None = Query(None, description="职务"),
    ) -> None:
        from app.common.enums import QueueEnum

        if personnel_name:
            self.personnel_name = (QueueEnum.like.value, personnel_name)
        if personnel_code:
            self.personnel_code = (QueueEnum.eq.value, personnel_code)
        if personnel_type:
            self.personnel_type = (QueueEnum.eq.value, personnel_type)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if team_name:
            self.team_name = (QueueEnum.like.value, team_name)
        if province:
            self.province = (QueueEnum.eq.value, province)
        if city:
            self.city = (QueueEnum.eq.value, city)
        if status:
            self.status = (QueueEnum.eq.value, status)
        if position:
            self.position = (QueueEnum.eq.value, position)