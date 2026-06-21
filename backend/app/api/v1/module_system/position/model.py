from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin, TenantMixin, UserMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel


class PositionModel(ModelMixin, TenantMixin, UserMixin):
    """
    岗位模型
    """

    __tablename__: str = "sys_position"
    __table_args__: dict[str, str] = {"comment": "岗位表"}
    __loader_options__: list[str] = [
        "users",
        "created_by",
        "updated_by",
        "deleted_by",
        "tenant_by",
    ]

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="岗位名称")
    code: Mapped[str] = mapped_column(String(64), nullable=False, comment="岗位编码")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="显示排序")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:启动 1:停用)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")

    # 关联关系
    users: Mapped[list["UserModel"]] = relationship(
        secondary="sys_user_positions",
        back_populates="positions",
        lazy="selectin",
    )
