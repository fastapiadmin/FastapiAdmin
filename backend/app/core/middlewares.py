import json
import uuid
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.common.enums import RedisInitKeyConfig, SysParamKey
from app.common.response import ErrorResponse
from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import logger, reset_correlation_id, set_correlation_id
from app.core.redis_crud import RedisCURD
from app.utils.ip_local_util import get_client_ip


class CustomCORSMiddleware(CORSMiddleware):
    """CORS 中间件"""

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
    """演示模式 & IP黑名单拦截"""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = get_client_ip(request)

        try:
            path = request.url.path
            config = await self._load_config(request)
            is_blacklisted = bool(client_ip and client_ip in config[SysParamKey.IP_BLACK_LIST])
            in_demo = (
                config.get(SysParamKey.DEMO_ENABLE, False)
                and request.method != "GET"
                and (client_ip is None or client_ip not in config.get(SysParamKey.IP_WHITE_LIST, ()))
                and not any(
                    path.startswith(item.rstrip("*")) if item.endswith("*") else path == item
                    for item in settings.WHITE_API_LIST_PATH
                    if isinstance(item, str) and item
                )
            )

            if is_blacklisted or in_demo:
                logger.warning(
                    "请求被拦截: {} {} | ip={} | 原因={}",
                    request.method,
                    path,
                    client_ip,
                    "IP黑名单" if is_blacklisted else "演示模式",
                )
                return ErrorResponse(msg="IP已被黑名单" if is_blacklisted else "演示环境，禁止操作")

            return await call_next(request)
        except CustomException as e:
            logger.exception(f"中间件异常: {e!s}")
            return ErrorResponse(msg="系统异常，请联系管理员", data=str(e))

    @staticmethod
    async def _load_config(request: Request) -> dict:
        """加载中间件配置，失败时返回全部默认值。"""
        redis = getattr(request.app.state, "redis", None)
        if not redis:
            return {SysParamKey.DEMO_ENABLE: False, SysParamKey.IP_WHITE_LIST: (), SysParamKey.IP_BLACK_LIST: ()}
        try:
            config_keys = [
                f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{SysParamKey.DEMO_ENABLE.value}",
                f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{SysParamKey.IP_WHITE_LIST.value}",
                f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{SysParamKey.IP_BLACK_LIST.value}",
            ]
            config_values = await RedisCURD(redis).mget(config_keys)
            result: dict[str, Any] = {SysParamKey.DEMO_ENABLE: False, SysParamKey.IP_WHITE_LIST: (), SysParamKey.IP_BLACK_LIST: ()}
            raw_demo, raw_white, raw_black = config_values
            for raw, key in ((raw_demo, SysParamKey.DEMO_ENABLE), (raw_white, SysParamKey.IP_WHITE_LIST), (raw_black, SysParamKey.IP_BLACK_LIST)):
                if not raw:
                    continue
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    logger.error("解析系统配置 %s 失败", key)
                    continue
                if not isinstance(payload, dict) or payload.get("status", 0) != 0:
                    continue
                cv = payload.get("config_value")
                if cv is None:
                    continue
                if key == SysParamKey.DEMO_ENABLE:
                    result[key.value] = cv in (True, "true", "1", "yes", "on")
                else:
                    result[key.value] = json.loads(cv) if isinstance(cv, str) else cv
            return result
        except Exception:
            return {SysParamKey.DEMO_ENABLE: False, SysParamKey.IP_WHITE_LIST: (), SysParamKey.IP_BLACK_LIST: ()}


class CustomGZipMiddleware(GZipMiddleware):
    """GZip 压缩中间件"""

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
    """请求 ID 中间件"""

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

