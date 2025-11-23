# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import JSON, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin, UserMixin, TenantMixin, CustomerMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel
    from app.api.v1.module_system.tenant.model import TenantModel
    from app.api.v1.module_system.customer.model import CustomerModel


class McpModel(ModelMixin, UserMixin, TenantMixin, CustomerMixin):
    """
    MCP 服务器表
    
    数据隔离策略:
    ===========
    - 系统级MCP: tenant_id=1, customer_id=NULL (平台预置MCP,所有租户可用)
    - 租户级MCP: tenant_id>1, customer_id=NULL (租户自定义MCP,仅本租户可用)
    - 客户级MCP: tenant_id>1, customer_id>0 (客户专属MCP,仅该客户可用)
    
    MCP类型:
    - 0: stdio (标准输入输出)
    - 1: sse (Server-Sent Events)
    """
    __tablename__: str = 'app_ai_mcp'
    __table_args__: dict[str, str] = ({'comment': 'MCP 服务器表'})
    __loader_options__: list[str] = ["created_by", "updated_by", "tenant", "customer"]

    name: Mapped[str] = mapped_column(String(50), comment='MCP 名称')
    type: Mapped[int] = mapped_column(Integer, default=0, comment='MCP 类型（0:stdio 1:sse）')
    url: Mapped[str | None] = mapped_column(String(255), default=None, comment='远程 SSE 地址')
    command: Mapped[str | None] = mapped_column(String(255), default=None, comment='MCP 命令')
    args: Mapped[str | None] = mapped_column(String(255), default=None, comment='MCP 命令参数')
    env: Mapped[dict[str, str] | None] = mapped_column(JSON(), default=None, comment='MCP 环境变量')
    
    # 关联关系 (覆盖Mixin中的property)
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="McpModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="McpModel.updated_id",
        lazy="selectin"
    )
    tenant: Mapped["TenantModel"] = relationship(
        foreign_keys="McpModel.tenant_id",
        lazy="selectin"
    )
    customer: Mapped["CustomerModel | None"] = relationship(
        foreign_keys="McpModel.customer_id",
        lazy="selectin"
    )