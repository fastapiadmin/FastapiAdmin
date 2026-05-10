"""
组织架构管理 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.base_schema import BaseSchema, UserBySchema


class TeamCreateSchema(BaseModel):
    """新增招生组模型"""

    name: str | None = Field(default=None, description="招生组名称", min_length=2, max_length=100)
    parent_id: int | None = Field(default=None, description="上级招生组ID")
    level: int = Field(default=1, description="层级")
    leader_id: int | None = Field(default=None, description="负责人用户ID")
    leader_name: str | None = Field(default=None, description="负责人姓名", max_length=100)
    leader_phone: str | None = Field(default=None, description="负责人电话", max_length=20)
    province: str | None = Field(default=None, description="省份", max_length=50)
    city: str | None = Field(default=None, description="城市", max_length=50)
    responsible_area: str | None = Field(default=None, description="负责区域", max_length=200)
    description: str | None = Field(default=None, description="描述")
    team_name: str | None = Field(default=None, description="团队名称(兼容字段)")
    team_code: str | None = Field(default=None, description="团队编码")
    team_level: str | None = Field(default=None, description="团队级别")
    display_order: int | None = Field(default=None, description="显示顺序")
    remark: str | None = Field(default=None, description="备注")

    @field_validator("name", "team_name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        """验证招生组名称"""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("招生组名称不能为空")
        return v

    @model_validator(mode="after")
    def validate_name_required(self) -> "TeamCreateSchema":
        """确保name字段有值"""
        if self.name is None and self.team_name:
            self.name = self.team_name
        if self.name is None:
            raise ValueError("招生组名称不能为空")
        return self


class TeamUpdateSchema(TeamCreateSchema):
    """更新招生组模型"""

    pass


class TeamOutSchema(TeamCreateSchema, BaseSchema, UserBySchema):
    """招生组响应模型"""

    model_config = ConfigDict(from_attributes=True)

    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class TeamQuerySchema(BaseModel):
    """招生组查询模型"""

    name: str | None = Query(None, description="招生组名称")
    team_name: str | None = Query(None, description="团队名称")
    team_code: str | None = Query(None, description="团队编码")
    team_level: str | None = Query(None, description="团队级别")
    team_status: str | None = Query(None, description="团队状态")

    def to_search(self) -> dict:
        """转换为搜索参数字典"""
        search = {}
        if self.name:
            search["name"] = self.name
        if self.team_name:
            search["name"] = self.team_name
        if self.team_code:
            search["team_code"] = self.team_code
        if self.team_level:
            search["team_level"] = self.team_level
        if self.team_status:
            search["team_status"] = self.team_status
        return search


class TeamTreeSchema(BaseModel):
    """招生组树形结构模型"""

    id: int
    name: str = Field(..., description="招生组名称")
    parent_id: int | None = Field(default=None, description="上级招生组ID")
    level: int = Field(default=1, description="层级")
    leader_name: str | None = Field(default=None, description="负责人姓名")
    team_level: str | None = Field(default=None, description="团队级别")
    team_status: str | None = Field(default=None, description="团队状态")
    children: list["TeamTreeSchema"] = Field(default_factory=list, description="子节点")
