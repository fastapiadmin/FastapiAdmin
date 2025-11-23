# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Boolean, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import MappedBase, ModelMixin, UserMixin, TenantMixin, CustomerMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.dept.model import DeptModel
    from app.api.v1.module_system.position.model import PositionModel
    from app.api.v1.module_system.role.model import RoleModel
    from app.api.v1.module_system.tenant.model import TenantModel
    from app.api.v1.module_system.customer.model import CustomerModel


class UserRolesModel(MappedBase):
    """
    用户角色关联表
    
    定义用户与角色的多对多关系
    """
    __tablename__: str = "system_user_roles"
    __table_args__: dict[str, str] = ({'comment': '用户角色关联表'})

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("system_user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="用户ID"
    )
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("system_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="角色ID"
    )


class UserPositionsModel(MappedBase):
    """
    用户岗位关联表
    
    定义用户与岗位的多对多关系
    """
    __tablename__: str = "system_user_positions"
    __table_args__: dict[str, str] = ({'comment': '用户岗位关联表'})

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("system_user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="用户ID"
    )
    position_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("system_position.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="岗位ID"
    )


class UserModel(ModelMixin, UserMixin, TenantMixin, CustomerMixin):
    """
    用户模型
    
    用户类型与数据隔离关系：
    ====================
    - 系统用户(user_type=0): 
      * tenant_id=1(系统租户)
      * customer_id=None
      * 用于平台管理,可管理所有租户
    
    - 租户管理员(user_type=1): 
      * tenant_id>1
      * customer_id=None
      * 可管理本租户内所有数据(包括所有客户)
    
    - 租户普通用户(user_type=1):
      * tenant_id>1
      * customer_id=None
      * 数据权限由role.data_scope控制
    
    - 客户用户(user_type=2):
      * tenant_id>1
      * customer_id>1
      * 只能访问其所属客户的数据
    
    数据权限实现机制：
    ==================
    通过角色的data_scope字段和用户-部门-角色关系实现:
    - 1(仅本人): WHERE created_id = current_user.id
    - 2(本部门): WHERE user.dept_id = current_user.dept_id
    - 3(本部门及以下): WHERE dept.tree_path LIKE 'current_user.dept.tree_path%'
    - 4(全部数据): WHERE tenant_id = current_user.tenant_id (AND customer_id IS NULL OR customer_id = current_user.customer_id)
    - 5(自定义): WHERE dept_id IN (SELECT dept_id FROM role_depts WHERE role_id IN current_user.role_ids)
    
    客户用户额外限制:
    - 无论data_scope如何,都必须加上: AND customer_id = current_user.customer_id
    """
    __tablename__: str = "system_user"
    __table_args__: dict[str, str] = ({'comment': '用户表'})
    __loader_options__: list[str] = ["dept", "roles", "positions", "created_by", "updated_by", "tenant", "customer"]

    username: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, comment="用户名/登录账号")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码哈希")
    name: Mapped[str] = mapped_column(String(32), nullable=False, comment="昵称")
    mobile: Mapped[str | None] = mapped_column(String(11), nullable=True, unique=True, comment="手机号")
    email: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True, comment="邮箱")
    gender: Mapped[str | None] = mapped_column(String(1), default='2', nullable=True, comment="性别(0:男 1:女 2:未知)")
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="头像URL地址")
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否超管")
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="最后登录时间")
    
    gitee_login: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="Gitee登录")
    github_login: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="Github登录")
    wx_login: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="微信登录")
    qq_login: Mapped[str | None] = mapped_column(String(32), nullable=True, comment="QQ登录")
    user_type: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="用户类型(0:系统用户 1:租户用户 2:客户用户)")
    salt: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="加密盐")
    
    # 部门关联
    dept_id: Mapped[int | None] = mapped_column(
        Integer, 
        ForeignKey('system_dept.id', ondelete="SET NULL", onupdate="CASCADE"), 
        nullable=True, 
        index=True, 
        comment="部门ID"
    )
    
    # 关联关系 (继承自UserMixin, TenantMixin, CustomerMixin)
    dept: Mapped["DeptModel | None"] = relationship(
        back_populates="users", 
        foreign_keys=[dept_id], 
        lazy="selectin"
    )
    roles: Mapped[list["RoleModel"]] = relationship(
        secondary="system_user_roles", 
        back_populates="users", 
        lazy="selectin"
    )
    positions: Mapped[list["PositionModel"]] = relationship(
        secondary="system_user_positions", 
        back_populates="users", 
        lazy="selectin"
    )
    tenant: Mapped["TenantModel"] = relationship(
        back_populates="users",
        foreign_keys="UserModel.tenant_id",
        lazy="selectin"
    )
    customer: Mapped["CustomerModel | None"] = relationship(
        back_populates="users",
        foreign_keys="UserModel.customer_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="UserModel.created_id",
        remote_side="UserModel.id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="UserModel.updated_id",
        remote_side="UserModel.id",
        lazy="selectin"
    )

