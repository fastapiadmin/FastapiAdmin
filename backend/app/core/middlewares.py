import json
import time
import uuid
from dataclasses import replace
from types import MappingProxyType

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
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
from app.utils.ip_local_util import get_client_ip


def _strip_bearer(authorization: str) -> str | None:
    """从 Authorization header 提取 token，非 Bearer 返回 None。"""
    v = authorization.strip()
    if v[:7].lower() == "bearer ":
        v = v[7:].strip()
    elif v[:6].lower() == "bearer":
        v = v[6:].strip()
    else:
        return None
    return v or None


# 中间件配置的「安全默认值」：Redis 不可用 / 解析异常时启用，确保中间件行为可预测。
# 使用 MappingProxyType 防止任何地方误改导致跨请求污染。
_DEFAULT_CONFIG: MappingProxyType = MappingProxyType({
    "demo_enable": False,
    "ip_white_list": (),
    "ip_black_list": (),
    "white_api_list_path": (),
})


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
        """从 ctx / JWT 中提取 session_id 并写入 ctx。"""
        ctx = getattr(request.state, "ctx", None)
        sid = ctx.session_id if ctx else None
        if not sid and ctx and ctx.jwt_user_info:
            sid = ctx.jwt_user_info.get("session_id")
        if not sid:
            token = _strip_bearer(request.headers.get("Authorization", ""))
            if token:
                try:
                    payload = decode_access_token(token)
                    sid = getattr(payload, "sub", None) if payload else None
                except Exception:
                    sid = None
        if sid:
            request.state.ctx = replace(ctx or RequestContext(), session_id=sid)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        self._hydrate_session_id(request)

        client_ip = get_client_ip(request)
        logger.info("请求: {} {} | client={}", request.method, request.url.path, client_ip or "unknown")

        try:
            path = request.url.path
            config = await self._load_config(request)
            is_blacklisted = bool(client_ip and client_ip in config["ip_black_list"])
            in_demo = (
                config["demo_enable"]
                and request.method != "GET"
                and (client_ip is None or client_ip not in config["ip_white_list"])
                and not _is_path_whitelisted(path, config["white_api_list_path"])
            )

            if is_blacklisted or in_demo:
                logger.warning(
                    "请求被拦截: {} {} | ip={} | 原因={}",
                    request.method, path, client_ip,
                    "IP黑名单" if is_blacklisted else "演示模式",
                )
                return ErrorResponse(
                    msg="IP已被黑名单" if is_blacklisted else "演示环境，禁止操作"
                )

            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            logger.info("响应: {} | {:.4f}秒", response.status_code, process_time)
            return response
        except CustomException as e:
            logger.exception(f"中间件异常: {e!s}")
            return ErrorResponse(msg="系统异常，请联系管理员", data=str(e))

    @staticmethod
    async def _load_config(request: Request) -> dict:
        """加载中间件配置（带 60 秒内存缓存），失败时返回全部默认值。"""
        redis = getattr(request.app.state, "redis", None)
        if not redis:
            return _DEFAULT_CONFIG
        try:
            tenant_id = await _extract_tenant_from_token(request) or 1
            return await ParamsService.get_system_config_for_middleware(redis, tenant_id)
        except Exception:
            return _DEFAULT_CONFIG


class CustomGZipMiddleware(GZipMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app, minimum_size=settings.GZIP_MIN_SIZE, compresslevel=settings.GZIP_COMPRESS_LEVEL)


class CustomHTTPSRedirectMiddleware(HTTPSRedirectMiddleware):
    """HTTP → HTTPS 重定向中间件"""
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)


class CustomTrustedHostMiddleware(TrustedHostMiddleware):
    """可信主机 Host 头校验中间件"""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app, allowed_hosts=settings.ALLOWED_HOSTS)


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


_TENANT_WHITELIST_PREFIXES = ("/docs", "/redoc", "/openapi.json", "/metrics", "/static/")
_WHITELIST_ALL = (
    "/api/v1/system/auth/login", "/api/v1/system/auth/captcha",
    "/api/v1/system/auth/refresh", "/api/v1/health", "/api/v1/common/health",
) + tuple(settings.TENANT_WHITELIST_PATHS)


def _tenant_is_whitelisted(path: str) -> bool:
    """白名单路径：精确匹配公共接口，前缀匹配文档 / 静态资源。"""
    for prefix in (*_WHITELIST_ALL, *_TENANT_WHITELIST_PREFIXES):
        if path == prefix or path.startswith(prefix):
            return True
    return False


async def _extract_tenant_from_token(request: Request) -> int | None:
    """从 JWT + Redis 会话解析租户 ID；结果挂到 request.state 上以便本请求内复用。

    返回 None 表示未登录 / 会话过期，调用方应避免回退到平台租户（1）。
    """
    if hasattr(request.state, "tenant_id_resolved"):
        return request.state.tenant_id

    request.state.tenant_id_resolved = True
    request.state.tenant_id = None

    token = _strip_bearer(request.headers.get("Authorization", ""))
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        if not payload or not hasattr(payload, "sub"):
            return None

        session_id = payload.sub
        redis = getattr(request.app.state, "redis", None)
        raw = await await_redis_get(redis, session_id) if redis else None
        user_info = json.loads(raw) if raw else None

        base = getattr(request.state, "ctx", None) or RequestContext()
        request.state.ctx = replace(base, jwt_payload=payload, jwt_user_info=user_info)
        if user_info and user_info.get("tenant_id"):
            request.state.tenant_id = int(user_info["tenant_id"])
    except Exception:
        pass
    return request.state.tenant_id


async def await_redis_get(redis, key: str) -> str | None:
    """获取用户会话；Redis 不可用时返回 None。"""
    from app.common.enums import RedisInitKeyConfig
    from app.core.redis_crud import RedisCURD
    try:
        return await RedisCURD(redis).get(f"{RedisInitKeyConfig.USER_SESSION.key}:{key}")
    except Exception:
        return None


def _is_path_whitelisted(path: str, whitelist: list) -> bool:
    """精确匹配；``*`` 结尾表示前缀通配。"""
    for item in whitelist:
        if not isinstance(item, str) or not item:
            continue
        if item.endswith("*"):
            if path.startswith(item.rstrip("*")):
                return True
        elif path == item:
            return True
    return False


class TenantMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method == "OPTIONS" or _tenant_is_whitelisted(request.url.path):
            return await call_next(request)
        try:
            set_current_tenant(await _extract_tenant_from_token(request))
        except Exception:
            logger.exception("租户中间件异常: path={}", request.url.path)
        try:
            return await call_next(request)
        finally:
            clear_current_tenant()