import json
import time
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask

from app.config.setting import settings
from app.core.base_schema import AuthSchema
from app.core.database import async_db_session
from app.core.logger import logger


async def _write_operation_log_async(log_data: dict) -> None:
    from app.api.v1.module_system.log.schema import OperationLogCreateSchema
    from app.api.v1.module_system.log.service import OperationLogService
    try:
        async with async_db_session() as _session:
            async with _session.begin():
                _auth = AuthSchema(db=_session)
                await OperationLogService(_auth).create(data=OperationLogCreateSchema(**log_data))
    except Exception:
        logger.exception("操作日志写入失败: path={}", log_data.get("request_path"))


class OperationLogRoute(APIRoute):
    """操作日志路由 — 自动记录请求/响应并后台异步写入"""

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            start = time.time()
            response: Response = await original_route_handler(request)

            if request.method not in settings.OPERATION_RECORD_METHOD:
                return response
            route: APIRoute = request.scope.get("route", None)

            try:
                oper_param: dict[str, Any] = {}
                content_type = request.headers.get("Content-Type", "")
                if content_type.startswith(("multipart/form-data", "application/x-www-form-urlencoded")):
                    form_data = await request.form()
                    oper_param["form"] = dict(form_data.items())
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

                ctx = getattr(request.state, "ctx", None)
                current_user_id = ctx.user_id if ctx else None

                log_data: dict[str, Any] = {
                    "request_path": request.url.path,
                    "request_method": request.method,
                    "request_payload": log_payload,
                    "response_code": response.status_code,
                    "response_json": response_data.decode(),
                    "process_time": f"{(time.time() - start):.2f}s",
                    "description": route.summary if route else "",
                    "created_id": current_user_id,
                    "updated_id": current_user_id,
                }
                response.background = BackgroundTask(_write_operation_log_async, log_data)
            except Exception:
                logger.warning("操作日志采集异常: {}", request.url.path, exc_info=True)
            return response

        return custom_route_handler
