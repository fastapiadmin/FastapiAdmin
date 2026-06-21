from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.common.enums import PermissionFilterStrategy
from app.core.base_model import MappedBase, ModelMixin

if TYPE_CHECKING:
    from app.api.v1.module_platform.package.model import PackageModel


class TenantModel(ModelMixin):
    """
    租户模型 - 单一大表设计

    - 系统租户(id=1)：平台管理，由超级管理员维护，不受套餐限制
    - 普通租户(id>1)：配额和菜单通过关联的 Package 控制
    - 配置字段直接集成到主表
    """

    __tablename__: str = "platform_tenant"
    __table_args__: dict[str, str] = {"comment": "租户表"}
    __permission_strategy__: PermissionFilterStrategy = PermissionFilterStrategy.DATA_SCOPE

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="租户名称")
    code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="租户编码")
    contact_name: Mapped[str | None] = mapped_column(String(64), nullable=True, default=None, comment="联系人姓名")
    contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True, default=None, comment="联系人电话")
    contact_email: Mapped[str | None] = mapped_column(String(128), nullable=True, default=None, comment="联系人邮箱")
    address: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None, comment="地址")
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None, comment="域名")
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None, comment="Logo URL")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="排序")
    package_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("platform_package.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True, default=None, index=True, comment="关联套餐ID")
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None, comment="开始时间")
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None, comment="结束时间")
    version: Mapped[str | None] = mapped_column(String(20), nullable=True, default=None, comment="版本号")
    favicon: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None, comment="favicon地址")
    login_bg: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None, comment="登录背景地址")
    copyright: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None, comment="版权信息")
    keep_record: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None, comment="备案号")
    help_doc: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None, comment="帮助文档地址")
    privacy: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None, comment="隐私政策地址")
    clause: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None, comment="服务条款地址")
    git_code: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None, comment="源码地址")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:启动 1:停用)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")

    # 关联关系
    package: Mapped["PackageModel | None"] = relationship("PackageModel", lazy="selectin")

    @validates("name")
    def validate_name(self, key: str, name: str) -> str:
        if not name or not name.strip():
            raise ValueError("名称不能为空")
        return name

    @validates("code")
    def validate_code(self, key: str, code: str) -> str:
        if not code or not code.strip():
            raise ValueError("编码不能为空")
        if not code.isalnum():
            raise ValueError("编码只能包含字母和数字")
        return code


class TenantUserModel(MappedBase):
    """
    用户-租户关联表

    支持一个用户关联多个租户（如顾问在多个租户间切换）。
    每个用户有一个默认租户（is_default=1），用于登录后的默认上下文。
    """

    __tablename__: str = "platform_user_tenant"
    __table_args__ = (
        UniqueConstraint("user_id", "tenant_id", name="uq_user_tenant"),
        {"comment": "用户租户关联表"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_user.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True, comment="用户ID")
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("platform_tenant.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True, comment="租户ID")
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="member", comment="租户内角色(owner:拥有者 admin:管理员 member:成员)")
    is_default: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, comment="是否默认租户(0:否 1:是)")
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
