"""
组织架构管理 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class TeamCreateSchema(BaseModel):
    """新增招生组模型"""

    team_name: str = Field(..., description="招生组名称", min_length=2, max_length=200)
    team_code: str | None = Field(default=None, description="招生组编码", max_length=50)
    team_level: str = Field(default="city", description="招生组级别")

    parent_id: int | None = Field(default=None, description="上级招生组ID")
    level_path: str | None = Field(default=None, description="层级路径")
    level_depth: int = Field(default=1, description="层级深度")

    region_name: str | None = Field(default=None, description="区域名称", max_length=100)
    province: str | None = Field(default=None, description="省份", max_length=50)
    city: str | None = Field(default=None, description="城市", max_length=50)
    district: str | None = Field(default=None, description="区县", max_length=50)

    responsibility: str | None = Field(default=None, description="职责描述")
    target_schools: int | None = Field(default=None, description="目标学校数量")
    target_students: int | None = Field(default=None, description="目标学生数量")

    leader_id: int | None = Field(default=None, description="负责人用户ID")
    leader_name: str | None = Field(default=None, description="负责人姓名", max_length=100)
    leader_phone: str | None = Field(default=None, description="负责人电话", max_length=20)

    member_count: int = Field(default=0, description="成员数量")
    display_order: int = Field(default=0, description="显示排序")

    @field_validator("team_name")
    @classmethod
    def validate_team_name(cls, v: str) -> str:
        """验证招生组名称"""
        v = v.strip()
        if not v:
            raise ValueError("招生组名称不能为空")
        return v


class TeamUpdateSchema(TeamCreateSchema):
    """更新招生组模型"""
    pass


class TeamOutSchema(TeamCreateSchema, BaseSchema, UserBySchema):
    """招生组响应模型"""

    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(default=None, description="状态")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class TeamQuerySchema(BaseModel):
    """招生组查询参数模型"""

    def __init__(
        self,
        team_name: str | None = Query(None, description="招生组名称"),
        team_code: str | None = Query(None, description="招生组编码"),
        team_level: str | None = Query(None, description="招生组级别"),
        parent_id: int | None = Query(None, description="上级招生组ID"),
        province: str | None = Query(None, description="省份"),
        city: str | None = Query(None, description="城市"),
        status: str | None = Query(None, description="状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if team_name:
            self.team_name = (QueueEnum.like.value, team_name)
        if team_code:
            self.team_code = (QueueEnum.eq.value, team_code)
        if team_level:
            self.team_level = (QueueEnum.eq.value, team_level)
        if parent_id is not None:
            self.parent_id = (QueueEnum.eq.value, parent_id)
        if province:
            self.province = (QueueEnum.eq.value, province)
        if city:
            self.city = (QueueEnum.eq.value, city)
        if status:
            self.status = (QueueEnum.eq.value, status)


class TeamTreeSchema(BaseModel):
    """招生组树形结构模型"""

    id: int = Field(..., description="招生组ID")
    team_name: str = Field(..., description="招生组名称")
    team_code: str | None = Field(default=None, description="招生组编码")
    team_level: str = Field(..., description="招生组级别")
    parent_id: int | None = Field(default=None, description="上级招生组ID")
    level_depth: int = Field(default=1, description="层级深度")
    region_name: str | None = Field(default=None, description="区域名称")
    province: str | None = Field(default=None, description="省份")
    city: str | None = Field(default=None, description="城市")
    status: str = Field(..., description="状态")
    member_count: int = Field(default=0, description="成员数量")
    children: list["TeamTreeSchema"] = Field(default_factory=list, description="子节点")