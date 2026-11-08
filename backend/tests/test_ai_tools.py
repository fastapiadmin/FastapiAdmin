"""AI 只读工具注册与签名守卫。"""

from __future__ import annotations

import pytest

from app.modules.ai.tools import registry as r


def test_build_tools_names_and_signatures() -> None:
    tools = r.build_readonly_tools(object(), redis=None)
    assert [t.name for t in tools] == ["server_status", "storage_sources", "storage_files", "cron_jobs", "redis_keys"]


def test_injected_param_guard() -> None:
    def bad(auth): ...
    with pytest.raises(RuntimeError, match="闭包参数"):
        r._assert_no_injected_params([r.ReadonlyToolSpec("bad", "x", bad)])


async def test_redis_keys_without_redis() -> None:
    tools = {t.name: t for t in r.build_readonly_tools(object(), redis=None)}
    assert await tools["redis_keys"].func() == {"error": "Redis 不可用"}


async def test_server_status_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fail(): raise RuntimeError("x")
    monkeypatch.setattr(r.ServerService, "get_server_monitor_info", staticmethod(fail))
    tools = {t.name: t for t in r.build_readonly_tools(object())}
    out = await tools["server_status"].func()
    assert out["error"].startswith("查询服务器状态失败")
