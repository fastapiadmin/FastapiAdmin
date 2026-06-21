"""
模块接口测试 —— module_common（公共模块）
每个接口一个测试用例，验证路由存在且返回码正确。
"""

from conftest import assert_route
from fastapi.testclient import TestClient


class TestHealth:
    """健康检查接口。"""

    def test_health_check(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/common/health", expected_status=200)

    def test_health_ready(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/common/health/ready", expected_status=200)

    def test_health_live(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/common/health/live", expected_status=200)


class TestFile:
    """文件管理接口。"""

    def test_upload_file(self, test_client: TestClient) -> None:
        assert_route(test_client, "POST", "/common/file/upload")

    def test_download_file(self, test_client: TestClient) -> None:
        assert_route(
            test_client,
            "POST",
            "/common/file/download",
            json={"file_path": "test.txt", "delete": False},
        )
