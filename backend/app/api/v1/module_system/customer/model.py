# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.core.base_model import ModelMixin, UserMixin, TenantMixin


if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel


class CustomerModel(ModelMixin, UserMixin, TenantMixin):
    """
    客户表
    
    客户是租户下的业务实体，用于业务数据的二级隔离:
    - 一个租户可以有多个客户
    - 客户用户(user.customer_id>0)只能访问其所属客户的数据
    - 客户表需要tenant_id(属于哪个租户)
    - 客户表不需要customer_id(客户不属于客户,避免循环)
    
    典型场景:
    - 代理商系统: 租户=总公司, 客户=各地代理商
    - SaaS平台: 租户=企业, 客户=企业下的子公司/部门
    """
    __tablename__: str = 'system_customer'
    __table_args__: dict[str, str] = ({'comment': '客户表'})
    __loader_options__: list[str] = ["created_by", "updated_by", "tenant"]
    
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment='客户名称')
    code: Mapped[str] = mapped_column(String(20), nullable=False, index=True, comment='客户编码')
    
    users: Mapped[list["UserModel"]] = relationship(
        back_populates="customer",
        foreign_keys="UserModel.customer_id",
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
