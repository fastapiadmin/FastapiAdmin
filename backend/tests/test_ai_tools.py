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


async def test_tool_storage_and_cron_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    class Ctx:
        async def __aenter__(self): return object()
        async def __aexit__(self,*a): return False
    monkeypatch.setattr(r,"async_db_session",lambda: Ctx())
    class N:
        def __init__(self,*a): pass
        async def get_list(self): raise RuntimeError("x")
    monkeypatch.setattr(r,"StorageNodeService",N)
    tools={t.name:t for t in r.build_readonly_tools(object())}
    out=await tools["storage_sources"].func()
    assert out[0]["error"].startswith("列出存储源失败")
    class DB:
        async def execute(self,stmt): raise RuntimeError("x")
    class Ctx2(Ctx):
        async def __aenter__(self): return DB()
    monkeypatch.setattr(r,"async_db_session",lambda: Ctx2())
    out=await tools["cron_jobs"].func()
    assert out[0]["error"].startswith("列出定时任务失败")


async def test_storage_files_tool(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    class Ctx:
        async def __aenter__(self): return object()
        async def __aexit__(self,*a): return False
    monkeypatch.setattr(r,"async_db_session",lambda: Ctx())
    class N:
        def __init__(self,*a): pass
        async def get_list(self): return [SimpleNamespace(id=1,name="n")]
    monkeypatch.setattr(r,"StorageNodeService",N)
    tools={t.name:t for t in r.build_readonly_tools(object())}
    out=await tools["storage_files"].func("x")
    assert out["error"].startswith("存储源不存在") and out["available"]==["n"]


async def test_storage_tools_success(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    class Ctx:
        async def __aenter__(self): return object()
        async def __aexit__(self,*a): return False
    monkeypatch.setattr(r,"async_db_session",lambda: Ctx())
    class N:
        def __init__(self,*a): pass
        async def get_list(self): return [SimpleNamespace(id=1,name="n",protocol="s3",status=0,is_default=True)]
    monkeypatch.setattr(r,"StorageNodeService",N)
    class F:
        def __init__(self,*a): pass
        async def list_files(self,**kw): return [SimpleNamespace(name="a",is_dir=False,size=1)]
    monkeypatch.setattr(r,"StorageFileService",F)
    tools={t.name:t for t in r.build_readonly_tools(object())}
    sources=await tools["storage_sources"].func()
    assert sources[0]["name"]=="n"
    files=await tools["storage_files"].func("n")
    assert files["entries"][0]["name"]=="a"


async def test_redis_keys_tool(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    class B:
        @staticmethod
        async def scan_keys(redis,db,pattern,count):
            return SimpleNamespace(keys=[SimpleNamespace(key="k1")],cursor="c")
    monkeypatch.setattr(r,"RedisBrowserService",B)
    tools={t.name:t for t in r.build_readonly_tools(object(),redis=object())}
    out=await tools["redis_keys"].func("a*",5)
    assert out=={"keys":["k1"],"cursor":"c"}
