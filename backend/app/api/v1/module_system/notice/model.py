# -*- coding: utf-8 -*-

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin, TenantMixin, CustomerMixin


class NoticeModel(ModelMixin, UserMixin, TenantMixin, CustomerMixin):
    """
    通知公告表
    
    通知公告隔离策略:
    ==============
    - 系统通知(tenant_id=1, customer_id=NULL):
      * 平台级通知,发送给所有租户
      * 如:系统维护公告、版本更新通知
      
    - 租户通知(tenant_id>1, customer_id=NULL):
      * 租户级通知,发送给本租户所有用户
      * 如:租户内部公告、政策通知
      
    - 客户通知(tenant_id>1, customer_id>1):
      * 客户级通知,仅发送给特定客户的用户
      * 如:针对某个客户的专属通知
    
    用于存储系统通知公告信息，包括：
    - 通知标题、内容、类型和状态
    - 创建人和创建时间
    - 通知的可见范围和发布状态
    """
    __tablename__: str = "system_notice"
    __table_args__: dict[str, str] = ({'comment': '通知公告表'})
    __loader_options__: list[str] = ["created_by", "updated_by", "tenant", "customer"]

    notice_title: Mapped[str] = mapped_column(String(50), nullable=False, comment='公告标题')
    notice_type: Mapped[str] = mapped_column(String(50), nullable=False, comment='公告类型(1通知 2公告)')
    notice_content: Mapped[str | None] = mapped_column(Text, nullable=True, comment='公告内容')
