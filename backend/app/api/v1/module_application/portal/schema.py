from urllib.parse import urlparse

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema, TenantBySchema, UserBySchema
from app.core.validator import DateTimeStr


class ApplicationCreateSchema(BaseModel):
    """应用创建模型"""

    name: str = Field(..., max_length=64, description="应用名称")
    access_url: str = Field(..., max_length=255, description="访问地址")
    icon_url: str | None = Field(None, max_length=300, description="应用图标URL")
    status: str = Field("0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="描述")

    @field_validator("access_url")
    @classmethod
    def _validate_access_url(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("访问地址不能为空")
        parsed = urlparse(v)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("访问地址必须为 http/https URL")
        return v

    @field_validator("icon_url")
    @classmethod
    def _validate_icon_url(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        parsed = urlparse(v)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("应用图标URL必须为 http/https URL")
        return v


class ApplicationUpdateSchema(ApplicationCreateSchema):
    """应用更新模型"""


class ApplicationOutSchema(ApplicationCreateSchema, BaseSchema, UserBySchema, TenantBySchema):
    """应用响应模型"""

    model_config = ConfigDict(from_attributes=True)


class PluginInfoOut(BaseModel):
    """``app/plugin/module_*`` 插件目录与可选 ``plugin.toml`` 的汇总信息。"""

    module_dir: str = Field(..., description="目录名，如 module_example")
    route_prefix: str = Field(..., description="动态路由容器前缀，如 /example")
    has_manifest: bool = Field(..., description="是否存在 plugin.toml")
    name: str | None = Field(None, description="manifest 中的 name，应与目录段一致")
    title: str | None = None
    version: str | None = None
    description: str | None = None
    optional: bool | None = Field(None, description="语义：是否可关闭该子系统")
    tags: list[str] | None = None
    manifest_name_mismatch: bool | None = Field(
        None, description="manifest 的 name 与目录 module_<name> 不一致时为 True"
    )


class ApplicationQueryParam:
    """应用系统查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="应用名称"),
        status: str | None = Query(None, description="是否启用"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        updated_time: list[DateTimeStr] | None = Query(
            None,
            description="更新时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:
        # 模糊查询字段
        self.name = (QueueEnum.like.value, name)

        # 精确查询字段
        self.status = (QueueEnum.eq.value, status)
        self.created_id = (QueueEnum.eq.value, created_id)
        self.updated_id = (QueueEnum.eq.value, updated_id)

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = (QueueEnum.between.value, (updated_time[0], updated_time[1]))
