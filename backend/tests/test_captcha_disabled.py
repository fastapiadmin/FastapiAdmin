"""验证码关闭时 /captcha/get 的行为 —— 返回 enable=false 而不是报错。"""

from fastapi.testclient import TestClient


def test_get_captcha_when_disabled_returns_enable_false(test_client: TestClient) -> None:
    response = test_client.get("/system/auth/captcha/get")

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["enable"] is False
    assert data["key"] == ""
