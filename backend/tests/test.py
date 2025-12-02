"""
注意测试函数是普通的 def，不是 async def。

还有client的调用也是普通的调用，不是用 await。

这让你可以直接使用 pytest 而不会遇到麻烦。
"""

from fastapi.testclient import TestClient

from main import create_app

app = create_app()


client = TestClient(app)


def test_check_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Healthy"}
