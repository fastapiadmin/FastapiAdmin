import os
import sys

# 必须在首次 import app 之前设置，以便 Settings / database 引擎使用 SQLite 与内存 Redis
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, _ROOT)

os.environ.setdefault("ENVIRONMENT", "dev")
os.environ["TESTING"] = "1"
os.environ["DATABASE_TYPE"] = "sqlite"
os.environ["DATABASE_NAME"] = os.path.join(_ROOT, "pytest_fastapiadmin")

import pytest
from fastapi.testclient import TestClient

from main import create_app

# 创建测试客户端（依赖上述环境变量）
app = create_app()


@pytest.fixture(scope="session")
def test_client():
    """
    会话级 HTTP 测试客户端（与 ``conftest`` 中单例 ``app`` 对齐，只启动一次生命周期）。

    若使用 ``module`` 作用域，多个测试文件各开一个 ``TestClient`` 会重复驱动同一
    ``app`` 的 lifespan，易导致第二次 ``__enter__`` 时出现 ``CancelledError``。

    返回:
    - TestClient: 供用例发起的同步测试客户端（yield 注入）。
    """
    with TestClient(app) as client:
        yield client
