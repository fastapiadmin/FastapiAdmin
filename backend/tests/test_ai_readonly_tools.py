"""AI 只读工具回归测试。

固化：
1. 工具清单只含「查询类」且签名里**没有**闭包参数（auth/redis 不能变成模型要填的参数）；
2. 工具内部出错返回 ``{"error": ...}`` 而不是抛异常；
3. 工厂确实把工具注入 Agent；ChatService 的开关关闭时零行为变化。
"""

import inspect
import json
from types import SimpleNamespace
from typing import Any

import httpx
import pytest
from agno.models.openai.like import OpenAILike
from openai import AsyncOpenAI
from starlette.websockets import WebSocket

from app.core.exceptions import CustomException
from app.modules.ai import tools as ai_tools_pkg
from app.modules.ai.chat import controller as chat_controller
from app.modules.ai.chat import service as chat_service_module
from app.modules.ai.chat.service import ChatService
from app.modules.ai.tools import registry as registry_module
from app.modules.ai.tools.registry import build_readonly_tools


class _FakeRedis:
    def __init__(self, keys: list[str] | None = None) -> None:
        self.keys = keys or []
        self.connection_pool = SimpleNamespace(connection_kwargs={"db": 0})

    async def scan(self, cursor: int = 0, match: str = "*", count: int = 100) -> tuple[int, list[str]]:
        return 0, self.keys

    def pipeline(self, transaction: bool = False) -> Any:
        key_count = len(self.keys)

        class _Pipe:
            async def __aenter__(self) -> "_Pipe":
                return self

            async def __aexit__(self, *args: Any) -> bool:
                return False

            def type(self, key: str) -> None:
                return None

            def ttl(self, key: str) -> None:
                return None

            async def execute(self) -> list[Any]:
                return ["string", -1] * key_count

        return _Pipe()

    async def aclose(self) -> None:
        return None


def test_tool_list_is_readonly_and_has_no_injected_params() -> None:
    tools = build_readonly_tools(None, None)  # type: ignore[arg-type]
    assert [tool.name for tool in tools] == [
        "server_status",
        "storage_sources",
        "storage_files",
        "cron_jobs",
        "redis_keys",
    ]
    forbidden = {"auth", "self", "cls", "redis", "db"}
    for tool in tools:
        assert tool.description.strip()
        params = set(inspect.signature(tool.func).parameters)
        assert not (params & forbidden), f"{tool.name} 的签名泄露了闭包参数: {params & forbidden}"


async def test_redis_keys_returns_names_only() -> None:
    tools = {tool.name: tool for tool in build_readonly_tools(None, _FakeRedis(["a:1", "b:2"]))}  # type: ignore[arg-type]
    result = await tools["redis_keys"].func(pattern="a*", limit=10)
    assert result["keys"] == ["a:1", "b:2"]


async def test_redis_keys_without_redis_returns_error() -> None:
    tools = {tool.name: tool for tool in build_readonly_tools(None, None)}  # type: ignore[arg-type]
    result = await tools["redis_keys"].func()
    assert "error" in result


async def test_server_status_error_is_converted(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _boom() -> Any:
        raise RuntimeError("psutil broken")

    monkeypatch.setattr(registry_module.ServerService, "get_server_monitor_info", staticmethod(_boom))
    tools = {tool.name: tool for tool in build_readonly_tools(None, None)}  # type: ignore[arg-type]
    result = await tools["server_status"].func()
    assert "error" in result and "psutil broken" in result["error"]


async def test_storage_files_unknown_source_returns_available_names(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeCtx:
        async def __aenter__(self) -> object:
            return object()

        async def __aexit__(self, *args: Any) -> bool:
            return False

    class _FakeNodeService:
        def __init__(self, auth: Any, db: Any) -> None:
            pass

        async def get_list(self) -> list[SimpleNamespace]:
            return [SimpleNamespace(id=1, name="node-a", protocol="sftp", status=0, is_default=False)]

    monkeypatch.setattr(registry_module, "async_db_session", lambda: _FakeCtx())
    monkeypatch.setattr(registry_module, "StorageNodeService", _FakeNodeService)
    tools = {tool.name: tool for tool in build_readonly_tools(None, None)}  # type: ignore[arg-type]
    result = await tools["storage_files"].func(source_name="missing")
    assert "error" in result
    assert result["available"] == ["node-a"]


async def test_cron_jobs_returns_compact_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeResult:
        def scalars(self) -> "_FakeResult":
            return self

        def all(self) -> list[SimpleNamespace]:
            return [
                SimpleNamespace(job_name="sync", trigger_type="cron", next_run_time="2026-01-01 00:00", status=0),
            ]

    class _FakeSession:
        async def execute(self, stmt: Any) -> _FakeResult:
            return _FakeResult()

        async def __aenter__(self) -> "_FakeSession":
            return self

        async def __aexit__(self, *args: Any) -> bool:
            return False

    monkeypatch.setattr(registry_module, "async_db_session", lambda: _FakeSession())
    tools = {tool.name: tool for tool in build_readonly_tools(None, None)}  # type: ignore[arg-type]
    rows = await tools["cron_jobs"].func(limit=5)
    assert rows == [{"job_name": "sync", "trigger_type": "cron", "next_run_time": "2026-01-01 00:00", "status": 0}]


def test_agno_factory_injects_tools(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.utils import ai_factory as factory_module

    captured: dict[str, Any] = {}

    class _FakeAgent:
        def __init__(self, **kwargs: Any) -> None:
            captured["agent"] = kwargs

    class _FakeTeam:
        def __init__(self, **kwargs: Any) -> None:
            captured["team"] = kwargs

    class _FakeModel:
        def __init__(self, **kwargs: Any) -> None:
            captured["model"] = kwargs

    monkeypatch.setattr(factory_module, "Agent", _FakeAgent)
    monkeypatch.setattr(factory_module, "Team", _FakeTeam)
    monkeypatch.setattr(factory_module, "OpenAILike", _FakeModel)

    def _tool() -> str:
        return "ok"

    factory_module.AgnoFactory().create_agent("u1", "t1", "s1", tools=[_tool])
    assert captured["agent"]["tools"] == [_tool]


def test_chat_service_tools_switch_off_keeps_behavior() -> None:
    service = ChatService.__new__(ChatService)
    setattr(service, "auth", None)
    setattr(service, "redis", None)
    assert service._chat_tools(False) == []
    enabled = service._chat_tools(True)
    assert len(enabled) == 5
    assert all(callable(item) for item in enabled)


@pytest.mark.parametrize("use_tools", [True, False])
async def test_chat_delegation_uses_tool_context_only_when_enabled(
    monkeypatch: pytest.MonkeyPatch, use_tools: bool,
) -> None:
    contexts = []
    model_tools = []
    monitor_calls = 0

    async def fake_monitor() -> SimpleNamespace:
        nonlocal monitor_calls
        monitor_calls += 1
        return SimpleNamespace(
            cpu=SimpleNamespace(model_dump=lambda: {"cpu_num": 8}),
            mem=SimpleNamespace(model_dump=lambda: {"usage": 62.5}),
            disks=[SimpleNamespace(model_dump=lambda: {"dir_name": "/", "usage": 68.0})],
        )

    def model_response(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        messages = body["messages"]
        tools = {tool["function"]["name"] for tool in body.get("tools", [])}
        model_tools.append(tools)
        results = [message["content"] for message in messages if message["role"] == "tool"]
        delta: dict[str, Any] = {"role": "assistant"}
        extra_text = []
        tool = None
        if not use_tools:
            contexts.append(messages[0]["content"])
            delta["content"] = "当前对话未启用监控工具"
        elif "delegate_task_to_member" in tools and not results:
            contexts.append(messages[0]["content"])
            delta["content"] = "Team 将任务委派给成员"
            tool = ("delegate_task_to_member", {"member_id": "verify-user", "task": "调用 server_status"})
        elif "server_status" in tools and not results:
            delta["content"] = "Agent 正在查询"
            tool = ("server_status", {})
        elif "server_status" in tools:
            assert "62.5" in results[-1] and "68.0" in results[-1]
            delta["content"] = "Agent 已取得监控数据 62.5%"
        else:
            assert "62.5" in results[-1]
            delta["content"] = "内存 62.5%"
            extra_text = ["，磁盘 68%"]

        if tool:
            name, arguments = tool
            delta["tool_calls"] = [{
                "index": 0, "id": f"call_{name}", "type": "function",
                "function": {"name": name, "arguments": json.dumps(arguments)},
            }]
        chunk = {"id": "fixture", "object": "chat.completion.chunk", "created": 1, "model": "fixture"}
        events = [
            {**chunk, "choices": [{"index": 0, "delta": delta, "finish_reason": None}]},
            *[
                {**chunk, "choices": [{"index": 0, "delta": {"content": text}, "finish_reason": None}]}
                for text in extra_text
            ],
            {**chunk, "choices": [{"index": 0, "delta": {}, "finish_reason": "tool_calls" if tool else "stop"}]},
        ]
        data = "".join(f"data: {json.dumps(event)}\n\n" for event in events)
        return httpx.Response(200, headers={"Content-Type": "text/event-stream"}, text=data + "data: [DONE]\n\n")

    monkeypatch.setattr(registry_module.ServerService, "get_server_monitor_info", fake_monitor)
    monkeypatch.setattr(chat_service_module, "ChatSessionCRUD", lambda auth: SimpleNamespace(db=None))
    config = {"base_url": "https://model.invalid/v1", "api_key": "fixture", "model_id": "fixture"}
    auth = SimpleNamespace(user=SimpleNamespace(id=1, username="verify_user", is_superuser=True))

    async def authenticate(websocket: WebSocket) -> tuple[SimpleNamespace, None]:
        return auth, None

    async def get_model_config(redis: Any, user_id: int) -> dict[str, str]:
        return config

    monkeypatch.setattr(chat_controller, "websocket_authenticate", authenticate)
    monkeypatch.setattr(chat_controller, "get_user_model_config", get_model_config)
    query = {"message": "现在服务器的内存和磁盘使用率是多少？", "session_id": "fixture", "use_tools": use_tools}
    incoming = iter([
        {"type": "websocket.connect"},
        {"type": "websocket.receive", "text": json.dumps(query)},
        {"type": "websocket.disconnect", "code": 1000},
    ])
    frames = []

    async def receive() -> dict[str, Any]:
        return next(incoming)

    async def send(message: dict[str, Any]) -> None:
        if message["type"] == "websocket.send":
            frames.append(message["text"])

    websocket = WebSocket(
        {"type": "websocket", "app": SimpleNamespace(state=SimpleNamespace(redis=None)), "client": None},
        receive=receive,
        send=send,
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(model_response)) as http:
        client = AsyncOpenAI(base_url=config["base_url"], api_key=config["api_key"], http_client=http)
        monkeypatch.setattr(OpenAILike, "get_async_client", lambda self: client)
        await chat_controller.websocket_chat_controller(websocket)

    assert len(contexts) == 1
    if use_tools:
        assert 'member id="verify-user"' in contexts[0]
        assert "member_id" in contexts[0] and "verify-user" in contexts[0]
        assert "server_status" in contexts[0] and "查询服务器资源状态" in contexts[0]
        assert "redis_keys" in contexts[0] and "只返回键名" in contexts[0]
        assert monitor_calls == 1
        assert frames == ["内存 62.5%", "，磁盘 68%", "[DONE]"]
    else:
        assert model_tools == [{"get_chat_history"}]
        assert "server_status" not in contexts[0] and "redis_keys" not in contexts[0]
        assert "member_id" not in contexts[0]
        assert monitor_calls == 0
        assert frames == ["当前对话未启用监控工具", "[DONE]"]


def test_ai_tools_router_exposes_tools_listing() -> None:
    from app.modules.ai.chat.controller import ChatRouter

    assert any(str(getattr(route, "path", "")).endswith("/tools") for route in ChatRouter.routes)
    assert ai_tools_pkg is not None


@pytest.mark.parametrize("missing", [CustomException(msg="x")])
def test_guard_rejects_hallucinated_signature_param(missing: Exception) -> None:
    """guard 自检：若签名里出现闭包参数，构造工具时应直接失败（防止回归）。"""
    from app.modules.ai.tools.registry import _assert_no_injected_params

    async def _bad_tool(auth: Any) -> str:  # noqa: ANN401 - 故意模拟泄漏
        return "x"

    spec = registry_module.ReadonlyToolSpec("bad", "bad tool", _bad_tool)
    with pytest.raises(RuntimeError):
        _assert_no_injected_params([spec])
    assert isinstance(missing, Exception)
