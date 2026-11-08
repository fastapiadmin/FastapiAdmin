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


async def test_chat_non_stream(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.ai.chat.service as mod
    async def ensure(crud, sid): return "s1"
    monkeypatch.setattr(mod, "_ensure_session", ensure)
    class Crud:
        def __init__(self, *a): self.db = object()
    monkeypatch.setattr(mod, "ChatSessionCRUD", Crud)
    class Agent:
        async def arun(self, input): return SimpleNamespace(content="请跳转到用户管理")
    class Factory:
        def create_agent(self, **kw): return Agent()
    monkeypatch.setattr(mod, "AgnoFactory", Factory)
    svc = ChatService.__new__(ChatService); svc.auth = SimpleNamespace(user=SimpleNamespace(username="u")); svc.redis = None
    out = await svc.chat_non_stream("hi", None)
    assert out["session_id"] == "s1" and out["action"]["path"] == "/system/user"


async def test_chat_session_service_success(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.ai.chat.service as mod
    from app.modules.ai.chat.schema import ChatSessionCreateSchema, ChatSessionQueryParam, ChatSessionUpdateSchema
    monkeypatch.setattr(mod, "_format_session_data", lambda s, **kw: {"session_id": "s"})
    class C:
        def __init__(self,*a): self.renamed=False
        async def get_by_id(self,**kw): return {"x":1}
        async def list_page(self,**kw): return ([{}], 2)
        async def create(self,**kw): return {}
        async def rename(self,**kw): self.renamed=True
        async def delete(self,**kw): self.deleted=True
    monkeypatch.setattr(mod, "ChatSessionCRUD", C)
    s=ChatService.__new__(ChatService); s.auth=object(); s.redis=None
    assert (await s.get_session("s")).session_id == "s"
    assert (await s.create(ChatSessionCreateSchema(title="t"))).session_id == "s"
    page=await s.page(1,10,ChatSessionQueryParam())
    assert page.total == 2
    await s.update("s", ChatSessionUpdateSchema(title="n"))
    await s.delete(["s"])


async def test_chat_non_stream_error(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.ai.chat.service as mod
    async def ensure(crud,sid): return "s"
    monkeypatch.setattr(mod,"_ensure_session",ensure)
    class Crud:
        def __init__(self,*a): self.db=object()
    monkeypatch.setattr(mod,"ChatSessionCRUD",Crud)
    class Agent:
        async def arun(self,input): raise RuntimeError()
    class F:
        def create_agent(self,**kw): return Agent()
    monkeypatch.setattr(mod,"AgnoFactory",F)
    s=ChatService.__new__(ChatService); s.auth=SimpleNamespace(user=SimpleNamespace(username="u")); s.redis=None
    out=await s.chat_non_stream("x",None)
    assert out["action"] is None and "暂时不可用" in out["response"]


def test_extract_action_branches() -> None:
    assert ChatService._extract_action('{"type":"x"}') == {"type":"x"}
    assert ChatService._extract_action('```json\n{"type":"y"}\n```') == {"type":"y"}
    assert ChatService._extract_action('```json{bad}```') is None
    assert ChatService._extract_action("请打开用户管理页面") == {"type":"navigate","path":"/system/user","name":"用户管理"}
    assert ChatService._extract_action("打开未知页面") is None


async def test_chat_non_stream_success(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.ai.chat.service as mod
    async def ensure(crud,sid): return "s"
    monkeypatch.setattr(mod,"_ensure_session",ensure)
    class Crud:
        def __init__(self,*a): self.db=object()
    monkeypatch.setattr(mod,"ChatSessionCRUD",Crud)
    class Agent:
        async def arun(self,input): return SimpleNamespace(content="hi")
    class F:
        def create_agent(self,**kw): return Agent()
    monkeypatch.setattr(mod,"AgnoFactory",F)
    s=ChatService.__new__(ChatService); s.auth=SimpleNamespace(user=SimpleNamespace(username="u")); s.redis=None
    out=await s.chat_non_stream("x",None)
    assert out["response"]=="hi" and out["session_id"]=="s"


async def _collect(gen):
    out=[]
    async for x in gen: out.append(x)
    return out


async def test_chat_query_stream_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    import asyncio
    import app.modules.ai.chat.service as mod
    from app.modules.ai.chat.schema import ChatQuerySchema
    async def ensure(crud,sid): return "s"
    monkeypatch.setattr(mod,"_ensure_session",ensure)
    class Crud:
        def __init__(self,*a): self.db=object()
    monkeypatch.setattr(mod,"ChatSessionCRUD",Crud)
    class Agent:
        def __init__(self,stream): self.stream=stream
        def arun(self,**kw): return self.stream
    class F:
        def __init__(self,stream): self.stream=stream
        def create_agent(self,**kw): return Agent(self.stream)
    def svc(stream):
        s=ChatService.__new__(ChatService); s.auth=SimpleNamespace(user=SimpleNamespace(username="u")); s.redis=None
        monkeypatch.setattr(mod,"AgnoFactory",lambda:F(stream))
        return s
    assert await _collect(svc(None).chat_query(ChatQuerySchema(message=" "))) == ["请输入消息内容"]
    async def chunks():
        for c in ("a","b"):
            yield SimpleNamespace(content=c)
    assert await _collect(svc(chunks()).chat_query(ChatQuerySchema(message="hi"))) == ["a","b"]
    assert await _collect(svc(SimpleNamespace(content="z")).chat_query(ChatQuerySchema(message="hi"))) == ["z"]
    async def bad():
        raise RuntimeError()
        yield
    out=await _collect(svc(bad()).chat_query(ChatQuerySchema(message="hi")))
    assert "暂时不可用" in out[0]
    async def cancelled():
        raise asyncio.CancelledError()
        yield
    with pytest.raises(asyncio.CancelledError):
        await _collect(svc(cancelled()).chat_query(ChatQuerySchema(message="hi")))
