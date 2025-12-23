# -*- coding: utf-8 -*-

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.base_model import ModelMixin


class TenantModel(ModelMixin):
    """
    租户模型
    """
    __tablename__: str = 'sys_tenant'
    __table_args__: dict[str, str] = {'comment': '租户表'}

    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, comment='租户名称')
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, comment='租户编码')
    domain: Mapped[str | None] = mapped_column(String(100), unique=True, comment="租户域名")

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
