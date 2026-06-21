"""
模块接口测试 —— module_generator（代码生成模块）

动态路由映射：module_generator → /generator
每个接口一个测试用例，覆盖查询 / 新增 / 修改 / 删除 等操作。
"""

from conftest import assert_route
from fastapi.testclient import TestClient


class TestGenerator:
    """代码生成模块接口。"""

    def test_gencode_list(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/generator/gencode/list")

    def test_gencode_db_list(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/generator/gencode/db/list")

    def test_gencode_import(self, test_client: TestClient) -> None:
        assert_route(
            test_client,
            "POST",
            "/generator/gencode/import",
            json=["test_table"],
        )

    def test_gencode_detail(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/generator/gencode/detail/1")

    def test_gencode_create(self, test_client: TestClient) -> None:
        assert_route(
            test_client,
            "POST",
            "/generator/gencode/create",
            json={"sql": "CREATE TABLE test (id INTEGER PRIMARY KEY)"},
        )

    def test_gencode_update(self, test_client: TestClient) -> None:
        assert_route(
            test_client,
            "PUT",
            "/generator/gencode/update/1",
            json={"table_name": "updated_table"},
        )

    def test_gencode_delete(self, test_client: TestClient) -> None:
        assert_route(test_client, "DELETE", "/generator/gencode/delete", json=[9999])

    def test_gencode_preview(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/generator/gencode/preview/1")

    def test_gencode_output(self, test_client: TestClient) -> None:
        assert_route(test_client, "POST", "/generator/gencode/output/test_table")

    def test_gencode_sync_db(self, test_client: TestClient) -> None:
        assert_route(test_client, "POST", "/generator/gencode/sync_db/test_table")

    def test_gencode_sync_db_preview(self, test_client: TestClient) -> None:
        assert_route(test_client, "GET", "/generator/gencode/sync_db/preview/test_table")

    def test_gencode_batch_output(self, test_client: TestClient) -> None:
        assert_route(
            test_client,
            "PATCH",
            "/generator/gencode/batch/output",
            json={"table_ids": [1]},
        )
