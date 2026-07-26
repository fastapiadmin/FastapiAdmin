import json
import time
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask

from app.config.setting import settings
from app.core.logger import logger
from app.utils.ip_local_util import get_client_ip

_WRITE_METHODS = {"POST", "PUT", "DELETE", "PATCH"}

# （通常在登录前调用，没有 JWT token）
_PUBLIC_WRITE_PATHS: set[str] = {
    "/auth/login",
    "/auth/token/refresh",
    "/auth/captcha/slider/complete",
    "/auth/user/register",
}


async def _write_operation_log_async(log_data: dict) -> None:
    """直接写入操作日志（函数体内导入避免循环依赖）。"""
    try:
        from app.api.v1.module_system.log.crud import OperationLogCRUD
        from app.api.v1.module_system.log.schema import OperationLogCreateSchema
        from app.core.base_schema import AuthSchema
        from app.core.database import async_db_session

        async with async_db_session() as _session, _session.begin():
            auth = AuthSchema()
            await OperationLogCRUD(auth, _session).create(data=OperationLogCreateSchema(**log_data))
    except Exception:
        logger.exception("操作日志写入失败: path={}", log_data.get("request_path"))


class OperationLogRoute(APIRoute):
    """操作日志路由 — 自动记录请求/响应并后台异步写入。

    根据 HTTP 方法判断：
    - 写方法 (POST/PUT/DELETE/PATCH)：注入租户写权限检查
    - 读方法 (GET/HEAD/OPTIONS)：不注入
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        methods = getattr(self, "methods", set())
        if methods & _WRITE_METHODS and self.path not in _PUBLIC_WRITE_PATHS:
            if self.dependencies is None:
                self.dependencies = []

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            start = time.perf_counter()
            response: Response = await original_route_handler(request)

            if request.method not in settings.OPERATION_RECORD_METHOD:
                return response
            route: APIRoute = request.scope.get("route", None)

            try:
                oper_param: dict[str, Any] = {}
                content_type = request.headers.get("Content-Type", "")
                if content_type.startswith(("multipart/form-data", "application/x-www-form-urlencoded")):
                    try:
                        form_data = await request.form()
                        # 过滤掉 UploadFile 对象，只保留纯表单字段
                        oper_param["form"] = {k: v for k, v in form_data.items() if not hasattr(v, "read")}
                    except Exception:
                        oper_param["form"] = {}
                else:
                    payload = await request.body()
                    if payload:
                        try:
                            oper_param["body"] = json.loads(payload.decode())
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            oper_param["body"] = payload.decode("utf-8", errors="ignore")

                if request.path_params:
                    oper_param["path_params"] = dict(request.path_params)

                log_payload = json.dumps(oper_param, ensure_ascii=False)
                if len(log_payload) > 2000:
                    log_payload = "请求参数过长"

                is_json = "application/json" in response.headers.get("Content-Type", "")
                response_data = response.body if is_json else b"{}"

                log_data: dict[str, Any] = {
                    "username": getattr(getattr(request.state, "ctx", None), "user_username", "unknown"),
                    "request_path": request.url.path,
                    "request_method": request.method,
                    "request_payload": log_payload,
                    "response_code": response.status_code,
                    "response_json": bytes(response_data).decode(),
                    "process_time": f"{(time.perf_counter() - start):.2f}s",
                    "description": route.summary if route else "",
                    "request_ip": get_client_ip(request),
                }
                response.background = BackgroundTask(_write_operation_log_async, log_data)
            except Exception:
                logger.warning("操作日志采集异常: {}", request.url.path, exc_info=True)
            return response

        return custom_route_handler
