"""真实 PostgreSQL 下 AI 会话/模型配置 HTTP 接口集成。"""

from __future__ import annotations

import os
import uuid

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


def _title() -> str:
    return f"it_api_{uuid.uuid4().hex[:8]}"


def test_ai_session_api(test_client, auth_headers) -> None:
    title = _title()
    resp = test_client.post("/api/v1/ai/chat/create", json={"title": title}, headers=auth_headers)
    assert resp.status_code == 200, resp.text
    sid = resp.json()["data"]["session_id"]
    try:
        detail = test_client.get(f"/api/v1/ai/chat/detail/{sid}", headers=auth_headers)
        assert detail.status_code == 200 and detail.json()["data"]["session_id"] == sid
        listing = test_client.get("/api/v1/ai/chat/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers)
        assert listing.status_code == 200 and listing.json()["data"]["total"] >= 1
        updated = test_client.put(f"/api/v1/ai/chat/update/{sid}", json={"title": title + "_x"}, headers=auth_headers)
        assert updated.status_code == 200
    finally:
        deleted = test_client.request("DELETE", "/api/v1/ai/chat/delete", json=[sid], headers=auth_headers)
        assert deleted.status_code == 200


def test_ai_session_missing(test_client, auth_headers) -> None:
    assert test_client.get("/api/v1/ai/chat/detail/missing-session", headers=auth_headers).status_code == 404


def test_ai_model_config_api(test_client, auth_headers) -> None:
    payload = {"name": _title(), "model_id": "m", "base_url": "https://api.example.com/v1", "api_key": "secret"}
    created = test_client.post("/api/v1/ai/chat/model", json=payload, headers=auth_headers)
    assert created.status_code == 200, created.text
    cfg = created.json()["data"]
    # conftest 的 mock Redis 锁语义不完整，清理残留锁键，避免影响后续接口
    import conftest
    for key in list(conftest._mock_redis_store):
        if ":lock:" in (key.decode() if isinstance(key, bytes) else key):
            del conftest._mock_redis_store[key]
    try:
        listing = test_client.get("/api/v1/ai/chat/model", headers=auth_headers)
        assert listing.status_code == 200 and any(x["id"] == cfg["id"] for x in listing.json()["data"]["items"])
        activated = test_client.post(f"/api/v1/ai/chat/model/{cfg['id']}/activate", headers=auth_headers)
        assert activated.status_code == 200
        updated = test_client.put(f"/api/v1/ai/chat/model/{cfg['id']}", json={**payload, "name": "it2"}, headers=auth_headers)
        assert updated.status_code == 200
    finally:
        for key in list(conftest._mock_redis_store):
            if ":lock:" in (key.decode() if isinstance(key, bytes) else key):
                del conftest._mock_redis_store[key]
        deleted = test_client.delete(f"/api/v1/ai/chat/model/{cfg['id']}", headers=auth_headers)
        assert deleted.status_code == 200


def test_ai_tools_api(test_client, auth_headers) -> None:
    resp = test_client.get("/api/v1/ai/chat/tools", headers=auth_headers)
    assert resp.status_code == 200
    names = {item["name"] for item in resp.json()["data"]}
    assert {"server_status", "storage_sources", "redis_keys"} <= names


def test_ai_model_probe_api(test_client, auth_headers, monkeypatch: pytest.MonkeyPatch) -> None:
    async def models(base_url, api_key): return [{"id": "m1", "owned_by": "x"}]
    async def probe(base_url, api_key, model_id): return {"ok": True, "model_id": model_id, "latency_ms": 1}
    import app.modules.ai.chat.controller as c
    monkeypatch.setattr(c, "probe_available_models", models)
    monkeypatch.setattr(c, "probe_model_connection", probe)
    a = test_client.post("/api/v1/ai/chat/model/available", json={"base_url": "https://x/v1", "api_key": "k"}, headers=auth_headers)
    assert a.status_code == 200 and a.json()["data"][0]["id"] == "m1"
    b = test_client.post("/api/v1/ai/chat/model/test", json={"base_url": "https://x/v1", "api_key": "k", "model_id": "m1"}, headers=auth_headers)
    assert b.status_code == 200 and b.json()["data"]["ok"] is True


def test_ai_chat_permission_helper() -> None:
    from types import SimpleNamespace
    from app.modules.ai.chat.controller import _has_chat_permission
    superuser = SimpleNamespace(user=SimpleNamespace(id=1, is_superuser=True), permissions=[])
    normal = SimpleNamespace(user=SimpleNamespace(id=2, is_superuser=False), permissions=["module_ai:chat:query"])
    denied = SimpleNamespace(user=SimpleNamespace(id=3, is_superuser=False), permissions=[])
    assert _has_chat_permission(superuser) is True
    assert _has_chat_permission(normal) is True
    assert _has_chat_permission(denied) is False


def test_ai_chat_endpoint(test_client, auth_headers, monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.ai.chat.controller as c
    async def cfg(redis, uid): return {"model_id": "m"}
    async def chat(self, **kw): return {"response": "pong", "session_id": "s", "function_calls": None, "action": None}
    monkeypatch.setattr(c, "get_user_model_config", cfg)
    monkeypatch.setattr(c.ChatService, "chat_non_stream", chat)
    resp = test_client.post("/api/v1/ai/chat/ai-chat", json={"message": "ping"}, headers=auth_headers)
    assert resp.status_code == 200, resp.text
    assert resp.json()["data"]["response"] == "pong"
