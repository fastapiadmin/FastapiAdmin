# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel


class PositionModel(ModelMixin, UserMixin):
    """
    岗位模型
    """
    __tablename__: str = "sys_position"
    __table_args__: dict[str, str] = ({'comment': '岗位表'})
    __loader_options__: list[str] = ["users", "created_by", "updated_by"]
    
    name: Mapped[str] = mapped_column(String(40), nullable=False, comment="岗位名称")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="显示排序")
    
    # 关联关系
    users: Mapped[list["UserModel"]] = relationship(
        secondary="sys_user_positions", 
        back_populates="positions", 
        lazy="selectin"
    )
