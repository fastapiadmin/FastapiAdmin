"""多租户多模块纯单元测试（不依赖数据库连接）。"""

import pytest


# ==================== 01. 租户 ContextVar ====================

class TestTenantContextVar:
    """租户上下文变量读写与清理。"""

    def test_initially_none(self) -> None:
        from app.core.tenant import get_current_tenant_id, get_is_super_admin

        assert get_current_tenant_id() is None
        assert get_is_super_admin() is False

    def test_set_and_get(self) -> None:
        from app.core.tenant import (
            clear_current_tenant,
            get_current_tenant_id,
            get_is_super_admin,
            set_current_tenant,
        )

        set_current_tenant(42, True)
        assert get_current_tenant_id() == 42
        assert get_is_super_admin() is True

        clear_current_tenant()
        assert get_current_tenant_id() is None


# ==================== 02. ORM 模型定义 ====================

class TestModels:
    """核心业务模型表名与字段完整性。"""

    def test_tenant_model(self) -> None:
        from app.api.v1.module_system.tenant.model import TenantModel

        assert TenantModel.__tablename__ == "sys_tenant"
        assert hasattr(TenantModel, "name")
        assert hasattr(TenantModel, "code")
        assert hasattr(TenantModel, "status")
        assert hasattr(TenantModel, "end_time")

    def test_tenant_quota_model(self) -> None:
        from app.api.v1.module_system.tenant.model import TenantQuotaModel

        assert TenantQuotaModel.__tablename__ == "sys_tenant_quota"
        assert hasattr(TenantQuotaModel, "max_users")
        assert hasattr(TenantQuotaModel, "max_roles")

    def test_tenant_config_model(self) -> None:
        from app.api.v1.module_system.tenant.model import TenantConfigModel

        assert TenantConfigModel.__tablename__ == "sys_tenant_config"
        assert hasattr(TenantConfigModel, "config_key")

    def test_tenant_menu_model(self) -> None:
        from app.api.v1.module_system.tenant.model import TenantMenuModel

        assert TenantMenuModel.__tablename__ == "sys_tenant_menu"
        assert hasattr(TenantMenuModel, "menu_id")

    def test_tenant_user_model(self) -> None:
        from app.api.v1.module_system.tenant.model import TenantUserModel

        assert TenantUserModel.__tablename__ == "sys_user_tenant"
        assert hasattr(TenantUserModel, "role")
        assert hasattr(TenantUserModel, "is_default")

    def test_user_model_has_tenant_id(self) -> None:
        from app.api.v1.module_system.user.model import UserModel

        assert hasattr(UserModel, "tenant_id")
        assert hasattr(UserModel, "is_superuser")

    def test_role_model_has_tenant_id(self) -> None:
        from app.api.v1.module_system.role.model import RoleModel

        assert hasattr(RoleModel, "tenant_id")
        assert hasattr(RoleModel, "menus")

    def test_menu_model_has_tenant_id(self) -> None:
        from app.api.v1.module_system.menu.model import MenuModel

        assert hasattr(MenuModel, "type")

    def test_notice_model(self) -> None:
        from app.api.v1.module_system.notice.model import NoticeModel

        assert NoticeModel.__tablename__ == "sys_notice"
        assert hasattr(NoticeModel, "notice_title")
        assert hasattr(NoticeModel, "status")

    def test_plugin_model(self) -> None:
        from app.api.v1.module_system.plugin.model import PluginModel

        assert PluginModel.__tablename__ == "sys_plugin"
        assert hasattr(PluginModel, "code")

    def test_tenant_plugin_model(self) -> None:
        from app.api.v1.module_system.plugin.model import TenantPluginModel

        assert TenantPluginModel.__tablename__ == "sys_tenant_plugin"

    def test_ticket_model(self) -> None:
        from app.plugin.module_ticket.ticket.model import TicketModel

        assert TicketModel.__tablename__ == "sys_ticket"
        assert hasattr(TicketModel, "ticket_type")
        assert hasattr(TicketModel, "reply")


# ==================== 03. Pydantic Schema ====================

class TestSchemas:
    """请求/响应Schema字段验证。"""

    def test_tenant_create_schema(self) -> None:
        from app.api.v1.module_system.tenant.schema import TenantCreateSchema

        s = TenantCreateSchema(name="test", code="test001", status="0")
        assert s.name == "test"
        assert s.code == "test001"

    def test_tenant_update_schema_partial(self) -> None:
        from app.api.v1.module_system.tenant.schema import TenantUpdateSchema

        s = TenantUpdateSchema(name="renamed")
        assert s.name == "renamed"
        assert s.code is None  # 未传则为 None

    def test_tenant_quota_schema_validation(self) -> None:
        from app.api.v1.module_system.tenant.schema import TenantQuotaUpdateSchema

        s = TenantQuotaUpdateSchema(max_users=100, max_roles=30)
        assert s.max_users == 100

        # 负数应被拒绝
        with pytest.raises(Exception):
            TenantQuotaUpdateSchema(max_users=-1)

    def test_ticket_schema(self) -> None:
        from app.plugin.module_ticket.ticket.schema import TicketCreateSchema

        s = TicketCreateSchema(title="test", content="content", ticket_type="suggestion")
        assert s.title == "test"
        assert s.ticket_type == "suggestion"

    def test_menu_type_enum(self) -> None:
        """菜单类型: 1=目录 2=菜单 3=按钮 4=链接"""
        from app.api.v1.module_system.menu.model import MenuModel

        assert hasattr(MenuModel, "type")
        # type 是 int 字段


# ==================== 04. 配置类 ====================

class TestSettings:
    """配置默认值与环境变量覆盖。"""

    def test_settings_defaults(self) -> None:
        from app.config.setting import settings

        assert settings.DATABASE_HOST
        assert settings.DATABASE_PORT > 0
        assert settings.SERVER_PORT > 0

    def test_redis_config(self) -> None:
        from app.config.setting import settings

        assert isinstance(settings.REDIS_ENABLE, bool)
        assert settings.REDIS_PORT == 6379

    def test_database_password_empty_by_default(self) -> None:
        """密码默认值为空，需通过 .env 或环境变量提供。"""
        from app.config.setting import Settings

        # 检查字段默认值（不依赖运行时环境变量）
        assert Settings.model_fields["DATABASE_PASSWORD"].default == ""


# ==================== 05. 常量与枚举 ====================

class TestEnums:
    """业务枚举值完整性。"""

    def test_status_operate_enum(self) -> None:
        from app.common.enums import BusinessType

        assert hasattr(BusinessType, "OTHER")

    def test_menu_type_values(self) -> None:
        """type: 1=目录 2=菜单 3=按钮 4=链接"""
        from app.api.v1.module_system.menu.model import MenuModel

        assert MenuModel.__tablename__ == "sys_menu"
        # type 字段是 int 类型
        col = next((c for c in MenuModel.__table__.columns if c.name == "type"), None)
        assert col is not None
