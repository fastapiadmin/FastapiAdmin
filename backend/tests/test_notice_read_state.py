"""公告已读状态：未读数、按条标记、全部标记、按用户隔离。

口径：公告状态 0 = 启用（对外可见）、1 = 停用；未读数只统计启用公告，
已读按用户存储，重复标记幂等。

断言一律用**增量**而不是绝对值：测试库可能承接多次运行的数据（PostgreSQL 不像 sqlite
每次都重建），`/notice/available` 也固定最多返回 10 条。
"""

import uuid

from fastapi.testclient import TestClient


def _create_notice(client: TestClient, headers: dict, title: str, status: int = 0) -> int:
    unique_title = f"{title}-{uuid.uuid4().hex[:8]}"
    resp = client.post(
        "/system/notice/create",
        json={"notice_title": unique_title, "notice_type": "1", "notice_content": f"{unique_title} 正文", "status": status},
        headers=headers,
    )
    assert resp.json()["success"] is True, resp.text
    return resp.json()["data"]["id"]


def _login(client: TestClient, username: str = "user", password: str = "123456") -> dict:
    resp = client.post("/system/auth/login", data={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    return {"Authorization": f"Bearer {resp.json()['data']['access_token']}"}


def _unread(client: TestClient, headers: dict) -> int:
    resp = client.get("/system/notice/unread-count", headers=headers)
    assert resp.json()["success"] is True, resp.text
    return resp.json()["data"]["unread"]


class TestNoticeReadState:
    def test_unread_count_and_mark_read(self, test_client: TestClient, auth_headers: dict) -> None:
        user_h = _login(test_client)
        before = _unread(test_client, user_h)

        first = _create_notice(test_client, auth_headers, "已读测试-A")
        _create_notice(test_client, auth_headers, "已读测试-B")
        # 停用的不计入未读
        _create_notice(test_client, auth_headers, "已读测试-停用", status=1)
        assert _unread(test_client, user_h) == before + 2

        # 按条标记：未读 -1，已读 ID 里能看到它
        resp = test_client.post("/system/notice/read", json={"notice_ids": [first]}, headers=user_h)
        assert resp.json()["data"]["unread"] == before + 1
        assert first in test_client.get("/system/notice/read-ids", headers=user_h).json()["data"]

        # 重复标记幂等
        again = test_client.post("/system/notice/read", json={"notice_ids": [first]}, headers=user_h)
        assert again.json()["data"]["unread"] == before + 1

        # 全部标记 → 0
        assert test_client.post("/system/notice/read", json={}, headers=user_h).json()["data"]["unread"] == 0

    def test_read_state_is_per_user(self, test_client: TestClient, auth_headers: dict) -> None:
        """已读按用户隔离：我标记不影响别人的未读数。"""
        user_a = _login(test_client)
        other = _login(test_client, "admin", "admin123")
        notice_id = _create_notice(test_client, auth_headers, "已读测试-隔离")

        other_before = _unread(test_client, other)
        test_client.post("/system/notice/read", json={"notice_ids": [notice_id]}, headers=user_a)
        assert _unread(test_client, other) == other_before

    def test_mark_read_requires_login(self, test_client: TestClient) -> None:
        assert test_client.get("/system/notice/unread-count").status_code == 401
        assert test_client.post("/system/notice/read", json={}).status_code == 401
