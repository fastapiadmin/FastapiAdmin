"""
模块接口测试 —— module_monitor（系统监控）
认证数据测试：admin 登录后验证监控接口数据。
"""

from conftest import assert_route  # noqa: F401
from fastapi.testclient import TestClient


class TestCache:
    """缓存监控接口。"""

    def test_cache_info(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/monitor/cache/info", auth=auth_headers)

    def test_cache_names(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/monitor/cache/get/names", auth=auth_headers)

    def test_cache_keys(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/monitor/cache/get/keys/test", auth=auth_headers)

    def test_cache_value(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/monitor/cache/get/value/test/key", auth=auth_headers)

    def test_cache_delete_name(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/monitor/cache/delete/name/test", auth=auth_headers)

    def test_cache_delete_key(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/monitor/cache/delete/key/test", auth=auth_headers)

    def test_cache_clear_all(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/monitor/cache/delete/all", auth=auth_headers)


class TestServer:
    """服务器监控接口。"""

    def test_server_info(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/monitor/server/info", auth=auth_headers)


class TestOnline:
    """在线用户监控接口。"""

    def test_online_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/monitor/online/list", auth=auth_headers)

    def test_online_delete(self, test_client: TestClient, auth_headers: dict) -> None:
        import json

        assert_route(
            test_client,
            "DELETE",
            "/monitor/online/delete",
            auth=auth_headers,
            content=json.dumps("test-session"),
            headers={"Content-Type": "application/json"},
        )

    def test_online_clear(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "DELETE", "/monitor/online/clear", auth=auth_headers)


class TestResource:
    """资源管理接口。"""

    def test_resource_list(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "GET", "/monitor/resource/list", auth=auth_headers)

    def test_resource_delete(self, test_client: TestClient, auth_headers: dict) -> None:
        import json

        assert_route(
            test_client,
            "DELETE",
            "/monitor/resource/delete",
            auth=auth_headers,
            content=json.dumps(["/nonexistent"]),
            headers={"Content-Type": "application/json"},
        )

    def test_resource_create_dir(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/monitor/resource/create-dir", auth=auth_headers,
            json={"name": "test_dir", "parent_path": "/"},
        )

    def test_resource_rename(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/monitor/resource/rename", auth=auth_headers,
            json={"old_path": "/old.txt", "new_path": "/new.txt"},
        )

    def test_resource_copy(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/monitor/resource/copy", auth=auth_headers,
            json={"source_path": "/src.txt", "target_path": "/dst.txt"},
        )

    def test_resource_move(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(
            test_client, "POST", "/monitor/resource/move", auth=auth_headers,
            json={"source_path": "/src.txt", "target_path": "/dst.txt"},
        )

    def test_resource_upload(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "POST", "/monitor/resource/upload", auth=auth_headers)

    def test_resource_export(self, test_client: TestClient, auth_headers: dict) -> None:
        assert_route(test_client, "POST", "/monitor/resource/export", auth=auth_headers)
