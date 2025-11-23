# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin, TenantMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.tenant.model import TenantModel
    from app.api.v1.module_system.user.model import UserModel


class DictTypeModel(ModelMixin, UserMixin, TenantMixin):
    """
    字典类型表
    
    字典类型隔离策略:
    =============
    - 系统级字典(tenant_id=NULL):
      * 平台预定义的字典,所有租户共享
      * 如:性别、状态等通用字典
    
    - 租户级字典(tenant_id>1):
      * 租户自定义字典,仅本租户可用
      * 如:租户特有的业务分类
    
    - 不需要customer_id:
      * 字典是租户级配置,不属于客户
    
    与字典数据的一对多关系
    """
    __tablename__: str = "system_dict_type"
    __table_args__: dict[str, str] = ({'comment': '字典类型表'})
    __loader_options__: list[str] = ["creator"]

    # 覆盖TenantMixin的tenant_id为可选(支持系统级字典)
    tenant_id: Mapped[int | None] = mapped_column(  # type: ignore
        Integer,
        ForeignKey("system_tenant.id", ondelete="CASCADE"),
        default=None,
        nullable=True,
        index=True,
        comment="所属租户ID(NULL表示系统级字典,所有租户共享)"
    )

    dict_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='字典名称')
    dict_type: Mapped[str] = mapped_column(String(100), nullable=False, comment='字典类型')
    
    # 关联关系 (继承自UserMixin和TenantMixin)
    dict_datas: Mapped[list["DictDataModel"]] = relationship(
        back_populates="dict_type_rel", 
        lazy="selectin"
    )
    tenant: Mapped["TenantModel | None"] = relationship(
        foreign_keys="DictTypeModel.tenant_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="DictTypeModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="DictTypeModel.updated_id",
        lazy="selectin"
    )


class DictDataModel(ModelMixin, UserMixin, TenantMixin):
    """
    字典数据表
    
    与字典类型表的多对一关系
    用于存储具体的字典项数据
    
    隔离策略继承自字典类型:
    - 系统字典的数据项也是系统级(tenant_id=NULL)
    - 租户字典的数据项也是租户级(tenant_id>1)
    - 不需要customer_id
    """
    __tablename__: str = "system_dict_data"
    __table_args__: dict[str, str] = ({'comment': '字典数据表'})
    __loader_options__: list[str] = ["creator", "dict_type"]
    
    # 覆盖TenantMixin的tenant_id为可选(支持系统级字典数据)
    tenant_id: Mapped[int | None] = mapped_column(  # type: ignore
        Integer,
        ForeignKey("system_tenant.id", ondelete="CASCADE"),
        default=None,
        nullable=True,
        index=True,
        comment="所属租户ID(NULL表示系统级字典数据,所有租户共享)"
    )
    
    dict_sort: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='字典排序')
    dict_label: Mapped[str] = mapped_column(String(100), nullable=False, comment='字典标签')
    dict_value: Mapped[str] = mapped_column(String(100), nullable=False, comment='字典键值')
    css_class: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='样式属性（其他样式扩展）')
    list_class: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='表格回显样式')
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment='是否默认（True是 False否）')
    
    # 字典类型关联
    dict_type_id: Mapped[int | None] = mapped_column(
        ForeignKey('system_dict_type.id'), 
        nullable=True, 
        comment='字典类型ID'
    )
    
    # 关联关系 (继承自UserMixin和TenantMixin)
    dict_type_rel: Mapped["DictTypeModel | None"] = relationship(
        back_populates="dict_datas", 
        lazy="selectin"
    )
    tenant: Mapped["TenantModel | None"] = relationship(
        foreign_keys="DictDataModel.tenant_id",
        lazy="selectin"
    )
    created_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="DictDataModel.created_id",
        lazy="selectin"
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        foreign_keys="DictDataModel.updated_id",
        lazy="selectin"
    )