import os
import sys

import pytest
from fastapi.testclient import TestClient

# 导入 main 模块，确保路径正确
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import create_app

# 创建测试客户端
app = create_app()


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client
