"""中间件异常/配置解析/HTTPS 重定向。"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from fastapi.responses import Response

import app.core.middlewares as M
from app.core.exceptions import CustomException


class Req:
    def __init__(self, path="/x", method="POST", scheme="http"):
        self.url = SimpleNamespace(path=path, scheme=scheme, replace=lambda **k: "https://x")
        self.method = method
        self.headers = {"X-Forwarded-Proto": "http"}
        self.client = SimpleNamespace(host="1.2.3.4")
        self.app = SimpleNamespace(state=SimpleNamespace(redis=object()))


async def test_dispatch_custom_exception() -> None:
    mw = M.RequestLogMiddleware(app=lambda *a: None)
    async def bad(req): raise CustomException(msg="x")
    r = await mw.dispatch(Req(), bad)
    assert r.status_code == 400


async def test_load_config_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self, redis): pass
        async def mget(self, keys):
            return ["bad", json.dumps({"status": 1}), json.dumps({"status": 0, "config_value": '["1.2.3.4"]'})]
    monkeypatch.setattr(M, "RedisCURD", C)
    out = await M.RequestLogMiddleware._load_config(Req())
    assert out


async def test_https_redirect() -> None:
    mw = M.CustomHTTPSRedirectMiddleware(app=lambda *a: None)
    async def nxt(req): return Response()
    r = await mw.dispatch(Req(scheme="http"), nxt)
    assert r.status_code == 301
    r2 = await mw.dispatch(Req(scheme="https"), nxt)
    assert r2.status_code == 200
