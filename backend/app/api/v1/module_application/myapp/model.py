# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin, UserMixin, TenantMixin, CustomerMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel
    from app.api.v1.module_system.tenant.model import TenantModel
    from app.api.v1.module_system.customer.model import CustomerModel


class ApplicationModel(ModelMixin, UserMixin, TenantMixin, CustomerMixin):
    """
    应用系统表 - 用于管理分系统和外部应用
    
    数据隔离策略:
    ===========
    - 系统级应用: tenant_id=1, customer_id=NULL (平台级应用,所有租户可见)
    - 租户级应用: tenant_id>1, customer_id=NULL (租户自己的应用,仅本租户可见)
    - 客户级应用: tenant_id>1, customer_id>0 (客户专属应用,仅该客户可见)
    
    根据业务需求,此表支持三级隔离
    """
    __tablename__: str = 'app_myapp'
    __table_args__: dict[str, str] = ({'comment': '应用系统表'})
    __loader_options__: list[str] = ["created_by", "updated_by", "tenant", "customer"]

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment='应用名称')
    access_url: Mapped[str] = mapped_column(String(500), nullable=False, comment='访问地址')
    icon_url: Mapped[str | None] = mapped_column(String(300), nullable=True, comment='应用图标URL')
    
    # 关联关系 (覆盖Mixin中的property)
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="ApplicationModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="ApplicationModel.updated_id",
        lazy="selectin"
    )
    tenant: Mapped["TenantModel"] = relationship(
        foreign_keys="ApplicationModel.tenant_id",
        lazy="selectin"
    )
    customer: Mapped["CustomerModel | None"] = relationship(
        foreign_keys="ApplicationModel.customer_id",
        lazy="selectin"
    )