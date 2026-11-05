"""登录/验证码服务纯函数与状态分支。"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.system.auth.service import CaptchaService, LoginService


def _user(**over):
    data = dict(id=1, username="u", name="U", avatar=None, is_superuser=False, status=0, dept_id=None, mobile="1", email=None, gender=0, last_login=None, roles=[])
    data.update(over)
    return SimpleNamespace(**data)


def test_collect_permissions() -> None:
    role_ok = SimpleNamespace(status=0, menus=[SimpleNamespace(id=1, status=0, permission="a"), SimpleNamespace(id=2, status=1, permission="b")])
    role_off = SimpleNamespace(status=1, menus=[SimpleNamespace(id=3, status=0, permission="c")])
    u = _user(roles=[None, role_off, role_ok])
    assert LoginService._collect_permissions(u) == (["a"], [1])
    assert LoginService._collect_permissions(_user(is_superuser=True)) == ([], [])


async def test_login_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    class R:
        def __init__(self, count=1, fail=False): self.count = count; self.fail = fail; self.expired = []
        async def incr(self, key):
            if self.fail: raise RuntimeError("redis down")
            return self.count
        async def expire(self, key, ttl): self.expired.append((key, ttl))
    await LoginService._check_login_rate_limit(R(), None)
    await LoginService._check_login_rate_limit(R(), "127.0.0.1")
    r = R(); await LoginService._check_login_rate_limit(r, "8.8.8.8")
    assert r.expired
    with pytest.raises(CustomException):
        await LoginService._check_login_rate_limit(R(count=99999), "8.8.8.8")
    await LoginService._check_login_rate_limit(R(fail=True), "8.8.8.8")


def test_build_login_out_and_session() -> None:
    token = SimpleNamespace(access_token="a", refresh_token="r", expires_in=1, token_type="bearer")
    u = _user(mobile="138")
    out = LoginService.build_login_out(token, u, with_mobile=True)
    assert out.user_info["mobile"] == "138"
    session = LoginService._build_session_dict(u, "s", ["p"], [1], "1.1.1.1", "BJ", SimpleNamespace(os=SimpleNamespace(family="mac"), user_agent=SimpleNamespace(family="Chrome")), "pc")
    assert session["session_id"] == "s" and session["permissions"] == ["p"] and session["browser"] == "Chrome"


async def test_captcha_read_states(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.redis_crud import RedisCURD
    values = [None, b"legacy", '{"status":"pending","fingerprint":"f","issued_at":1,"target_x":2}', "[1]"]
    async def get(_key): return values.pop(0)
    monkeypatch.setattr(RedisCURD, "get", staticmethod(get))
    with pytest.raises(CustomException):
        await CaptchaService._read_state(object(), "k")
    assert (await CaptchaService._read_state(object(), "k"))["status"] == "legacy"
    state = await CaptchaService._read_state(object(), "k")
    assert state["fingerprint"] == "f" and state["target_x"] == 2
    assert (await CaptchaService._read_state(object(), "k"))["status"] == ""


async def test_captcha_matches_write_check(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.redis_crud import RedisCURD
    stored = {}
    async def set(key, value, expire): stored[key] = value
    async def delete(key): stored.pop(key, None)
    monkeypatch.setattr(RedisCURD, "set", staticmethod(set))
    monkeypatch.setattr(RedisCURD, "delete", staticmethod(delete))
    monkeypatch.setattr("app.modules.system.auth.service.get_client_fingerprint", lambda request: "other")
    await CaptchaService._write_state(object(), "k", "pending", "f", 1, 2)
    assert "captcha_codes:k" in stored
    assert CaptchaService._matches({"fingerprint": ""}, object()) is True
    assert CaptchaService._matches({"fingerprint": "f"}, object()) is False
    await CaptchaService._write_state(object(), "v", "verified", "f", 1)
    async def get(_key): return stored["captcha_codes:v"]
    monkeypatch.setattr(RedisCURD, "get", staticmethod(get))
    # 来源不一致时先消费再拒绝
    with pytest.raises(CustomException):
        await CaptchaService.check_captcha(object(), object(), "v")
