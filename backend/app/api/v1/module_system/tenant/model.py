# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from app.core.base_model import ModelMixin, UserMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel
    from app.api.v1.module_system.dept.model import DeptModel
    from app.api.v1.module_system.customer.model import CustomerModel
    from app.api.v1.module_system.role.model import RoleModel
    from app.api.v1.module_system.position.model import PositionModel
    from app.api.v1.module_system.menu.model import MenuModel

class TenantModel(ModelMixin, UserMixin):
    """
    租户模型
    
    核心数据隔离模型：
    - 系统租户(id=1)：管理所有租户和系统配置,由平台超管管理
    - 普通租户(id>1)：拥有自己的用户、部门、角色、客户等数据,租户间完全隔离
    - 所有业务表通过tenant_id字段关联到租户，实现租户间数据隔离
    
    注意：
    - 租户表本身不需要tenant_id字段(租户不属于租户)
    - 租户表不需要customer_id字段(租户不属于客户)
    - 但需要created_id/updated_id用于审计追踪
    """
    __tablename__: str = 'system_tenant'
    __table_args__: dict[str, str] = {'comment': '租户表'}

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment='租户名称')
    code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment='租户编码')
    domain: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=True, comment='租户域名')
    logo: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='租户Logo')
    expire_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment='过期时间')
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None, comment='开始时间')
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None, comment='结束时间')
    
    # 关联关系 (继承自UserMixin的created_id和updated_id)
    users: Mapped[list["UserModel"]] = relationship(
        back_populates="tenant", 
        foreign_keys="UserModel.tenant_id",
        lazy="selectin"
    )
    depts: Mapped[list["DeptModel"]] = relationship(
        back_populates="tenant",
        foreign_keys="DeptModel.tenant_id", 
        lazy="selectin"
    )
    customers: Mapped[list["CustomerModel"]] = relationship(
        back_populates="tenant",
        foreign_keys="CustomerModel.tenant_id",
        lazy="selectin"
    )
    roles: Mapped[list["RoleModel"]] = relationship(
        back_populates="tenant",
        foreign_keys="RoleModel.tenant_id",
        lazy="selectin"
    )
    positions: Mapped[list["PositionModel"]] = relationship(
        back_populates="tenant",
        foreign_keys="PositionModel.tenant_id",
        lazy="selectin"
    )
    menus: Mapped[list["MenuModel"]] = relationship(
        back_populates="tenant",
        foreign_keys="MenuModel.tenant_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="TenantModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="TenantModel.updated_id",
        lazy="selectin"
    )
    
    @validates('name')
    def validate_name(self, key: str, name: str) -> str:
        """验证名称不为空"""
        if not name or not name.strip():
            raise ValueError('名称不能为空')
        return name
    
    @validates('code')
    def validate_code(self, key: str, code: str) -> str:
        """验证编码格式校验"""
        if not code or not code.strip():
            raise ValueError('编码不能为空')
        if not code.isalnum():
            raise ValueError('编码只能包含字母和数字')
        return code
