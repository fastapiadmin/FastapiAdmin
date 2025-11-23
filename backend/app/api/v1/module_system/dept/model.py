# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin, TenantMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.role.model import RoleModel
    from app.api.v1.module_system.user.model import UserModel
    from app.api.v1.module_system.tenant.model import TenantModel

class DeptModel(ModelMixin, UserMixin, TenantMixin):
    """
    部门模型
    
    部门是租户级别的组织架构，用于实现数据权限控制:
    - 部门属于租户(tenant_id必填)
    - 部门不属于客户(customer_id不需要)
    - 支持无限层级嵌套的树形结构
    - tree_path字段用于高效实现"本部门及以下"数据权限
    
    数据权限实现:
    - 本部门: WHERE user.dept_id = current_user.dept_id
    - 本部门及以下: WHERE dept.tree_path LIKE 'current_dept.tree_path%'
    - 自定义: WHERE dept_id IN (role关联的部门ID列表)
    
    tree_path格式:
    - 格式: /1/3/5/ 表示从根部门到当前部门的完整路径
    - 根部门: /1/
    - 二级部门: /1/3/
    - 三级部门: /1/3/5/
    """
    __tablename__: str = "system_dept"
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
        ForeignKey("system_dept.id", ondelete="SET NULL", onupdate="CASCADE"), 
        default=None, 
        index=True, 
        comment="父级部门ID"
    )
    tree_path: Mapped[str | None] = mapped_column(
        String(500), 
        default=None, 
        index=True, 
        comment="部门树路径(格式:/1/2/3/),用于高效查询本部门及以下数据权限"
    )
    
    # 关联关系 (继承自UserMixin和TenantMixin)
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
        secondary="system_role_depts", 
        back_populates="depts", 
        lazy="selectin"
    )
    users: Mapped[list["UserModel"]] = relationship(
        back_populates="dept",
        foreign_keys="UserModel.dept_id",
        lazy="selectin"
    )
    tenant: Mapped["TenantModel"] = relationship(
        back_populates="depts",
        foreign_keys="DeptModel.tenant_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="DeptModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="DeptModel.updated_id",
        lazy="selectin"
    )
    