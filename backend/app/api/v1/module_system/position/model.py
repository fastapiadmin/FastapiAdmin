# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin, TenantMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel
    from app.api.v1.module_system.tenant.model import TenantModel

class PositionModel(ModelMixin, UserMixin, TenantMixin):
    """
    岗位模型
    
    岗位是租户级别的职位定义:
    - 岗位属于租户(tenant_id必填)
    - 岗位不属于客户(customer_id不需要)
    - 用于定义租户内的各种职位(如:总监、经理、专员等)
    - 用户可以同时拥有多个岗位
    
    使用场景:
    - 职位管理: 定义公司组织架构中的各类职位
    - 权限控制: 可以根据岗位分配特定权限
    - 业务流程: 某些审批流可以指定特定岗位处理
    """
    __tablename__: str = "system_position"
    __table_args__: dict[str, str] = ({'comment': '岗位表'})
    __loader_options__: list[str] = ["users", "created_by", "updated_by", "tenant"]
    
    name: Mapped[str] = mapped_column(String(40), nullable=False, comment="岗位名称")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="显示排序")
    
    # 关联关系 (继承自UserMixin和TenantMixin)
    users: Mapped[list["UserModel"]] = relationship(
        secondary="system_user_positions", 
        back_populates="positions", 
        lazy="selectin"
    )
    tenant: Mapped["TenantModel"] = relationship(
        foreign_keys="PositionModel.tenant_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="PositionModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="PositionModel.updated_id",
        lazy="selectin"
    )
