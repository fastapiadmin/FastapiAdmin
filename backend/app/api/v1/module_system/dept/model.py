# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import ModelMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.role.model import RoleModel
    from app.api.v1.module_system.user.model import UserModel


class DeptModel(ModelMixin):
    """
    部门模型
    """
    __tablename__: str = "sys_dept"
    __table_args__: dict[str, str] = ({'comment': '部门表'})

    name: Mapped[str] = mapped_column(String(40), nullable=False, comment="部门名称")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=999, comment="显示排序")
    code: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True, comment="部门编码")
    leader: Mapped[str | None] = mapped_column(String(32), default=None, comment='部门负责人')
    phone: Mapped[str | None] = mapped_column(String(11), default=None, comment='手机')
    email: Mapped[str | None] = mapped_column(String(64), default=None, comment='邮箱')
    
    # 树形结构字段
    parent_id: Mapped[int | None] = mapped_column(
        Integer, 
        ForeignKey("sys_dept.id", ondelete="SET NULL", onupdate="CASCADE"), 
        default=None, 
        index=True, 
        comment="父级部门ID"
    )
    # 关联关系
    parent: Mapped["DeptModel | None"] = relationship(
        back_populates='children', 
        remote_side="DeptModel.id",
        foreign_keys=[parent_id],
        uselist=False
    )
    children: Mapped[list["DeptModel"]] = relationship(
        back_populates='parent', 
        foreign_keys=[parent_id],
        lazy="selectin"
    )
    roles: Mapped[list["RoleModel"]] = relationship(
        secondary="sys_role_depts", 
        back_populates="depts", 
        lazy="selectin"
    )
    users: Mapped[list["UserModel"]] = relationship(
        back_populates="dept",
        foreign_keys="UserModel.dept_id",
        lazy="selectin"
    )
