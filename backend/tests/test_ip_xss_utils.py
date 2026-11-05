"""IP 归属地与 XSS 工具覆盖。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.utils.ip_local_util import (
    LOCATION_DISABLED,
    LOCATION_INTRANET,
    LOCATION_UNKNOWN,
    IpLocalUtil,
    _format_region,
    _is_trusted_proxy,
    get_client_fingerprint,
    get_client_ip,
)
from app.utils.xss_util import sanitize_html


def _req(peer="1.2.3.4", headers=None):
    return SimpleNamespace(client=SimpleNamespace(host=peer), headers=headers or {})


def test_trusted_proxy_and_client_ip(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _is_trusted_proxy(None) is False
    assert _is_trusted_proxy("bad") is False
    assert _is_trusted_proxy("127.0.0.1") is True
    assert _is_trusted_proxy("10.0.0.1") is True
    assert get_client_ip(_req("8.8.8.8")) == "8.8.8.8"
    # 可信代理 + X-Real-IP
    monkeypatch.setattr("app.utils.ip_local_util.settings.TRUSTED_PROXY_HOPS", 1)
    assert get_client_ip(_req("127.0.0.1", {"X-Real-IP": "9.9.9.9"})) == "9.9.9.9"
    # 多跳 XFF 取右侧
    req = _req("127.0.0.1", {"X-Forwarded-For": "fake, 8.8.8.8, 7.7.7.7"})
    monkeypatch.setattr("app.utils.ip_local_util.settings.TRUSTED_PROXY_HOPS", 2)
    assert get_client_ip(req) == "8.8.8.8"
    # 无代理头回退 peer
    assert get_client_ip(_req("127.0.0.1")) == "127.0.0.1"
    assert len(get_client_fingerprint(_req("1.1.1.1", {"user-agent": "ua"}))) == 32


def test_ip_validation_and_format() -> None:
    assert IpLocalUtil.is_valid_ip(None) is False
    assert IpLocalUtil.is_valid_ip("bad") is False
    assert IpLocalUtil.is_valid_ip("1.1.1.1") is True
    assert IpLocalUtil.is_private_ip(None) is False
    assert IpLocalUtil.is_private_ip("bad") is False
    assert IpLocalUtil.is_private_ip("10.0.0.1") is True
    assert IpLocalUtil.is_private_ip("8.8.8.8") is False
    assert _format_region("中国|广东省|深圳市|电信|CN") == "广东省 深圳市 电信"
    assert _format_region("United States|California|0|Google|US") == "United States California Google"
    assert _format_region("0|0") == ""


async def test_location_enabled_and_resolve(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.redis_crud import RedisCURD
    async def get(_): return '{"config_value":"on"}'
    monkeypatch.setattr(RedisCURD, "get", staticmethod(get))
    assert await IpLocalUtil._is_location_enabled(object()) is True
    monkeypatch.setattr(RedisCURD, "get", staticmethod(lambda _: (_ for _ in ()).throw(RuntimeError())))
    assert await IpLocalUtil._is_location_enabled(object()) is False
    assert await IpLocalUtil._is_location_enabled(None) is False
    assert await IpLocalUtil.resolve_location(None, "bad") is None
    assert await IpLocalUtil.resolve_location(None, "10.0.0.1") == LOCATION_INTRANET
    async def disabled(_): return False
    monkeypatch.setattr(IpLocalUtil, "_is_location_enabled", disabled)
    assert await IpLocalUtil.resolve_location(None, "8.8.8.8") == LOCATION_DISABLED
    async def enabled(_): return True
    monkeypatch.setattr(IpLocalUtil, "_is_location_enabled", enabled)
    monkeypatch.setattr(IpLocalUtil, "_query_offline", staticmethod(lambda ip: "x"))
    assert await IpLocalUtil.resolve_location(None, "8.8.8.8") == "x"


def test_query_offline_fallbacks(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.utils.ip_local_util as mod
    monkeypatch.setattr(mod, "_get_searcher", lambda: None)
    assert IpLocalUtil._query_offline("8.8.8.8") == LOCATION_UNKNOWN
    class S:
        def search(self, ip): return "中国|广东省|深圳市|电信|CN"
    monkeypatch.setattr(mod, "_get_searcher", lambda: S())
    assert IpLocalUtil._query_offline("8.8.8.8") == "广东省 深圳市 电信"
    assert IpLocalUtil._query_offline("2001:db8::1") == LOCATION_UNKNOWN


def test_sanitize_html() -> None:
    assert sanitize_html("") == ""
    assert "<script>" not in sanitize_html("<script>alert(1)</script><b>x</b>")
    assert "<b>" in sanitize_html("<b>x</b>")
