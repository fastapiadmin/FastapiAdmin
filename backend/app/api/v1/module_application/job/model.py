# -*- coding: utf-8 -*-

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import MappedBase, ModelMixin, UserMixin, TenantMixin, CustomerMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel
    from app.api.v1.module_system.tenant.model import TenantModel
    from app.api.v1.module_system.customer.model import CustomerModel


class JobModel(ModelMixin, UserMixin, TenantMixin, CustomerMixin):
    """
    定时任务调度表
    
    数据隔离策略:
    ===========
    - 系统级任务: tenant_id=1, customer_id=NULL (平台定时任务,如系统维护)
    - 租户级任务: tenant_id>1, customer_id=NULL (租户定时任务,如数据统计)
    - 客户级任务: tenant_id>1, customer_id>0 (客户专属定时任务)
    
    任务状态:
    - 0: 运行中
    - 1: 暂停中
    """
    __tablename__: str = 'app_job'
    __table_args__: dict[str, str] = ({'comment': '定时任务调度表'})
    __loader_options__: list[str] = ["job_logs", "created_by", "updated_by", "tenant", "customer"]

    name: Mapped[str | None] = mapped_column(String(64), nullable=True, default='', comment='任务名称')
    jobstore: Mapped[str | None] = mapped_column(String(64), nullable=True, default='default', comment='存储器')
    executor: Mapped[str | None] = mapped_column(String(64), nullable=True, default='default', comment='执行器:将运行此作业的执行程序的名称')
    trigger: Mapped[str] = mapped_column(String(64), nullable=False, comment='触发器:控制此作业计划的 trigger 对象')
    trigger_args: Mapped[str | None] = mapped_column(Text, nullable=True, comment='触发器参数')
    func: Mapped[str] = mapped_column(Text, nullable=False, comment='任务函数')
    args: Mapped[str | None] = mapped_column(Text, nullable=True, comment='位置参数')
    kwargs: Mapped[str | None] = mapped_column(Text, nullable=True, comment='关键字参数')
    coalesce: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False, comment='是否合并运行:是否在多个运行时间到期时仅运行作业一次')
    max_instances: Mapped[int] = mapped_column(Integer, nullable=True, default=1, comment='最大实例数:允许的最大并发执行实例数')
    start_date: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='开始时间')
    end_date: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='结束时间')
    
    # 关联关系
    job_logs: Mapped[list['JobLogModel'] | None] = relationship(
        back_populates="job", 
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="JobModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="JobModel.updated_id",
        lazy="selectin"
    )
    tenant: Mapped["TenantModel"] = relationship(
        foreign_keys="JobModel.tenant_id",
        lazy="selectin"
    )
    customer: Mapped["CustomerModel | None"] = relationship(
        foreign_keys="JobModel.customer_id",
        lazy="selectin"
    )


class JobLogModel(MappedBase):
    """
    定时任务调度日志表
    
    日志表不需要租户隔离,因为通过job关联已经隐式隔离
    但为了查询性能,可以考虑冗余tenant_id
    """
    __tablename__: str = 'app_job_log'
    __table_args__: dict[str, str] = ({'comment': '定时任务调度日志表'})
    __loader_options__: list[str] = ["job"]

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    status: Mapped[str] = mapped_column(String(10), default='0', nullable=False, comment="执行状态(0:成功 1:失败)")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, default=None, comment="备注/描述")
    job_name: Mapped[str] = mapped_column(String(64), nullable=False, comment='任务名称')
    job_group: Mapped[str] = mapped_column(String(64), nullable=False, comment='任务组名')
    job_executor: Mapped[str] = mapped_column(String(64), nullable=False, comment='任务执行器')
    invoke_target: Mapped[str] = mapped_column(String(500), nullable=False, comment='调用目标字符串')
    job_args: Mapped[str | None] = mapped_column(String(255), nullable=True, default='', comment='位置参数')
    job_kwargs: Mapped[str | None] = mapped_column(String(255), nullable=True, default='', comment='关键字参数')
    job_trigger: Mapped[str | None] = mapped_column(String(255), nullable=True, default='', comment='任务触发器')
    job_message: Mapped[str | None] = mapped_column(String(500), nullable=True, default='', comment='日志信息')
    exception_info: Mapped[str | None] = mapped_column(String(2000), nullable=True, default='', comment='异常信息')
    create_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    
    # 任务关联
    job_id: Mapped[int | None] = mapped_column(
        ForeignKey('app_job.id', ondelete="CASCADE"), 
        nullable=True,
        index=True,
        comment='任务ID'
    )
    job: Mapped["JobModel | None"] = relationship(
        back_populates="job_logs", 
        lazy="selectin"
    )