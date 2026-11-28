"""AI 只读工具回归测试。

固化：
1. 工具清单只含「查询类」且签名里**没有**闭包参数（auth/redis 不能变成模型要填的参数）；
2. 工具内部出错返回 ``{"error": ...}`` 而不是抛异常；
3. 工厂确实把工具注入 Agent；ChatService 的开关关闭时零行为变化。
"""

import inspect
from types import SimpleNamespace
from typing import Any

import pytest

from app.core.exceptions import CustomException
from app.modules.ai import tools as ai_tools_pkg
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
    setattr(service, "auth", SimpleNamespace(user=SimpleNamespace(is_superuser=True, username="root")))
    setattr(service, "redis", None)
    assert service._chat_tools(False) == []
    enabled = service._chat_tools(True)
    assert len(enabled) == 5
    assert all(callable(item) for item in enabled)


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
