# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import MappedBase, ModelMixin, UserMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.menu.model import MenuModel
    from app.api.v1.module_system.dept.model import DeptModel
    from app.api.v1.module_system.user.model import UserModel


class RoleMenusModel(MappedBase):
    """
    角色菜单关联表
    
    定义角色与菜单的多对多关系，用于权限控制
    """
    __tablename__: str = "sys_role_menus"
    __table_args__: dict[str, str] = ({'comment': '角色菜单关联表'})

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="角色ID"
    )
    menu_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_menu.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="菜单ID"
    )


class RoleDeptsModel(MappedBase):
    """
    角色部门关联表
    
    定义角色与部门的多对多关系，用于数据权限控制
    仅当角色的data_scope=5(自定义数据权限)时使用此表
    """
    __tablename__: str = "sys_role_depts"
    __table_args__: dict[str, str] = ({'comment': '角色部门关联表'})

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="角色ID"
    )
    dept_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_dept.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="部门ID"
    )


class RoleModel(ModelMixin, UserMixin):
    """
    角色模型
    """
    __tablename__: str = "sys_role"
    __table_args__: dict[str, str] = ({'comment': '角色表'})
    __loader_options__: list[str] = ["menus", "depts", "created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(40), nullable=False, comment="角色名称")
    code: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True, comment="角色编码")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=999, comment="显示排序")
    data_scope: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)")
    
    # 关联关系 (继承自UserMixin)
    menus: Mapped[list["MenuModel"]] = relationship(
        secondary="sys_role_menus", 
        back_populates="roles", 
        lazy="selectin", 
        order_by="MenuModel.order"
    )
    depts: Mapped[list["DeptModel"]] = relationship(
        secondary="sys_role_depts", 
        back_populates="roles", 
        lazy="selectin"
    )
    users: Mapped[list["UserModel"]] = relationship(
        secondary="sys_user_roles", 
        back_populates="roles", 
        lazy="selectin"
    )
