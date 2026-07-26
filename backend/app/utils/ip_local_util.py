import ipaddress
import json
import re
from collections.abc import Callable

import httpx
from starlette.requests import Request

from app.common.enums import RedisInitKeyConfig, SysParamKey
from app.config.setting import settings
from app.core.logger import logger
from app.core.redis_crud import RedisCURD

# 归属地缓存：IP 几乎不变化，缓存 7 天可显著减少外网请求
_IP_CACHE_TTL: int = settings.IP_LOCATION_CACHE_TTL
# 硬超时（秒），避免外网查询阻塞主流程
_IP_QUERY_TIMEOUT: float = settings.IP_LOCATION_QUERY_TIMEOUT


def get_client_ip(request: Request) -> str:
    """从请求中提取客户端真实 IP（优先取反向代理透传的头部，返回空字串表示无法识别）。"""
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP", "")
    if real_ip:
        return real_ip.strip()
    if request.client:
        return request.client.host or ""
    return ""


class IpLocalUtil:
    """获取 IP 归属地工具类（带 Redis 缓存、硬超时、降级）。"""

    @classmethod
    def is_valid_ip(cls, ip: str) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @classmethod
    def is_private_ip(cls, ip: str) -> bool:
        try:
            return ipaddress.ip_address(ip).is_private
        except ValueError:
            return False

    @classmethod
    async def _is_location_enabled(cls, redis) -> bool:
        """从参数缓存读取 IP 归属地查询开关。"""
        if not redis:
            return False
        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{SysParamKey.IP_LOCATION_ENABLE.value}"
        try:
            raw = await RedisCURD(redis).get(redis_key)
            if raw:
                payload = json.loads(raw)
                cv = payload.get("config_value", "off")
                return cv in (True, "true", "1", "yes", "on")
        except (json.JSONDecodeError, TypeError, Exception):
            pass
        return False

    @classmethod
    async def resolve_location_for_log(cls, redis, ip: str | None) -> str | None:
        """登录日志写入入口：仅返回可同步获取的值（内网/缓存/降级），

        外网查询由后台任务异步执行（见 ``resolve_location_async``）。
        """
        if not ip:
            return None
        if not await cls._is_location_enabled(redis):
            return "内网IP" if cls.is_private_ip(ip) else "未解析(已关闭归属地查询)"
        if cls.is_private_ip(ip):
            return "内网IP"
        if redis:
            cached = await cls._cache_get(redis, ip)
            if cached is not None:
                return cached
        return "归属地查询中"

    @classmethod
    async def resolve_location_async(cls, redis, ip: str) -> str:
        """异步查询归属地（含缓存、降级、硬超时）。"""
        if not cls.is_valid_ip(ip):
            return "未知"
        if not await cls._is_location_enabled(redis):
            return "未解析(已关闭归属地查询)"
        if cls.is_private_ip(ip):
            return "内网IP"

        cached = await cls._cache_get(redis, ip) if redis else None
        if cached is not None:
            return cached

        result = await cls._query_with_timeout(ip)
        if redis:
            await cls._cache_set(redis, ip, result)
        return result

    @classmethod
    async def _query_with_timeout(cls, ip: str) -> str:
        """在硬超时内依次尝试多个 API，全部失败返回未知。"""
        apis: list[tuple[str, Callable, dict[str, str]]] = [
            ("http://ip-api.com/json", cls._parse_ipapi, {"lang": "zh-CN"}),
            ("https://whois.pconline.com.cn/ipJson.jsp", cls._parse_pconline, {"ip": ip, "json": "true"}),
        ]
        async with httpx.AsyncClient(timeout=_IP_QUERY_TIMEOUT) as client:
            for url, parser, params in apis:
                try:
                    resp = await client.get(f"{url}/{ip}" if "ip-api" in url else url, params=params)
                    if resp.status_code == 200:
                        data = resp.json() if "ip-api" in url else resp.text
                        location = parser(data)
                        if location:
                            return location
                except Exception as e:
                    logger.warning(f"IP 归属地 API 失败: {url} - {e}")
        return "未知"

    @staticmethod
    def _parse_ipapi(data: dict) -> str | None:
        if data.get("status") != "success":
            return None
        parts = [data.get("country"), data.get("regionName"), data.get("city"), data.get("isp")]
        joined = "-".join(filter(None, parts))
        return joined or None

    @staticmethod
    def _parse_pconline(text: str) -> str | None:
        """解析 pconline 返回的 JSONP 文本，格式如 'if( {\"ip\":\"...\",\"pro\":\"省\",\"city\":\"市\"} )'。"""
        try:
            match = re.search(r"\{.*\}", text)
            if not match:
                return None
            data = json.loads(match.group())
            parts = [data.get("pro"), data.get("city"), data.get("addr")]
            joined = " ".join(filter(None, parts))
            return joined or None
        except Exception:
            return None

    @staticmethod
    async def _cache_get(redis, ip: str) -> str | None:
        try:
            value = await RedisCURD(redis).get(f"ip:location:{ip}")
            return value.decode("utf-8") if value else None
        except Exception:
            return None

    @staticmethod
    async def _cache_set(redis, ip: str, value: str) -> None:
        try:
            await RedisCURD(redis).set(f"ip:location:{ip}", value, expire=_IP_CACHE_TTL)
        except Exception:
            pass
