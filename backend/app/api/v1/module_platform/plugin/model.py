from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.base_model import MappedBase, ModelMixin


class PluginModel(ModelMixin):
    """插件注册表 — 超管维护的插件市场列表"""

    __tablename__: str = "platform_plugin"
    __table_args__: dict[str, str] = {"comment": "插件注册表"}

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="插件名称")
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment="插件编码(module_xxx)")
    version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0.0", comment="版本号")
    author: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="作者")
    icon: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="图标URL")
    category: Mapped[str] = mapped_column(String(20), nullable=False, default="tool", comment="分类(tool/ai/monitor/business)")
    price: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="价格(分,0=免费)")
    menu_path: Mapped[str | None] = mapped_column(String(200), nullable=True, comment="菜单路径(安装后显示)")
    permission_prefix: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="权限前缀")
    dependencies: Mapped[str | None] = mapped_column(Text, nullable=True, comment="依赖插件编码(JSON数组)")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="排序")
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="状态(0:启动 1:停用)", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True, comment="备注")

    @validates("name")
    def validate_name(self, key: str, name: str) -> str:
        if not name or not name.strip():
            raise ValueError("插件名称不能为空")
        return name.strip()

    @validates("code")
    def validate_code(self, key: str, code: str) -> str:
        if not code or not code.strip():
            raise ValueError("插件编码不能为空")
        return code.strip()


class TenantPluginModel(MappedBase):
    """租户插件关联表 — 租户已安装的插件"""

    __tablename__: str = "platform_tenant_plugin"
    __table_args__ = (
        UniqueConstraint("tenant_id", "plugin_id", name="uq_tenant_plugin"),
        {"comment": "租户插件关联表"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("platform_tenant.id", ondelete="CASCADE"), nullable=False, index=True, comment="租户ID")
    plugin_id: Mapped[int] = mapped_column(Integer, ForeignKey("platform_plugin.id", ondelete="CASCADE"), nullable=False, index=True, comment="插件ID")
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="启用(True:启用 False:禁用)")
    purchased: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="是否已购买(True:已购买 False:未购买)")
    installed_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False, comment="安装时间")
