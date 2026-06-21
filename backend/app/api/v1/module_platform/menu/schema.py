from dataclasses import dataclass, field
from typing import Literal

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam
from app.core.base_schema import BaseSchema
from app.core.validator import menu_request_validator


class MenuCreateSchema(BaseModel):
    """菜单创建模型"""

    name: str = Field(..., min_length=1, max_length=50, description="菜单名称")
    type: int = Field(..., ge=1, le=4, description="菜单类型(1:目录 2:菜单 3:按钮 4:外链)")
    order: int = Field(..., ge=0, description="显示顺序")
    permission: str | None = Field(default=None, max_length=100, description="权限标识")
    icon: str | None = Field(default=None, max_length=50, description="菜单图标")
    route_name: str | None = Field(default=None, max_length=100, description="路由名称")
    route_path: str | None = Field(default=None, max_length=200, description="路由地址")
    component_path: str | None = Field(default=None, max_length=200, description="组件路径")
    redirect: str | None = Field(default=None, max_length=200, description="重定向地址")
    hidden: bool = Field(default=False, description="是否隐藏")
    keep_alive: bool = Field(default=True, description="是否缓存")
    always_show: bool = Field(default=False, description="是否始终显示")
    title: str | None = Field(default=None, max_length=50, description="菜单标题")
    params: list[dict[str, str]] | None = Field(
        default=None,
        description="路由参数，格式为[{key: string, value: string}]",
    )
    affix: bool = Field(default=False, description="是否固定标签页")
    parent_id: int | None = Field(default=None, ge=1, description="父菜单ID")
    status: int = Field(default=0, ge=0, le=1, description="状态(0:启动 1:停用)")
    description: str | None = Field(default=None, max_length=255, description="描述")
    client: Literal["pc", "app"] = Field(
        default="pc",
        description="终端(pc:管理端桌面 app:移动端)",
    )
    link: str | None = Field(default=None, max_length=500, description="外链地址(仅type=4)")
    is_iframe: bool = Field(default=False, description="是否嵌入iframe")
    is_hide_tab: bool = Field(default=False, description="是否隐藏标签页")
    active_path: str | None = Field(default=None, max_length=200, description="激活菜单路径")
    show_badge: bool = Field(default=False, description="是否显示红点角标")
    show_text_badge: str | None = Field(default=None, max_length=20, description="文字角标内容")
    scope: Literal["platform", "tenant"] = Field(
        default="tenant",
        description="菜单可见范围(platform:仅平台 tenant:租户可用)",
    )

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int) -> int:
        if v not in {0, 1}:
            raise ValueError("状态仅支持 0(正常) 或 1(禁用)")
        return v

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, values):
        if isinstance(values, dict):
            for k in [
                "name",
                "icon",
                "permission",
                "route_name",
                "route_path",
                "component_path",
                "redirect",
                "title",
                "description",
                "link",
                "active_path",
                "show_text_badge",
            ]:
                if k in values and isinstance(values[k], str):
                    stripped = values[k].strip()
                    values[k] = stripped or None
            if "client" in values and isinstance(values["client"], str):
                cv = values["client"].strip()
                values["client"] = cv if cv in ("pc", "app") else "pc"
            if "parent_id" in values and isinstance(values["parent_id"], str):
                try:
                    values["parent_id"] = int(values["parent_id"].strip())
                except (ValueError, TypeError):
                    pass
            if "component_path" in values and isinstance(values["component_path"], str):
                cp = values["component_path"]
                if cp and cp.startswith("/"):
                    raise ValueError("组件路径不能以 / 开头")
        return values

    @model_validator(mode="after")
    def validate_fields(self):
        """
        统一校验菜单请求字段（委托到 `menu_request_validator`）。

        返回:
        - MenuCreateSchema: 校验后的同一实例。

        异常:
        - CustomException: 字段不满足菜单类型约束时抛出。
        """
        return menu_request_validator(self)


class MenuUpdateSchema(BaseModel):
    """菜单更新模型 — 所有字段可选"""

    name: str | None = Field(default=None, min_length=1, max_length=50, description="菜单名称")
    type: int | None = Field(default=None, ge=1, le=4, description="菜单类型(1:目录 2:菜单 3:按钮 4:外链)")
    order: int | None = Field(default=None, ge=0, description="显示顺序")
    permission: str | None = Field(default=None, max_length=100, description="权限标识")
    icon: str | None = Field(default=None, max_length=50, description="菜单图标")
    route_name: str | None = Field(default=None, max_length=100, description="路由名称")
    route_path: str | None = Field(default=None, max_length=200, description="路由地址")
    component_path: str | None = Field(default=None, max_length=200, description="组件路径")
    redirect: str | None = Field(default=None, max_length=200, description="重定向地址")
    hidden: bool | None = Field(default=None, description="是否隐藏")
    keep_alive: bool | None = Field(default=None, description="是否缓存")
    always_show: bool | None = Field(default=None, description="是否始终显示")
    title: str | None = Field(default=None, max_length=50, description="菜单标题")
    params: list[dict[str, str]] | None = Field(default=None, description="路由参数")
    affix: bool | None = Field(default=None, description="是否固定标签页")
    parent_id: int | None = Field(default=None, ge=1, description="父菜单ID")
    status: int | None = Field(default=None, ge=0, le=1, description="状态(0:启动 1:停用)")
    description: str | None = Field(default=None, max_length=255, description="描述")
    client: Literal["pc", "app"] | None = Field(default=None, description="终端(pc:管理端桌面 app:移动端)")
    link: str | None = Field(default=None, max_length=500, description="外链地址(仅type=4)")
    is_iframe: bool | None = Field(default=None, description="是否嵌入iframe")
    is_hide_tab: bool | None = Field(default=None, description="是否隐藏标签页")
    active_path: str | None = Field(default=None, max_length=200, description="激活菜单路径")
    show_badge: bool | None = Field(default=None, description="是否显示红点角标")
    show_text_badge: str | None = Field(default=None, max_length=20, description="文字角标内容")
    scope: Literal["platform", "tenant"] | None = Field(
        default=None,
        description="菜单可见范围(platform:仅平台 tenant:租户可用)",
    )
    parent_name: str | None = Field(default=None, max_length=50, description="父菜单名称")

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int | None) -> int | None:
        if v is None:
            return v
        if v not in {0, 1}:
            raise ValueError("状态仅支持 0(正常) 或 1(禁用)")
        return v

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, values):
        if isinstance(values, dict):
            for k in [
                "name",
                "icon",
                "permission",
                "route_name",
                "route_path",
                "component_path",
                "redirect",
                "title",
                "description",
                "link",
                "active_path",
                "show_text_badge",
            ]:
                if k in values and isinstance(values[k], str):
                    stripped = values[k].strip()
                    values[k] = stripped or None
            if "client" in values and isinstance(values["client"], str):
                cv = values["client"].strip()
                values["client"] = cv if cv in ("pc", "app") else None
            if "parent_id" in values and isinstance(values["parent_id"], str):
                try:
                    values["parent_id"] = int(values["parent_id"].strip())
                except (ValueError, TypeError):
                    pass
            if "component_path" in values and isinstance(values["component_path"], str) and values["component_path"]:
                if values["component_path"].startswith("/"):
                    raise ValueError("组件路径不能以 / 开头")
        return values

    @model_validator(mode="after")
    def validate_fields(self):
        if self.type is None:
            return self
        return menu_request_validator(self)


class MenuOutSchema(MenuCreateSchema, BaseSchema):
    """菜单详情响应模型（不含 children，用于详情和更新）"""

    model_config = ConfigDict(from_attributes=True)

    parent_name: str | None = Field(default=None, max_length=50, description="父菜单名称")


class MenuTreeOutSchema(MenuOutSchema):
    """菜单树形响应模型（含 children，用于树形列表）"""

    children: list["MenuTreeOutSchema"] | None = Field(default=None, description="子菜单列表")


@dataclass
class MenuQueryParam(BaseQueryParam):
    """菜单管理查询参数（菜单为平台级资源，无用户归属）"""

    name: str | None = Query(None, description="菜单名称")
    route_path: str | None = Query(None, description="路由地址")
    component_path: str | None = Query(None, description="组件路径")
    type: Literal[1, 2, 3, 4] | None = Query(None, description="菜单类型(1:目录 2:菜单 3:按钮 4:外链)")
    permission: str | None = Query(None, description="权限标识")
    description: str | None = Query(None, description="描述")
    status: str | None = Query(None, description="是否启用")
    menu_client: Literal["pc", "app"] | None = Query(
        None,
        description="管理端 Tab：pc=桌面端菜单 app=移动端菜单；不传则不过滤终端",
    )
    scope: Literal["tenant"] | None = Query(
        None,
        description="菜单范围过滤：tenant=仅租户可用菜单",
    )
    client: str | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        if self.name:
            self.name = (QueueEnum.like.value, self.name)
        if self.route_path:
            self.route_path = (QueueEnum.like.value, self.route_path)
        if self.component_path:
            self.component_path = (QueueEnum.like.value, self.component_path)
        if self.permission:
            self.permission = (QueueEnum.like.value, self.permission)
        if self.description:
            self.description = (QueueEnum.like.value, self.description)
        if self.status:
            self.status = (QueueEnum.eq.value, self.status)
        if self.menu_client in ("pc", "app"):
            self.client = (QueueEnum.eq.value, self.menu_client)
        del self.menu_client
        if self.scope == "tenant":
            self.scope = (QueueEnum.eq.value, "tenant")
