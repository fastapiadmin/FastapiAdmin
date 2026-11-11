"""全局异常处理器：业务/HTTP/校验/数据库/未知异常。"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, OperationalError

from app.core.exceptions import CustomException, handle_exception


def _app() -> FastAPI:
    app = FastAPI(); handle_exception(app)
    @app.get("/custom")
    async def custom(): raise CustomException(msg="业务错误", data={"x": 1})
    @app.get("/http")
    async def http(): raise HTTPException(status_code=404, detail="not found")
    @app.get("/value")
    async def value(): raise ValueError("值错误")
    @app.get("/boom")
    async def boom(): raise RuntimeError("boom")
    @app.get("/integrity")
    async def integrity(): raise IntegrityError("stmt", {}, Exception("Duplicate entry"))
    @app.get("/conn")
    async def conn(): raise OperationalError("stmt", {}, Exception("connection refused"))
    return app


def test_handlers() -> None:
    c = TestClient(_app(), raise_server_exceptions=False)
    assert c.get("/custom").status_code == 400
    assert c.get("/http").status_code == 404
    assert c.get("/value").status_code == 400
    assert c.get("/boom").status_code == 500
    assert c.get("/integrity").status_code == 409
    assert c.get("/conn").status_code == 503
