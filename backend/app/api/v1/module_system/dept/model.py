from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import PermissionFilterStrategy
from app.core.base_model import ModelMixin, TenantMixin, UserMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.role.model import RoleModel
    from app.api.v1.module_system.user.model import UserModel


class DeptModel(ModelMixin, TenantMixin, UserMixin):
    """
    部门模型
    """

    __tablename__: str = "sys_dept"
    __table_args__ = (UniqueConstraint("tenant_id", "code"), {"comment": "部门表"})
    __tree_children_attr__: str = "children"
    __loader_options__: list[str] = [
        "children",
        "created_by",
        "updated_by",
        "deleted_by",
        "tenant_by",
    ]
    __permission_strategy__: PermissionFilterStrategy = PermissionFilterStrategy.DEPT_RELATION

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="部门名称")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:启动 1:停用)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=999, comment="显示排序")
    code: Mapped[str] = mapped_column(String(64), nullable=False, comment="部门编码")
    leader: Mapped[str | None] = mapped_column(String(32), default=None, comment="部门负责人")
    phone: Mapped[str | None] = mapped_column(String(20), default=None, comment="手机")
    email: Mapped[str | None] = mapped_column(String(128), default=None, comment="邮箱")
    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_dept.id", ondelete="SET NULL", onupdate="CASCADE"),
        default=None,
        index=True,
        comment="父级部门ID",
    )
    parent: Mapped["DeptModel | None"] = relationship(
        back_populates="children",
        remote_side="DeptModel.id",
        foreign_keys=[parent_id],
        uselist=False,
    )
    children: Mapped[list["DeptModel"]] = relationship(back_populates="parent", foreign_keys=[parent_id], lazy="selectin")
    roles: Mapped[list["RoleModel"]] = relationship(secondary="sys_role_depts", back_populates="depts", lazy="selectin")
    users: Mapped[list["UserModel"]] = relationship(
        back_populates="dept",
        foreign_keys="UserModel.dept_id",
        lazy="selectin",
    )
