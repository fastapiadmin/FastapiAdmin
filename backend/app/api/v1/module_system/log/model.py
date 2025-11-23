# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin, TenantMixin, CustomerMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.tenant.model import TenantModel
    from app.api.v1.module_system.customer.model import CustomerModel
    from app.api.v1.module_system.user.model import UserModel


class OperationLogModel(ModelMixin, UserMixin, TenantMixin, CustomerMixin):
    """
    系统日志模型
    
    日志隔离策略:
    ===========
    - 日志记录操作人的实际租户和客户信息
    - tenant_id: 记录操作人所属租户(必填)
    - customer_id: 记录操作人所属客户(如果是客户用户)
    
    用于审计和追踪:
    - 系统用户操作: tenant_id=1, customer_id=NULL
    - 租户用户操作: tenant_id>1, customer_id=NULL
    - 客户用户操作: tenant_id>1, customer_id>1
    
    日志类型:
    - 1: 登录日志
    - 2: 操作日志
    """
    __tablename__: str = "system_log"
    __table_args__: dict[str, str] = ({'comment': '系统日志表'})
    __loader_options__: list[str] = ["creator"]

    type: Mapped[int] = mapped_column(Integer, comment="日志类型(1登录日志 2操作日志)")
    request_path: Mapped[str] = mapped_column(String(255), comment="请求路径")
    request_method: Mapped[str] = mapped_column(String(10), comment="请求方式")
    request_payload: Mapped[str | None] = mapped_column(Text, comment="请求体")
    request_ip: Mapped[str | None] = mapped_column(String(50), comment="请求IP地址")
    login_location: Mapped[str | None] = mapped_column(String(255), comment="登录位置")
    request_os: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="操作系统")
    request_browser: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="浏览器")
    response_code: Mapped[int] = mapped_column(Integer, comment="响应状态码")
    response_json: Mapped[str | None] = mapped_column(Text, nullable=True, comment="响应体")
    process_time: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="处理时间")
    
    # 关联关系 (继承自UserMixin, TenantMixin, CustomerMixin)
    tenant: Mapped["TenantModel"] = relationship(
        foreign_keys="OperationLogModel.tenant_id",
        lazy="selectin"
    )
    customer: Mapped["CustomerModel | None"] = relationship(
        foreign_keys="OperationLogModel.customer_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="OperationLogModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="OperationLogModel.updated_id",
        lazy="selectin"
    )