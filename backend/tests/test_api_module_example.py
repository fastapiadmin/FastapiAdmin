"""
模块接口测试 —— module_example（示例模块）

动态路由映射：module_example → /example
每个接口一个测试用例，覆盖查询 / 新增 / 修改 / 删除 等操作。
"""

from conftest import assert_route
from fastapi.testclient import TestClient


class TestExampleDemo:
    """示例模块接口。"""

    def test_demo_detail(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/example/demo/detail/1")

    def test_demo_list(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/example/demo/list")

    def test_demo_create(self, test_client: TestClient) -> None:
        assert_route(
            test_client,
            "POST",
            "/example/demo/create",
            json={"name": "测试示例", "status": 0},
        )

    def test_demo_update(self, test_client: TestClient) -> None:
        assert_route(
            test_client,
            "PUT",
            "/example/demo/update/1",
            json={"name": "更新示例"},
        )

    def test_demo_delete(self, test_client: TestClient) -> None:
        assert_route(test_client, "DELETE", "/example/demo/delete", json=[9999])

    def test_demo_export(self, test_client: TestClient) -> None:
        assert_route(test_client, "POST", "/example/demo/export")

    def test_demo_import(self, test_client: TestClient) -> None:
        assert_route(test_client, "POST", "/example/demo/import")

    def test_demo_download_template(self, test_client: TestClient) -> None:
        assert_route(test_client, "POST", "/example/demo/download/template")

    def test_demo_status_batch(self, test_client: TestClient) -> None:
        assert_route(
            test_client,
            "PATCH",
            "/example/demo/status/batch",
            json={"ids": [1], "status": 1},
        )
