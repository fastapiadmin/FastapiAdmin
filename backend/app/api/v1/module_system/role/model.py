# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import MappedBase, ModelMixin, UserMixin, TenantMixin

# 使用TYPE_CHECKING避免循环导入
if TYPE_CHECKING:
    from app.api.v1.module_system.menu.model import MenuModel
    from app.api.v1.module_system.dept.model import DeptModel
    from app.api.v1.module_system.user.model import UserModel
    from app.api.v1.module_system.tenant.model import TenantModel


class RoleMenusModel(MappedBase):
    """
    角色菜单关联表
    
    定义角色与菜单的多对多关系，用于权限控制
    """
    __tablename__: str = "system_role_menus"
    __table_args__: dict[str, str] = ({'comment': '角色菜单关联表'})

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("system_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="角色ID"
    )
    menu_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("system_menu.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="菜单ID"
    )


class RoleDeptsModel(MappedBase):
    """
    角色部门关联表
    
    定义角色与部门的多对多关系，用于数据权限控制
    仅当角色的data_scope=5(自定义数据权限)时使用此表
    """
    __tablename__: str = "system_role_depts"
    __table_args__: dict[str, str] = ({'comment': '角色部门关联表'})

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("system_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="角色ID"
    )
    dept_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("system_dept.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="部门ID"
    )


class RoleModel(ModelMixin, UserMixin, TenantMixin):
    """
    角色模型
    
    角色是租户级别的权限管理单元:
    - 角色属于租户(tenant_id必填)
    - 角色不属于客户(customer_id不需要)
    - 通过角色分配菜单权限和数据权限
    
    数据权限实现（data_scope字段）:
    ===========================
    - 1: 仅本人数据权限
      * 实现: WHERE created_id = current_user.id
      * 场景: 普通员工只能看自己创建的数据
      
    - 2: 本部门数据权限
      * 实现: WHERE user.dept_id = current_user.dept_id
      * 场景: 部门经理看本部门所有人的数据
      
    - 3: 本部门及以下数据权限
      * 实现: WHERE dept.tree_path LIKE 'current_user.dept.tree_path%'
      * 场景: 总监看本部门及所有下级部门的数据
      
    - 4: 全部数据权限
      * 实现: WHERE tenant_id = current_user.tenant_id
      * 场景: 租户管理员看租户内所有数据
      * 注意: 客户用户即使有此权限也只能看本客户数据
      
    - 5: 自定义数据权限
      * 实现: WHERE dept_id IN (SELECT dept_id FROM system_role_depts WHERE role_id IN current_user.role_ids)
      * 场景: 跨部门权限,如人事可以看多个指定部门
      * 使用: 通过role_depts关联表指定可访问的部门列表
    
    权限叠加规则:
    - 一个用户可以有多个角色
    - 取所有角色data_scope的最大值(4>3>2>5>1)
    - 5(自定义)需要合并所有角色关联的部门
    """
    __tablename__: str = "system_role"
    __table_args__: dict[str, str] = ({'comment': '角色表'})
    __loader_options__: list[str] = ["menus", "depts", "created_by", "updated_by", "tenant"]

    name: Mapped[str] = mapped_column(String(40), nullable=False, comment="角色名称")
    code: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True, comment="角色编码")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=999, comment="显示排序")
    data_scope: Mapped[str | None] = mapped_column(
        String(10), 
        default='1', 
        nullable=True, 
        comment="数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)"
    )
    
    # 关联关系 (继承自UserMixin和TenantMixin)
    menus: Mapped[list["MenuModel"]] = relationship(
        secondary="system_role_menus", 
        back_populates="roles", 
        lazy="selectin", 
        order_by="MenuModel.order"
    )
    depts: Mapped[list["DeptModel"]] = relationship(
        secondary="system_role_depts", 
        back_populates="roles", 
        lazy="selectin"
    )
    users: Mapped[list["UserModel"]] = relationship(
        secondary="system_user_roles", 
        back_populates="roles", 
        lazy="selectin"
    )
    tenant: Mapped["TenantModel"] = relationship(
        foreign_keys="RoleModel.tenant_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="RoleModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="RoleModel.updated_id",
        lazy="selectin"
    )
    