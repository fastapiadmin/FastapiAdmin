"""
模块接口测试 —— module_platform（平台管理）
认证数据测试：admin 登录后验证 CRUD 真实数据。
"""

from conftest import assert_route  # noqa: F401
from fastapi.testclient import TestClient


class TestTenant:
    """租户管理接口。"""

    def test_tenant_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/list", auth=auth_headers)

    def test_tenant_detail(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/detail/1", auth=auth_headers)

    def test_tenant_create(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/tenant/create", auth=auth_headers,
            json={"name": "测试租户", "code": "test_tenant", "contact_name": "张三", "contact_phone": "13800000000"},
        )

    def test_tenant_update(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PUT", "/platform/tenant/update/1", auth=auth_headers,
            json={"name": "更新租户"},
        )

    def test_tenant_delete(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/platform/tenant/delete", auth=auth_headers, json=[9999])

    def test_tenant_config_info(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/1/config/info", auth=auth_headers)

    def test_tenant_config(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "PUT", "/platform/tenant/1/config", auth=auth_headers, json={"key": "val"})

    def test_tenant_renew(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PUT", "/platform/tenant/renew/1", auth=auth_headers,
            json={"days": 30},
        )

    def test_tenant_status(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PUT", "/platform/tenant/status/1", auth=auth_headers,
            json={"status": 1},
        )

    def test_tenant_status_batch(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PATCH", "/platform/tenant/status/batch", auth=auth_headers,
            json={"ids": [1], "status": 1},
        )

    def test_tenant_package_change_preview(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/1/package-change-preview", auth=auth_headers)

    def test_tenant_users(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/1/users", auth=auth_headers)

    def test_tenant_add_user(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/tenant/1/users", auth=auth_headers,
            json={"user_id": 2},
        )

    def test_tenant_remove_user(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/platform/tenant/1/users/2", auth=auth_headers)

    def test_tenant_invoice_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/invoice/list", auth=auth_headers)

    def test_tenant_invoice_download(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/invoice/1/download", auth=auth_headers)

    def test_tenant_license_download(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/invoice/1/license/download", auth=auth_headers)


class TestPackage:
    """套餐管理接口。"""

    def test_package_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/package/list", auth=auth_headers)

    def test_package_detail(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/package/detail/1", auth=auth_headers)

    def test_package_create(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/package/create", auth=auth_headers,
            json={"name": "测试套餐", "code": "test_pkg", "price": 99.0, "sort": 1},
        )

    def test_package_update(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PUT", "/platform/package/update/1", auth=auth_headers,
            json={"name": "更新套餐"},
        )

    def test_package_delete(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/platform/package/delete", auth=auth_headers, json=[9999])

    def test_package_menus(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/package/menus/1", auth=auth_headers)

    def test_package_set_menus(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/package/menus/1/set", auth=auth_headers,
            json={"menu_ids": [1, 2]},
        )

    def test_package_plugins(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/package/plugins/1", auth=auth_headers)

    def test_package_set_plugins(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/package/plugins/1/set", auth=auth_headers,
            json={"plugin_ids": [1]},
        )

    def test_package_status_batch(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PATCH", "/platform/package/status/batch", auth=auth_headers,
            json={"ids": [1], "status": 1},
        )


class TestPlugin:
    """插件管理接口。"""

    def test_plugin_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/plugin/list", auth=auth_headers)

    def test_plugin_detail(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/plugin/detail/1", auth=auth_headers)

    def test_plugin_create(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/plugin/create", auth=auth_headers,
            json={"name": "测试插件", "code": "test_plugin"},
        )

    def test_plugin_update(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PUT", "/platform/plugin/update/1", auth=auth_headers,
            json={"name": "更新插件"},
        )

    def test_plugin_delete(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/platform/plugin/delete", auth=auth_headers, json=[9999])

    def test_plugin_marketplace(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/plugin/marketplace", auth=auth_headers)

    def test_plugin_my(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/plugin/my", auth=auth_headers)

    def test_plugin_install(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/plugin/install", auth=auth_headers,
            json={"code": "test_plugin"},
        )

    def test_plugin_uninstall(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/plugin/uninstall", auth=auth_headers,
            json={"code": "test_plugin"},
        )

    def test_plugin_toggle(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/plugin/toggle", auth=auth_headers,
            json={"code": "test_plugin"},
        )

    def test_plugin_reload(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "POST", "/platform/plugin/reload", auth=auth_headers)


class TestMenu:
    """菜单管理接口。"""

    def test_menu_tree(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/menu/tree", auth=auth_headers)

    def test_menu_create(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/menu/create", auth=auth_headers,
            json={"name": "测试菜单", "type": 0, "parent_id": 0, "sort": 1},
        )

    def test_menu_update(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PUT", "/platform/menu/update/1", auth=auth_headers,
            json={"name": "更新菜单"},
        )

    def test_menu_delete(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/platform/menu/delete", auth=auth_headers, json=[9999])

    def test_menu_detail(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/menu/detail/1", auth=auth_headers)

    def test_menu_status_batch(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PATCH", "/platform/menu/status/batch", auth=auth_headers,
            json={"ids": [1], "status": 1},
        )


class TestEmail:
    """邮件服务接口。"""

    def test_email_config_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/email/config/list", auth=auth_headers)

    def test_email_config_create(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/email/config/create", auth=auth_headers,
            json={"name": "测试配置", "host": "smtp.test.com", "port": 587, "username": "test", "password": "pwd"},
        )

    def test_email_config_update(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PUT", "/platform/email/config/update/1", auth=auth_headers,
            json={"host": "smtp.new.com"},
        )

    def test_email_config_delete(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/platform/email/config/delete", auth=auth_headers, json=[9999])

    def test_email_config_detail(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/email/config/detail/1", auth=auth_headers)

    def test_email_config_test(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/email/config/test", auth=auth_headers,
            json={"host": "smtp.test.com", "port": 587, "username": "t", "password": "p"},
        )

    def test_email_send(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/email/send", auth=auth_headers,
            json={"to": "test@test.com", "subject": "test", "body": "hello"},
        )

    def test_email_template_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/email/template/list", auth=auth_headers)

    def test_email_template_detail(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/email/template/detail/1", auth=auth_headers)

    def test_email_template_create(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/email/template/create", auth=auth_headers,
            json={"name": "测试模板", "code": "test_tpl", "subject": "标题", "content": "内容"},
        )

    def test_email_template_update(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "PUT", "/platform/email/template/update/1", auth=auth_headers,
            json={"name": "更新模板"},
        )

    def test_email_template_delete(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/platform/email/template/delete", auth=auth_headers, json=[9999])

    def test_email_log_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/email/log/list", auth=auth_headers)


class TestOrder:
    """订单管理接口。"""

    def test_order_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/order/list", auth=auth_headers)

    def test_order_detail(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/order/detail/1", auth=auth_headers)

    def test_order_create(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/order/create", auth=auth_headers,
            json={"package_id": 1},
        )

    def test_order_cancel(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "POST", "/platform/order/cancel/1", auth=auth_headers)

    def test_order_refund_apply(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/order/refund/apply/1", auth=auth_headers,
            json={"reason": "测试退款"},
        )


class TestPayment:
    """支付管理接口。"""

    def test_payment_record_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/payment/record/list", auth=auth_headers)

    def test_payment_pay(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/payment/pay/1", auth=auth_headers,
            json={"method": "wechat"},
        )

    def test_payment_status(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/payment/status/1", auth=auth_headers)

    def test_payment_callback(self, test_client: TestClient) -> None:
        assert_route(test_client, "POST", "/platform/payment/callback/wechat")

    def test_payment_mock_callback(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "POST", "/platform/payment/mock/callback", auth=auth_headers)


class TestRefund:
    """退款管理接口。"""

    def test_refund_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/refund/list", auth=auth_headers)

    def test_refund_approve(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "PUT", "/platform/refund/approve/1", auth=auth_headers)

    def test_refund_reject(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "PUT", "/platform/refund/reject/1", auth=auth_headers)


class TestInvoice:
    """发票管理接口。"""

    def test_invoice_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/invoice/list", auth=auth_headers)

    def test_invoice_apply(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/tenant/invoice/apply", auth=auth_headers,
            json={"order_id": 1, "invoice_type": 0, "title": "测试发票", "tax_no": "123456"},
        )

    def test_invoice_issue(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "PUT", "/platform/invoice/issue/1", auth=auth_headers, json={"status": 1})

    def test_invoice_void(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "PUT", "/platform/invoice/void/1", auth=auth_headers, json={"status": 2})


class TestSelfService:
    """租户自助服务接口。"""

    def test_package_available(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/package/available", auth=auth_headers)

    def test_package_preview(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/package/preview", auth=auth_headers)

    def test_plugin_purchase(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/tenant/plugin/purchase", auth=auth_headers,
            json={"plugin_code": "test_plugin"},
        )

    def test_self_order_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/order/list", auth=auth_headers)

    def test_self_order_detail(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/order/detail/1", auth=auth_headers)

    def test_self_order_create(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/platform/tenant/order/create", auth=auth_headers,
            json={"package_id": 1},
        )

    def test_self_workspace(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/platform/tenant/workspace", auth=auth_headers)
