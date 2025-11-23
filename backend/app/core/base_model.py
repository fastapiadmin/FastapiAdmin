# -*- coding: utf-8 -*-
"""
基础模型模块
提供跨数据库兼容的基础模型类和类型装饰器
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Integer, DateTime, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, declared_attr, mapped_column


class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    声明式基类

    `AsyncAttrs <https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs>`__

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__

    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__

    兼容 SQLite、MySQL 和 PostgreSQL
    """

    __abstract__ = True


# Mixin: 一种面向对象编程概念, 使结构变得更加清晰, `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
class UserMixin(MappedBase):
    """用户 Mixin 数据类"""
    __abstract__ = True

    created_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('system_users.id', ondelete="SET NULL", onupdate="CASCADE"), nullable=True, index=True, comment="创建人ID")
    updated_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('system_users.id', ondelete="SET NULL", onupdate="CASCADE"), nullable=True, index=True, comment="更新人ID")

    """
        创建人关联关系（延迟加载，避免循环依赖）
        SQLAlchemy ORM 中的这些加载策略用于控制关联对象的加载行为，它们的主要区别如下：

        1.select （默认）：延迟加载，当首次访问关联属性时执行单独的 SELECT 语句获取关联数据。
        2.joined ：预先加载，使用 LEFT OUTER JOIN 在主查询中一次性加载关联数据，适合一对一和多对一关系。
        3.selectin ：预加载优化，先查询主对象，然后使用 IN 子句批量查询所有关联对象，适合一对多和多对多关系。
        4.subquery ：使用子查询方式预加载关联数据，在某些复杂查询场景下有用。
        5.raise ：访问关联属性时抛出异常，禁止加载关联数据。
        6.raise_on_sql ：允许访问关联对象属性，但执行 SQL 时抛出异常。
        7.noload ：不加载关联数据，访问时返回空集合或 None。
        8.immediate ：立即加载，在主对象加载后立即执行额外查询获取关联数据，类似 select 但不延迟。
        9.write_only ：专为写入优化，不允许读取关联数据，只可添加新记录，适合只写不读的场景。
        10.dynamic ：返回动态查询对象而非实际结果集，允许进一步过滤和分页，适合处理大量关联数据。
    """
    @declared_attr
    def created_by(cls) -> Mapped[Optional["UserModel"]]:  # type: ignore
        """
        创建人关联关系（延迟加载，避免循环依赖）
        """
        return relationship(
            "UserModel",
            primaryjoin=f"{cls.__name__}.creator_id == UserModel.id",
            lazy="selectin",
            foreign_keys=lambda: [cls.creator_id],  # type: ignore
            viewonly=True,
            uselist=False  # 明确指定返回单个对象
        )

    @declared_attr
    def updated_by(cls) -> Mapped[Optional["UserModel"]]:  # type: ignore
        """
        更新人关联关系（延迟加载，避免循环依赖）
        """
        return relationship(
            "UserModel",
            primaryjoin=f"{cls.__name__}.creator_id == UserModel.id",
            lazy="selectin",
            foreign_keys=lambda: [cls.creator_id],  # type: ignore
            viewonly=True,
            uselist=False  # 明确指定返回单个对象
        )


class DateTimeMixin(MappedBase):
    """日期时间 Mixin 数据类"""
    __abstract__ = True

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class ModelMixin(DateTimeMixin):
    """
    基础模型混合类
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None, comment="备注/描述")


class CreatorMixin(ModelMixin):
    """
    创建人混合类
    """
    __abstract__ = True

    creator_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('system_users.id', ondelete="SET NULL", onupdate="CASCADE"), nullable=True, index=True, comment="创建人ID")

    @declared_attr
    def creator(cls) -> Mapped[Optional["UserModel"]]:  # type: ignore
        # 其他模型保持原有配置
        return relationship(
            "UserModel",
            primaryjoin=f"{cls.__name__}.creator_id == UserModel.id",
            lazy="selectin",
            foreign_keys=lambda: [cls.creator_id],  # type: ignore
            viewonly=True,
            uselist=False  # 明确指定返回单个对象
        )
