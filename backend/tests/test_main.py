"""
测试文件

注意：使用普通的 def 定义测试函数，不要使用 async def
执行命令: pytest tests/test.py
"""

import pytest
from fastapi.testclient import TestClient


def test_check_health(test_client: TestClient) -> None:
    """测试健康检查接口"""
    response = test_client.get("/common/health")
    assert response.status_code == 200
    assert response.json() == {"msg": "Healthy"}


# 运行所有测试
if __name__ == "__main__":
    pytest.main(["-v", "tests/test_main.py"])
