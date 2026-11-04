"""监控服务分支覆盖：server/cache。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.modules.monitor.cache.service import CacheService
from app.modules.monitor.server.service import ServerService


def test_server_cpu_memory_system_and_disk(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ServerService, "_get_local_ip", staticmethod(lambda: "1.2.3.4"))
    monkeypatch.setattr("app.modules.monitor.server.service.psutil.cpu_times_percent", lambda: SimpleNamespace(user=1.0, system=2.0, idle=97.0))
    monkeypatch.setattr("app.modules.monitor.server.service.psutil.cpu_count", lambda logical=True: None)
    monkeypatch.setattr("app.modules.monitor.server.service.psutil.virtual_memory", lambda: SimpleNamespace(total=100, used=30, free=70, percent=30.0))
    cpu = ServerService._get_cpu_info()
    assert cpu.cpu_num == 1 and cpu.used == 1.0
    mem = ServerService._get_memory_info()
    assert mem.usage == 30.0
    sys = ServerService._get_system_info()
    assert sys.computer_ip == "1.2.3.4"


def test_server_disk_skips_permission_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    parts = [SimpleNamespace(mountpoint="/ok", fstype="ext4"), SimpleNamespace(mountpoint="/bad", fstype="x")]
    monkeypatch.setattr("app.modules.monitor.server.service.psutil.disk_partitions", lambda: parts)
    def usage(path):
        if path == "/bad":
            raise PermissionError
        return SimpleNamespace(total=100, used=40, free=60, percent=40.0)
    monkeypatch.setattr("app.modules.monitor.server.service.psutil.disk_usage", usage)
    disks = ServerService._get_disk_info()
    assert len(disks) == 1 and disks[0].usage == 40.0


def test_server_run_time() -> None:
    import time
    assert ServerService._calculate_run_time(time.time() - 3661) .startswith("0天1小时1分钟")


async def test_server_monitor_delegates(monkeypatch: pytest.MonkeyPatch) -> None:
    sentinel = object()
    monkeypatch.setattr(ServerService, "_collect_monitor_info", staticmethod(lambda: sentinel))
    assert await ServerService.get_server_monitor_info() is sentinel


async def test_cache_service_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.redis_crud import RedisCURD
    fake = SimpleNamespace()
    async def info(): return {"redis_version": "7"}
    async def db_size(): return 1
    async def commandstats(): return {"cmd_get": {"calls": 2}}
    async def get_keys(pattern=None): return ["prefix:a", "other"]
    async def get(key): return "v"
    async def delete(*keys): fake.deleted = keys
    for name, fn in [("info", info), ("db_size", db_size), ("commandstats", commandstats), ("get_keys", get_keys), ("get", get), ("delete", delete)]:
        monkeypatch.setattr(RedisCURD, name, staticmethod(fn))
    redis = object()
    monitor = await CacheService.get_monitor_statistical_info(redis)
    assert monitor.db_size == 1 and monitor.command_stats[0]["name"] == "get"
    names = await CacheService.get_monitor_cache_names()
    assert names
    assert await CacheService.get_monitor_cache_keys(redis, "prefix") == ["a"]
    assert (await CacheService.get_monitor_cache_value(redis, "c", "k")).cache_value == "v"
    assert await CacheService.clear_monitor_cache_by_name(redis, "prefix") is True
    assert await CacheService.clear_monitor_cache_by_key(redis, "a") is True
    assert await CacheService.clear_monitor_cache_all(redis) is True
