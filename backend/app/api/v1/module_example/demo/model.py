# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin, UserMixin, TenantMixin, CustomerMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel
    from app.api.v1.module_system.tenant.model import TenantModel
    from app.api.v1.module_system.customer.model import CustomerModel


class DemoModel(ModelMixin, UserMixin, TenantMixin, CustomerMixin):
    """
    示例表
    
    数据隔离策略:
    - 租户级示例: tenant_id必填, customer_id=NULL
    - 客户级示例: tenant_id必填, customer_id>0
    
    根据业务需求,此示例表支持客户级数据隔离
    """
    __tablename__: str = 'gen_demo'
    __table_args__: dict[str, str] = ({'comment': '示例表'})
    __loader_options__: list[str] = ["created_by", "updated_by", "tenant", "customer"]

    name: Mapped[str | None] = mapped_column(String(64), nullable=True, default='', comment='名称')
    
    # 关联关系 (覆盖Mixin中的property)
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="DemoModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="DemoModel.updated_id",
        lazy="selectin"
    )
    tenant: Mapped["TenantModel"] = relationship(
        foreign_keys="DemoModel.tenant_id",
        lazy="selectin"
    )
    customer: Mapped["CustomerModel | None"] = relationship(
        foreign_keys="DemoModel.customer_id",
        lazy="selectin"
    )