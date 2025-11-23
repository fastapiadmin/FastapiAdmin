# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import Boolean, String, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin, TenantMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.role.model import RoleModel
    from app.api.v1.module_system.tenant.model import TenantModel
    from app.api.v1.module_system.user.model import UserModel


class MenuModel(ModelMixin, UserMixin, TenantMixin):
    """
    菜单表 - 用于存储系统菜单信息
    
    菜单类型说明:
    - 1: 目录(一级菜单)
    - 2: 菜单(二级菜单) 
    - 3: 按钮/权限(页面内按钮权限)
    - 4: 外部链接
    
    菜单隔离策略:
    ===========
    - 系统级菜单(tenant_id=1或NULL): 
      * 平台基础菜单,所有租户共享
      * 如:系统管理、用户管理等核心功能
    
    - 租户级菜单(tenant_id>1):
      * 租户自定义菜单,仅本租户可见
      * 如:租户特有的业务模块
      * 租户管理员可以为本租户添加自定义菜单
    
    - 不需要customer_id:
      * 菜单是租户级资源,不属于客户
      * 客户用户的菜单权限通过role控制
    
    支持树形结构(通过parent_id自关联)
    """
    __tablename__: str = "system_menu"
    __table_args__: dict[str, str] = ({'comment': '菜单表'})
    __loader_options__: list[str] = ["roles"]

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='菜单名称')
    type: Mapped[int] = mapped_column(Integer, nullable=False, default=2, comment='菜单类型(1:目录 2:菜单 3:按钮/权限 4:链接)')
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=999, comment='显示排序')
    permission: Mapped[str | None] = mapped_column(String(100), comment='权限标识(如:module_system:user:list)')
    icon: Mapped[str | None] = mapped_column(String(50), comment='菜单图标')
    route_name: Mapped[str | None] = mapped_column(String(100), comment='路由名称')
    route_path: Mapped[str | None] = mapped_column(String(200), comment='路由路径')
    component_path: Mapped[str | None] = mapped_column(String(200), comment='组件路径')
    redirect: Mapped[str | None] = mapped_column(String(200), comment='重定向地址')
    hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment='是否隐藏(True:隐藏 False:显示)')
    keep_alive: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment='是否缓存(True:是 False:否)')
    always_show: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment='是否始终显示(True:是 False:否)')
    title: Mapped[str | None] = mapped_column(String(50), comment='菜单标题')
    params: Mapped[list[dict[str, str]] | None] = mapped_column(JSON, comment='路由参数(JSON对象)')
    affix: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment='是否固定标签页(True:是 False:否)')
    
    # 树形结构
    parent_id: Mapped[int | None] = mapped_column(
        Integer, 
        ForeignKey('system_menu.id', ondelete='SET NULL'), 
        default=None, 
        index=True, 
        comment='父菜单ID'
    )
    
    # 关联关系 (继承自UserMixin和TenantMixin)
    parent: Mapped["MenuModel | None"] = relationship(
        back_populates='children', 
        remote_side="MenuModel.id", 
        foreign_keys="MenuModel.parent_id",
        uselist=False
    )
    children: Mapped[list["MenuModel"] | None] = relationship(
        back_populates='parent', 
        foreign_keys="MenuModel.parent_id",
        order_by="MenuModel.order"
    )
    roles: Mapped[list["RoleModel"]] = relationship(
        secondary="system_role_menus", 
        back_populates="menus", 
        lazy="selectin"
    )
    tenant: Mapped["TenantModel | None"] = relationship(
        foreign_keys="MenuModel.tenant_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="MenuModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="MenuModel.updated_id",
        lazy="selectin"
    )