"""登录 token 创建/刷新/退出生命周期。"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.auth.service import LoginService


class Redis:
    def __init__(self): self.store = {}; self.deleted = []; self.expired = []
    def __await__(self): return iter(())


class RedisCURD:
    def __init__(self, redis): self.redis = redis
    async def set(self, key, value, expire): self.redis.store[key] = value
    async def get(self, key): return self.redis.store.get(key)
    async def delete(self, *keys):
        self.redis.deleted.extend(keys)
        for k in keys: self.redis.store.pop(k, None)
    async def expire(self, key, expire): self.redis.expired.append((key, expire))


def _user():
    return SimpleNamespace(id=1, username="u", name="U", avatar=None, is_superuser=False, status=0, dept_id=None, mobile=None, email=None, gender=0, last_login=None, roles=[])


def _patch_token(monkeypatch, user_override=None):
    import app.modules.system.auth.service as mod
    monkeypatch.setattr(mod, "RedisCURD", RedisCURD)
    monkeypatch.setattr(mod, "create_access_token", lambda payload: "tok-" + ("refresh" if payload.is_refresh else "access"))
    monkeypatch.setattr(mod, "get_client_ip", lambda request: "1.1.1.1")
    async def _loc(redis, ip): return "BJ"
    monkeypatch.setattr(mod.IpLocalUtil, "resolve_location", staticmethod(_loc))
    class U:
        def __init__(self, *a): pass
        async def get(self, **kw): return user_override if user_override is not None else _user()
    monkeypatch.setattr(mod, "UserCRUD", U)


async def test_create_token(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_token(monkeypatch)
    redis = Redis()
    req = SimpleNamespace(headers={"user-agent": "ua"}, client=SimpleNamespace(host="1.1.1.1"))
    out = await LoginService.create_token(req, redis, _user(), "pc")
    assert out.access_token == "tok-access" and out.refresh_token == "tok-refresh"
    assert len(redis.store) == 3


async def test_refresh_success_and_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_token(monkeypatch)
    import app.modules.system.auth.service as mod
    redis = Redis(); sid = "s1"
    redis.store["user_session:" + sid] = json.dumps({"user_id": 1})
    redis.store["refresh_token:" + sid] = "old-refresh"
    monkeypatch.setattr(mod, "decode_access_token", lambda token: SimpleNamespace(is_refresh=True, sub=sid))
    out = await LoginService.refresh_token(object(), redis, "old-refresh")
    assert out.access_token == "tok-access"
    # 重放：存储中的 refresh 与新传入不一致，删除会话
    redis.store["user_session:s1"] = json.dumps({"user_id": 1}); redis.store["refresh_token:s1"] = "new"
    with pytest.raises(CustomException, match="失效"):
        await LoginService.refresh_token(object(), redis, "old-refresh")
    assert "user_session:s1" in redis.deleted


async def test_refresh_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_token(monkeypatch)
    import app.modules.system.auth.service as mod
    redis = Redis()
    monkeypatch.setattr(mod, "decode_access_token", lambda token: SimpleNamespace(is_refresh=False, sub="s"))
    with pytest.raises(CustomException, match="刷新令牌"):
        await LoginService.refresh_token(object(), redis, "x")
    monkeypatch.setattr(mod, "decode_access_token", lambda token: SimpleNamespace(is_refresh=True, sub="s"))
    with pytest.raises(CustomException, match="会话已过期"):
        await LoginService.refresh_token(object(), redis, "x")


async def test_logout(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_token(monkeypatch)
    import app.modules.system.auth.service as mod
    monkeypatch.setattr(mod, "decode_access_token", lambda token: SimpleNamespace(sub="s"))
    redis = Redis()
    assert await LoginService.logout(redis, "x") is True
    assert len(redis.deleted) == 3
    monkeypatch.setattr(mod, "decode_access_token", lambda token: SimpleNamespace(sub=None))
    with pytest.raises(CustomException):
        await LoginService.logout(redis, "x")
