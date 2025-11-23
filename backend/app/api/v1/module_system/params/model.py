# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin, TenantMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.tenant.model import TenantModel
    from app.api.v1.module_system.user.model import UserModel


class ParamsModel(ModelMixin, UserMixin, TenantMixin):
    """
    参数配置表
    
    参数配置隔离策略:
    =============
    - 系统级参数(tenant_id=NULL):
      * 平台级配置参数,影响所有租户
      * config_type=True表示系统内置,不可删除
      * 如:系统名称、Logo、邮件配置等
      
    - 租户级参数(tenant_id>1):
      * 租户自定义配置参数,仅本租户生效
      * config_type=False表示可自定义
      * 如:租户LOGO、业务配置等
      
    - 不需要customer_id:
      * 参数是租户级配置,不属于客户
    
    用于存储系统配置参数，包括：
    - 系统级别参数
    - 租户级别参数
    - 配置项的名称、键、值和类型等信息
    """
    __tablename__: str = "system_param"
    __table_args__: dict[str, str] = ({'comment': '系统参数表'})

    # 覆盖TenantMixin的tenant_id为可选(支持系统级参数)
    tenant_id: Mapped[int | None] = mapped_column(  # type: ignore
        Integer,
        ForeignKey("system_tenant.id", ondelete="CASCADE"),
        default=None,
        nullable=True,
        index=True,
        comment="所属租户ID(NULL表示系统级参数,所有租户共享)"
    )

    config_name: Mapped[str] = mapped_column(String(500), nullable=False, comment='参数名称')
    config_key: Mapped[str] = mapped_column(String(500), nullable=False, comment='参数键名')
    config_value: Mapped[str | None] = mapped_column(String(500), comment='参数键值')
    config_type: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True, comment="系统内置(True:是 False:否)")
    
    # 关联关系 (继承自UserMixin和TenantMixin)
    tenant: Mapped["TenantModel | None"] = relationship(
        foreign_keys="ParamsModel.tenant_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="ParamsModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="ParamsModel.updated_id",
        lazy="selectin"
    )
    