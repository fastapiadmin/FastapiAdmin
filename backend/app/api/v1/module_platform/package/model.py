from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.base_model import MappedBase, ModelMixin


class PackageModel(ModelMixin):
    """
    套餐模型 - 定义租户可用的功能套餐

    status: 0=正常 1=禁用
    """

    __tablename__: str = "platform_package"
    __table_args__: dict[str, str] = {"comment": "租户套餐表"}

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="套餐名称")
    code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="套餐编码")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="排序")
    price: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="价格(分)")
    period: Mapped[str] = mapped_column(String(10), nullable=False, default="month", comment="计费周期(month/year)")
    trial_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="免费试用天数")
    max_users: Mapped[int] = mapped_column(Integer, nullable=False, default=10, comment="最大用户数")
    max_roles: Mapped[int] = mapped_column(Integer, nullable=False, default=5, comment="最大角色数")
    max_depts: Mapped[int] = mapped_column(Integer, nullable=False, default=10, comment="最大部门数")
    max_storage_mb: Mapped[int] = mapped_column(Integer, nullable=False, default=1024, comment="最大存储(MB)")
    rate_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=60, comment="API速率限制(请求/10秒)")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:启动 1:停用)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")

    @validates("name")
    def validate_name(self, key: str, name: str) -> str:
        if not name or not name.strip():
            raise ValueError("套餐名称不能为空")
        return name

    @validates("code")
    def validate_code(self, key: str, code: str) -> str:
        if not code or not code.strip():
            raise ValueError("套餐编码不能为空")
        if not code.isalnum():
            raise ValueError("套餐编码只能包含字母和数字")
        return code


class PackageMenuModel(MappedBase):
    """
    套餐-菜单关联表 — 定义套餐包含的菜单资源
    """

    __tablename__: str = "platform_package_menu"
    __table_args__ = (
        UniqueConstraint("package_id", "menu_id", name="uq_package_menu"),
        {"comment": "套餐菜单关联表"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    package_id: Mapped[int] = mapped_column(Integer, ForeignKey("platform_package.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True, comment="套餐ID")
    menu_id: Mapped[int] = mapped_column(Integer, ForeignKey("platform_menu.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True, comment="菜单ID")


class PackagePluginModel(MappedBase):
    """
    套餐-插件关联表 — 定义套餐包含的插件资源
    """

    __tablename__: str = "platform_package_plugin"
    __table_args__ = (
        UniqueConstraint("package_id", "plugin_id", name="uq_package_plugin"),
        {"comment": "套餐插件关联表"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    package_id: Mapped[int] = mapped_column(Integer, ForeignKey("platform_package.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True, comment="套餐ID")
    plugin_id: Mapped[int] = mapped_column(Integer, ForeignKey("platform_plugin.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True, comment="插件ID")
