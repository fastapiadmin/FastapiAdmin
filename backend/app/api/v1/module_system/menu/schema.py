# -*- coding: utf-8 -*-

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.validator import menu_request_validator
from app.core.base_schema import BaseSchema


class MenuCreateSchema(BaseModel):
    """菜单创建模型"""
    name: str = Field(..., max_length=50, description="菜单名称")
    type: int = Field(..., ge=1, le=4, description="菜单类型(1:目录 2:菜单 3:按钮 4:外链)")
    order: int = Field(..., ge=1, description="显示顺序")
    permission: str | None = Field(default=None, max_length=100, description="权限标识")
    icon: str | None = Field(default=None, max_length=100, description="菜单图标")
    route_name: str | None = Field(default=None, max_length=100, description="路由名称")
    route_path: str | None = Field(default=None, max_length=200, description="路由地址")
    component_path: str | None = Field(default=None, max_length=255, description="组件路径")
    redirect: str | None = Field(default=None, max_length=200, description="重定向地址")
    hidden: bool = Field(default=False, description="是否隐藏(True:是 False:否)")
    keep_alive: bool = Field(default=True, description="是否缓存(True:是 False:否)")
    always_show: bool = Field(default=False, description="是否始终显示(True:是 False:否)")
    title: str | None = Field(default=None, max_length=50, description="菜单标题")
    params: list[dict[str, str]] | None = Field(default=None, description="路由参数，格式为[{key: string, value: string}]")
    affix: bool = Field(default=False, description="是否固定标签页(True:是 False:否)")
    parent_id: int | None = Field(default=None, ge=1, description="父菜单ID")
    status: str = Field(default="0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="描述")

    @model_validator(mode='before')
    @classmethod
    def _normalize(cls, values):
        if isinstance(values, dict):
            # 字符串去空格
            for k in ["name", "icon", "permission", "route_name", "route_path", "component_path", "redirect", "title", "description"]:
                if k in values and isinstance(values[k], str):
                    values[k] = values[k].strip() or None if values[k].strip() == "" else values[k].strip()
            # 父ID转整型
            if "parent_id" in values and isinstance(values["parent_id"], str):
                try:
                    values["parent_id"] = int(values["parent_id"].strip())
                except Exception:
                    pass
            # 路由名/路径规范
            import re
            if "route_name" in values and isinstance(values["route_name"], str):
                rn = values["route_name"]
                if rn and not re.match(r"^[A-Za-z][A-Za-z0-9_.-]{1,99}$", rn):
                    raise ValueError("路由名称需字母开头，仅含字母/数字/_ . -")
            if "route_path" in values and isinstance(values["route_path"], str):
                rp = values["route_path"]
                if rp and not rp.startswith("/"):
                    raise ValueError("路由路径需以 / 开头")
        return values

    @model_validator(mode='after')
    def validate_fields(self):
        return menu_request_validator(self)


class MenuUpdateSchema(MenuCreateSchema):
    """菜单更新模型"""
    parent_name: str | None = Field(default=None, max_length=50, description="父菜单名称")


class MenuOutSchema(MenuCreateSchema, BaseSchema):
    """菜单响应模型"""
    model_config = ConfigDict(from_attributes=True)

    parent_name: str | None = Field(default=None, max_length=50, description="父菜单名称")


class MenuQueryParam:
    """菜单管理查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="菜单名称"),
        route_path: str | None = Query(None, description="路由地址"),
        component_path: str | None = Query(None, description="组件路径"),
        type: Literal[1,2,3,4] | None = Query(None, description="菜单类型(1:目录 2:菜单 3:按钮 4:外链)"),
        permission: str | None = Query(None, description="权限标识"),
        status: str | None = Query(None, description="菜单状态(0:启用 1:禁用)"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", example=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        
        # 模糊查询字段
        self.name = ("like", name)
        self.route_path = ("like", route_path)
        self.component_path = ("like", component_path)
        self.permission = ("like", permission)

        # 精确查询字段
        self.type = type
        self.status = status

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
