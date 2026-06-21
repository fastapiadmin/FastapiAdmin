import json
import time
import uuid
from dataclasses import replace

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.api.v1.module_system.params.service import ParamsService
from app.common.response import ErrorResponse
from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.request_context import RequestContext, clear_current_tenant, reset_correlation_id, set_correlation_id, set_current_tenant
from app.core.security import decode_access_token


def _strip_bearer(authorization: str) -> str | None:
    """从 Authorization header 提取 token，非 Bearer 返回 None。"""
    v = authorization.strip()
    if v.lower().startswith("bearer "):
        v = v[7:].strip()
    elif v.lower().startswith("bearer"):
        v = v[6:].strip()
    else:
        return None
    return v or None


class CustomCORSMiddleware(CORSMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_methods=settings.ALLOW_METHODS,
            allow_headers=settings.ALLOW_HEADERS,
            allow_credentials=settings.ALLOW_CREDENTIALS,
            expose_headers=settings.CORS_EXPOSE_HEADERS,
        )


class RequestLogMiddleware(BaseHTTPMiddleware):
    """请求日志 & 演示模式拦截"""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    @staticmethod
    def _hydrate_session_id(request: Request) -> None:
        """从 request.state.ctx 或 JWT 中提取 session_id 并写入 ctx（纯 side-effect）。

        JWT sub 现为纯 session_id 字符串，无需 JSON 解析。
        """
        ctx = getattr(request.state, "ctx", None)
        if ctx:
            if ctx.session_id:
                return
            if ctx.jwt_user_info:
                sid = ctx.jwt_user_info.get("session_id")
                if sid:
                    request.state.ctx = replace(ctx, session_id=sid)
                    return

        token = _strip_bearer(request.headers.get("Authorization", ""))
        if not token:
            return
        try:
            payload = decode_access_token(token)
            if not payload or not hasattr(payload, "sub"):
                return
            sid = payload.sub
            if sid:
                base = ctx or RequestContext()
                request.state.ctx = replace(base, session_id=sid)
        except Exception:
            pass

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        self._hydrate_session_id(request)

        logger.info("请求: {} {} | client={}", request.method, request.url.path,
                     request.client.host if request.client else "unknown")

        try:
            path = request.scope.get("path")
            request_ip = (
                (x_forwarded_for.split(",")[0].strip())
                if (x_forwarded_for := request.headers.get("X-Forwarded-For"))
                else request.client.host if request.client else None
            )

            try:
                redis = request.app.state.redis
                config = await ParamsService.get_system_config_for_middleware(redis)
                demo_enable = config["demo_enable"]
                ip_white_list = config["ip_white_list"]
                white_api_list_path = config["white_api_list_path"]
                ip_black_list = config["ip_black_list"]
            except Exception:
                demo_enable = False
                ip_white_list, white_api_list_path, ip_black_list = [], [], []

            should_block = (request_ip and request_ip in ip_black_list) or (
                demo_enable and request.method != "GET"
                and request_ip not in ip_white_list
                and path not in white_api_list_path
            )

            if should_block:
                logger.warning("演示模式拦截: {} {} | ip={}", request.method, path, request_ip)
                return ErrorResponse(msg="演示环境，禁止操作")

            response = await call_next(request)
            process_time = round(time.time() - start_time, 5)
            response.headers["X-Process-Time"] = str(process_time)
            logger.info("响应: {} | {:.1f}ms", response.status_code, process_time * 1000)
            return response
        except CustomException as e:
            logger.exception(f"中间件异常: {e!s}")
            return ErrorResponse(msg="系统异常，请联系管理员", data=str(e))


class CustomGZipMiddleware(GZipMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app, minimum_size=settings.GZIP_MIN_SIZE, compresslevel=settings.GZIP_COMPRESS_LEVEL)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self._hsts = settings.HSTS_ENABLE

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self._hsts:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=(), usb=(), magnetometer=(), gyroscope=()"
        return response


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        self._header = "X-Correlation-ID"
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        cid = request.headers.get(self._header) or str(uuid.uuid4())
        token = set_correlation_id(cid)
        try:
            response = await call_next(request)
            response.headers[self._header] = cid
            return response
        finally:
            reset_correlation_id(token)


_TENANT_WHITELIST_PREFIXES = ("/docs", "/redoc", "/ljdoc", "/openapi.json", "/metrics", "/static")
_TENANT_WHITELIST_PATHS = (
    "/api/v1/system/auth/login", "/api/v1/system/auth/captcha",
    "/api/v1/system/auth/refresh", "/api/v1/health", "/api/v1/common/health",
)

_WHITELIST_ALL = _TENANT_WHITELIST_PATHS + tuple(settings.TENANT_WHITELIST_PATHS)


def _tenant_is_whitelisted(path: str) -> bool:
    return any(path.startswith(p) for p in _WHITELIST_ALL) or \
        any(path.startswith(p) for p in _TENANT_WHITELIST_PREFIXES)


async def _extract_tenant_from_token(request: Request) -> int | None:
    token = _strip_bearer(request.headers.get("Authorization", ""))
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        if not payload or not hasattr(payload, "sub"):
            return None
        session_id = payload.sub
        user_info = None

        # 从 Redis 读取完整会话信息（含 tenant_id）
        redis = request.app.state.redis
        raw = await await_redis_get(redis, session_id) if redis else None
        if raw:
            user_info = json.loads(raw)

        base = getattr(request.state, "ctx", None) or RequestContext()
        request.state.ctx = replace(base, jwt_payload=payload, jwt_user_info=user_info)
        return user_info.get("tenant_id") if user_info else None
    except Exception:
        return None


async def await_redis_get(redis, key: str) -> str | None:
    """异步获取 Redis 键值（封装为可复用工具函数）。"""
    from app.common.enums import RedisInitKeyConfig
    from app.core.redis_crud import RedisCURD
    try:
        return await RedisCURD(redis).get(
            f"{RedisInitKeyConfig.USER_SESSION.key}:{key}"
        )
    except Exception:
        return None


class TenantMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path
        if request.method == "OPTIONS" or _tenant_is_whitelisted(path):
            return await call_next(request)
        try:
            tenant_id = await _extract_tenant_from_token(request)
            set_current_tenant(tenant_id)
        except Exception:
            logger.exception("租户中间件异常: path={}", path)
        try:
            return await call_next(request)
        finally:
            clear_current_tenant()
