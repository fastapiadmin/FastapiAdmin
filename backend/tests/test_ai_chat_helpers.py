"""AI 会话动作解析与模型配置服务分支。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.ai.chat.service import AiModelConfigService, ChatService


def test_extract_json_and_navigation_action() -> None:
    assert ChatService._extract_action('{"type":"navigate","path":"/x"}') == {"type": "navigate", "path": "/x"}
    assert ChatService._extract_action('```json\n{"a":1}\n```') == {"a": 1}
    assert ChatService._extract_action("请跳转到用户管理") == {"type": "navigate", "path": "/system/user", "name": "用户管理"}
    assert ChatService._extract_action("请打开菜单管理") == {"type": "navigate", "path": "/system/menu", "name": "菜单管理"}
    assert ChatService._extract_action("普通回答") is None


def test_chat_tools_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = ChatService.__new__(ChatService)
    svc.auth = object(); svc.redis = None
    assert svc._chat_tools(False) == []
    import app.modules.ai.tools.registry as reg
    class Spec:
        def __init__(self, func): self.func = func
    monkeypatch.setattr(reg, "build_readonly_tools", lambda auth, redis: [Spec("fn")])
    assert svc._chat_tools(True) == ["fn"]


async def test_model_config_service(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.ai.chat.service as mod
    svc = AiModelConfigService(SimpleNamespace(user=SimpleNamespace(id=1)), object())
    assert svc._user_id == 1
    async def list_cfg(redis, uid): return [{"id": "a"}]
    async def active_id(redis, uid): return "a"
    async def get_cfg(redis, uid): return {"id": "a"}
    async def create_cfg(redis, uid, cfg): return {"id": "new"}
    async def update_cfg(redis, uid, cid, cfg): return {"id": cid} if cid == "a" else None
    async def delete_cfg(redis, uid, cid): return cid == "a"
    async def set_active(redis, uid, cid): return cid == "a"
    for name, fn in [("list_user_model_configs", list_cfg), ("get_active_model_id", active_id), ("get_user_model_config", get_cfg), ("create_user_model_config", create_cfg), ("update_user_model_config", update_cfg), ("delete_user_model_config", delete_cfg), ("set_active_model_config", set_active)]:
        monkeypatch.setattr(mod, name, fn)
    assert (await svc.list_configs())["active_id"] == "a"
    assert (await svc.get_active())["id"] == "a"
    cfg = SimpleNamespace()
    assert (await svc.create(cfg))["id"] == "new"
    assert (await svc.update("a", cfg))["id"] == "a"
    with pytest.raises(CustomException):
        await svc.update("missing", cfg)
    with pytest.raises(CustomException):
        await svc.delete("missing")
    with pytest.raises(CustomException):
        await svc.set_active("missing")


async def test_chat_session_service_missing_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    class CRUD:
        def __init__(self, *a): pass
        async def get_by_id(self, **kw): return None
        async def rename(self, **kw): return None
        async def delete(self, **kw): return None
    import app.modules.ai.chat.service as mod
    monkeypatch.setattr(mod, "ChatSessionCRUD", CRUD)
    svc = ChatService.__new__(ChatService); svc.auth = object(); svc.redis = None
    with pytest.raises(CustomException, match="会话不存在"):
        await svc.get_session("s")
    with pytest.raises(CustomException, match="会话不存在"):
        await svc.update("s", __import__("app.modules.ai.chat.schema", fromlist=["ChatSessionUpdateSchema"]).ChatSessionUpdateSchema(title="n"))
    with pytest.raises(CustomException, match="不能为空"):
        await svc.delete([])
    with pytest.raises(CustomException, match="会话不存在"):
        await svc.delete(["s"])
