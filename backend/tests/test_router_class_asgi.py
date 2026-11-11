"""操作日志路由的 ASGI 采集分支。"""

from __future__ import annotations

import json

from fastapi import APIRouter, FastAPI, Form
from fastapi.responses import Response
from fastapi.testclient import TestClient

from app.core.router_class import OperationLogRoute


def _app() -> FastAPI:
    app = FastAPI()
    r = APIRouter(route_class=OperationLogRoute)
    @r.post("/ok")
    async def ok():
        return {"a": 1}
    @r.post("/form")
    async def form(x: str = Form(...)):
        return {"x": x}
    @r.post("/big")
    async def big():
        return {"a": "x" * 5000}
    @r.post("/badjson")
    async def badjson():
        return Response("{bad", media_type="application/json")
    @r.post("/plain")
    async def plain():
        return Response("plain", media_type="text/plain")
    app.include_router(r)
    return app


def test_router_asgi_paths(monkeypatch) -> None:
    import app.core.router_class as m
    c = TestClient(_app())
    assert c.post("/ok", json={"a": 1}).status_code == 200
    assert c.post("/form", data={"x": "y"}).status_code == 200
    assert c.post("/big", json={"a": "x" * 10000}).status_code == 200
    assert c.post("/badjson").status_code == 200
    assert c.post("/plain").status_code == 200
    monkeypatch.setattr(m, "_redact_sensitive", lambda x: (_ for _ in ()).throw(RuntimeError("x")))
    assert c.post("/ok", json={"a": 1}).status_code == 200
    assert c.post("/form", content=b"bad", headers={"content-type": "multipart/form-data; boundary=x"}).status_code in (200, 400, 422)
