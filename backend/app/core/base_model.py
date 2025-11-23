# -*- coding: utf-8 -*-

import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs


class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    声明式基类

    `AsyncAttrs <https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs>`__

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__

    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__

    兼容 SQLite、MySQL 和 PostgreSQL
    """

    __abstract__: bool = True


class ModelMixin(MappedBase):
    """
    模型混入类 - 提供通用字段和功能

    基础模型混合类 Mixin: 一种面向对象编程概念, 使结构变得更加清晰
    
    数据隔离设计原则：
    ==================
    
    1. 租户隔离 (tenant_id):
        - 用于实现多租户SaaS架构的核心隔离
        - 系统租户(tenant_id=1): 管理平台级数据
        - 普通租户(tenant_id>1): 各自独立的业务数据
        - 大部分业务表都需要tenant_id字段
    
    2. 客户隔离 (customer_id):
        - 用于租户内部的二级隔离
        - 仅部分表需要,如用户、日志等
        - 客户属于租户,实现租户下的业务单元隔离
    
    3. 数据权限 (created_id/updated_id):
        - 配合角色的data_scope字段实现精细化权限控制
        - 1:仅本人 → WHERE created_id = current_user_id
        - 2:本部门 → WHERE user.dept_id = current_user.dept_id
        - 3:本部门及以下 → WHERE dept.tree_path LIKE 'current_dept_path%'
        - 4:全部数据 → WHERE tenant_id = current_tenant_id
        - 5:自定义 → WHERE dept_id IN (role_depts)
    
    4. 软删除 (deleted_at):
        - NULL: 正常数据(未删除)
        - 时间戳: 已删除数据
        - 查询时默认过滤: WHERE deleted_at IS NULL
        - 优点: 数据可恢复,保留审计追踪
        - 注意: 需要在唯一索引中包含deleted_at字段
    
    继承规则：
    - 需要租户隔离的业务表继承此类
    - 不需要隔离的表(如租户表本身)只继承MappedBase
    
    SQLAlchemy加载策略说明：
    - select(默认): 延迟加载,访问时单独查询
    - joined: 使用LEFT JOIN预加载
    - selectin: 使用IN查询批量预加载(推荐用于一对多)
    - subquery: 使用子查询预加载
    - raise/raise_on_sql: 禁止加载
    - noload: 不加载,返回None
    - immediate: 立即加载
    - write_only: 只写不读
    - dynamic: 返回查询对象,支持进一步过滤
    """
    __abstract__: bool = True
    
    # 基础字段
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True, comment='UUID全局唯一标识')
    status: Mapped[str] = mapped_column(String(10), default='0', nullable=False, comment="是否启用(0:启用 1:禁用)")
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注/描述")
    created_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment='创建时间')
    updated_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment='更新时间')
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None, nullable=True, index=True, comment='软删除时间(NULL:未删除, 时间戳:已删除)')


class UserMixin(MappedBase):
    """
    用户审计字段 Mixin
    
    用于记录数据的创建者和更新者
    用于实现数据权限中的"仅本人数据权限"
    
    使用方式:
    --------
    class MyModel(ModelMixin, UserMixin, TenantMixin):
        # 在子类中定义relationship即可,字段已由Mixin提供
        created_by: Mapped["UserModel | None"] = relationship(...)
        updated_by: Mapped["UserModel | None"] = relationship(...)
    """
    __abstract__: bool = True
    
    created_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("system_user.id", ondelete="SET NULL", onupdate="CASCADE"),
        default=None,
        nullable=True,
        index=True,
        comment="创建人ID"
    )
    updated_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("system_user.id", ondelete="SET NULL", onupdate="CASCADE"),
        default=None,
        nullable=True,
        index=True,
        comment="更新人ID"
    )


class TenantMixin(MappedBase):
    """
    租户隔离字段 Mixin
    
    用于实现多租户SaaS架构的核心数据隔离
    几乎所有业务表都需要此字段
    
    使用方式:
    --------
    # 租户级业务表 (必填tenant_id)
    class ProductModel(ModelMixin, UserMixin, TenantMixin):
        # 在子类中定义relationship即可,字段已由Mixin提供
        tenant: Mapped["TenantModel"] = relationship(...)
    
    # 系统级配置表 (可选tenant_id, NULL表示系统级) - 需要覆盖字段
    class MenuModel(ModelMixin, UserMixin, TenantMixin):
        tenant_id: Mapped[int | None] = mapped_column(...)  # 覆盖为可选
        tenant: Mapped["TenantModel | None"] = relationship(...)
    """
    __abstract__: bool = True
    
    tenant_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("system_tenant.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
        comment="所属租户ID"
    )


class CustomerMixin(MappedBase):
    """
    客户隔离字段 Mixin
    
    用于租户内部的二级数据隔离
    仅部分表需要此字段:
    - 客户用户 (必填)
    - 客户业务数据 (根据业务需求)
    - 客户专属通知/日志 (可选)
    
    使用方式:
    --------
    # 客户级业务表
    class OrderModel(ModelMixin, UserMixin, TenantMixin, CustomerMixin):
        # 在子类中定义relationship即可,字段已由Mixin提供
        customer: Mapped["CustomerModel | None"] = relationship(...)
    
    # 租户级业务表 (不需要CustomerMixin)
    class DeptModel(ModelMixin, UserMixin, TenantMixin):
        pass  # 不继承CustomerMixin
    """
    __abstract__: bool = True
    
    customer_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("system_customer.id", ondelete="CASCADE", onupdate="CASCADE"),
        default=None,
        nullable=True,
        index=True,
        comment="所属客户ID(NULL表示租户级数据,>0表示客户级数据)"
    )
