"""监控控制器基础分支（健康检查/服务器信息/SSE）。"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from app.modules.monitor.health import controller as health
from app.modules.monitor.health.schema import ServiceInfoOut
from app.modules.monitor.server import controller as server


async def test_server_info_controller(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.monitor.server.schema import CpuInfoSchema, MemoryInfoSchema, PyInfoSchema, ServerMonitorSchema, SysInfoSchema
    result = ServerMonitorSchema(
        cpu=CpuInfoSchema(cpu_num=1, used=0, sys=0, free=100),
        mem=MemoryInfoSchema(total="1", used="0", free="1", usage=0),
        sys=SysInfoSchema(computer_ip="x", computer_name="x", os_arch="x", os_name="x", user_dir="x"),
        py=PyInfoSchema(name="x", version="x", start_time="x", run_time="x", home="x", memory_total="x", memory_used="x", memory_free="x", memory_usage=0),
        disks=[],
    )
    async def info(): return result
    monkeypatch.setattr(server.ServerService, "get_server_monitor_info", info)
    resp = await server.get_monitor_server_info_controller()
    assert resp.status_code == 200


async def test_health_check_ok_and_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(redis=None)))
    settings = SimpleNamespace(VERSION="3")
    ok = ServiceInfoOut(name="x", version="1", environment="test", db_status=1, redis_status=1)
    async def collect(_): return ok
    monkeypatch.setattr(health.HealthService, "collect", collect)
    resp = await health.health_check(request, settings)
    body = json.loads(resp.body)
    assert "系统健康" in body["msg"]

    bad = ServiceInfoOut(name="x", version="1", environment="test", db_status=0, redis_status=0)
    async def collect2(_): return bad
    monkeypatch.setattr(health.HealthService, "collect", collect2)
    resp2 = await health.health_check(request, settings)
    assert "服务异常" in json.loads(resp2.body)["msg"]


async def test_health_stream_yields(monkeypatch: pytest.MonkeyPatch) -> None:
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(redis=None)))
    async def collect(_): return ServiceInfoOut(name="x", version="1", environment="test", db_status=1, redis_status=1)
    async def no_sleep(_): return None
    monkeypatch.setattr(health.HealthService, "collect", collect)
    monkeypatch.setattr(health.asyncio, "sleep", no_sleep)
    gen = health.health_stream_controller(request)
    event = await anext(gen)
    assert "db_status" in event.raw_data
    event2 = await anext(gen)
    assert "db_status" in event2.raw_data
    await gen.aclose()
