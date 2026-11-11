"""请求日志/演示模式/请求ID中间件。"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from fastapi import Response

import app.core.middlewares as M


class Req:
    def __init__(self, path="/api/x", method="POST", ip="1.2.3.4", redis=None):
        self.url = SimpleNamespace(path=path)
        self.method = method
        self.headers = {"user-agent": "pytest"}
        self.client = SimpleNamespace(host=ip)
        self.app = SimpleNamespace(state=SimpleNamespace(redis=redis))


def _mw():
    return M.RequestLogMiddleware(app=lambda *a: None)


async def _next(req):
    return Response(status_code=200)


async def test_request_log_default_and_demo(monkeypatch: pytest.MonkeyPatch) -> None:
    mw = _mw()
    assert await mw.dispatch(Req(redis=None), _next) is not None
    from app.common.enums import SysParamKey
    vals = [
        json.dumps({"status": 0, "config_value": "true"}),
        json.dumps({"status": 0, "config_value": "[]"}),
        json.dumps({"status": 0, "config_value": '["9.9.9.9"]'}),
    ]
    class C:
        def __init__(self, redis): pass
        async def mget(self, keys): return vals
    monkeypatch.setattr(M, "RedisCURD", C)
    resp = await mw.dispatch(Req(redis=object()), _next)
    assert resp.status_code == 400
    resp2 = await mw.dispatch(Req(path="/api/x", method="GET", redis=object()), _next)
    assert resp2.status_code == 200


async def test_request_log_blacklist(monkeypatch: pytest.MonkeyPatch) -> None:
    mw = _mw()
    class C:
        def __init__(self, redis): pass
        async def mget(self, keys): return [None, None, json.dumps({"status": 0, "config_value": '["1.2.3.4"]'})]
    monkeypatch.setattr(M, "RedisCURD", C)
    resp = await mw.dispatch(Req(redis=object()), _next)
    assert resp.status_code == 400


async def test_correlation_id() -> None:
    mw = M.CorrelationIdMiddleware(app=lambda *a: None)
    resp = await mw.dispatch(Req(), _next)
    assert resp.headers.get("X-Correlation-ID")
