"""在线用户服务分支测试（fake Redis/DB）。"""

from __future__ import annotations

import json
from datetime import datetime
from types import SimpleNamespace

import pytest

from app.modules.monitor.online.service import OnlineService

pytestmark = pytest.mark.asyncio


async def test_online_list_and_filters(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.redis_crud import RedisCURD
    from app.modules.monitor.online.schema import OnlineQueryParam
    sessions = {
        "a": json.dumps({"user_id": 1, "name": "Alice", "ipaddr": "1.1.1.1", "login_location": "Beijing", "login_time": "1"}),
        "b": json.dumps({"user_id": 2, "name": "Bob", "ipaddr": "2.2.2.2", "login_location": "Shanghai", "login_time": "2"}),
    }
    async def scan(_pattern): return [b"access_token:a", b"access_token:b"]
    async def mget(_keys): return [b"tok-a", b"tok-b"]
    async def get(key):
        sid = key.rsplit(":", 1)[-1]
        return sessions.get(sid)
    async def delete(*_keys): pass
    monkeypatch.setattr(RedisCURD, "scan_keys", staticmethod(scan))
    monkeypatch.setattr(RedisCURD, "mget", staticmethod(mget))
    monkeypatch.setattr(RedisCURD, "get", staticmethod(get))
    monkeypatch.setattr(RedisCURD, "delete", staticmethod(delete))
    monkeypatch.setattr("app.modules.monitor.online.service.decode_access_token", lambda token: SimpleNamespace(sub=(token.decode() if isinstance(token, bytes) else token)[-1]))
    online = await OnlineService.get_online_list(object())
    assert [x["name"] for x in online] == ["Bob", "Alice"]
    assert [x["name"] for x in await OnlineService.get_current_user_sessions(object(), 1)] == ["Alice"]
    # query filters: name / ip / location
    q = OnlineQueryParam(name="ali")
    assert [x["name"] for x in await OnlineService.get_online_list(object(), q)] == ["Alice"]
    q2 = OnlineQueryParam(ipaddr="2.2.2.2")
    assert [x["name"] for x in await OnlineService.get_online_list(object(), q2)] == ["Bob"]
    q3 = OnlineQueryParam(login_location="bei")
    assert [x["name"] for x in await OnlineService.get_online_list(object(), q3)] == ["Alice"]


async def test_online_invalid_token_cleanup(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.redis_crud import RedisCURD
    deleted = []
    async def scan(_): return ["access_token:x"]
    async def mget(_): return ["bad"]
    async def delete(*keys): deleted.extend(keys)
    monkeypatch.setattr(RedisCURD, "scan_keys", staticmethod(scan))
    monkeypatch.setattr(RedisCURD, "mget", staticmethod(mget))
    monkeypatch.setattr(RedisCURD, "delete", staticmethod(delete))
    monkeypatch.setattr("app.modules.monitor.online.service.decode_access_token", lambda token: (_ for _ in ()).throw(ValueError()))
    assert await OnlineService.get_online_list(object()) == []
    assert len(deleted) == 3


async def test_delete_clear_online(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.redis_crud import RedisCURD
    calls = []
    async def delete(*keys): calls.append(("delete", keys))
    async def clear(*keys): calls.append(("clear", keys))
    monkeypatch.setattr(RedisCURD, "delete", staticmethod(delete))
    monkeypatch.setattr(RedisCURD, "clear", staticmethod(clear))
    await OnlineService.delete_online(object(), "sid")
    await OnlineService.clear_online(object())
    assert len(calls) == 6


async def test_build_login_trend(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.monitor.online.service import OnlineService as S
    from datetime import timedelta
    today = datetime(2026, 1, 8)
    week = today - timedelta(days=6)

    class DB:
        def __init__(self): self.i = 0
        async def execute(self, stmt):
            self.i += 1
            if self.i == 1:
                return SimpleNamespace(all=lambda: [SimpleNamespace(day="2026-01-08", logins=2, unique_users=1)])
            return SimpleNamespace(all=lambda: [SimpleNamespace(day="2026-01-08", new_users=3)])

    trend = await S._build_login_trend(DB(), today_start=today, week_start=week)
    assert len(trend) == 7
    assert trend[-1].day == "2026-01-08" and trend[-1].logins == 2 and trend[-1].new_users == 3
