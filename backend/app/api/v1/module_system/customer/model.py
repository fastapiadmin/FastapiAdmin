# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.core.base_model import ModelMixin, UserMixin, TenantMixin
if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel


class CustomerModel(ModelMixin, TenantMixin, UserMixin):
    """
    客户表
    """
    __tablename__: str = 'sys_customer'
    __table_args__: dict[str, str] = ({'comment': '客户表'})
    __loader_options__: list[str] = ["created_by", "updated_by", "tenant"]
    
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment='客户名称')
    code: Mapped[str] = mapped_column(String(20), nullable=False, index=True, comment='客户编码')
    
    
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
