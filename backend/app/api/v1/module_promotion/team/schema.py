"""
组织架构管理 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema


class TeamCreateSchema(BaseModel):
    """新增招生组模型"""

    name: str = Field(..., description="招生组名称", min_length=2, max_length=100)
    parent_id: int | None = Field(default=None, description="上级招生组ID")
    level: int = Field(default=1, description="层级")
    leader_id: int | None = Field(default=None, description="负责人用户ID")
    leader_name: str | None = Field(default=None, description="负责人姓名", max_length=100)
    leader_phone: str | None = Field(default=None, description="负责人电话", max_length=20)
    province: str | None = Field(default=None, description="省份", max_length=50)
    city: str | None = Field(default=None, description="城市", max_length=50)
    responsible_area: str | None = Field(default=None, description="负责区域", max_length=200)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
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
        name: str | None = Query(None, description="招生组名称"),
        parent_id: int | None = Query(None, description="上级招生组ID"),
        level: int | None = Query(None, description="层级"),
        province: str | None = Query(None, description="省份"),
        status: str | None = Query(None, description="状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if name:
            self.name = (QueueEnum.like.value, name)
        if parent_id is not None:
            self.parent_id = (QueueEnum.eq.value, parent_id)
        if level is not None:
            self.level = (QueueEnum.eq.value, level)
        if province:
            self.province = (QueueEnum.eq.value, province)
        if status:
            self.status = (QueueEnum.eq.value, status)


class TeamTreeSchema(BaseModel):
    """招生组树形结构模型"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="招生组ID")
    name: str = Field(..., description="招生组名称")
    parent_id: int | None = Field(default=None, description="上级招生组ID")
    level: int = Field(..., description="层级")
    leader_id: int | None = Field(default=None, description="负责人用户ID")
    leader_name: str | None = Field(default=None, description="负责人姓名")
    leader_phone: str | None = Field(default=None, description="负责人电话")
    province: str | None = Field(default=None, description="省份")
    city: str | None = Field(default=None, description="城市")
    responsible_area: str | None = Field(default=None, description="负责区域")
    status: str | None = Field(default=None, description="状态")
    children: list["TeamTreeSchema"] = Field(default_factory=list, description="下级招生组")
