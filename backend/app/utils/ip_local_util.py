import hashlib
import ipaddress
import json

import ip2region.searcher as xdb
import ip2region.util as xdb_util
from starlette.requests import Request

from app.common.enums import RedisInitKeyConfig, SysParamKey
from app.config.path_conf import IP2REGION_XDB_V4
from app.config.setting import settings
from app.core.logger import logger
from app.core.redis_crud import RedisCURD

# 归属地降级返回文案（登录日志/会话共用）
LOCATION_INTRANET = "内网IP"
LOCATION_DISABLED = "未解析(已关闭归属地查询)"
LOCATION_UNKNOWN = "未知"

_searcher: xdb.Searcher | None = None
_searcher_init_failed = False


def _is_trusted_proxy(ip: str | None) -> bool:
    """直连对端是否为可信代理（回环 / 内网地址，如 docker 网络中的 nginx）。"""
    if not ip:
        return False
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return addr.is_private or addr.is_loopback


def get_client_ip(request: Request) -> str:
    """提取客户端真实 IP（防代理头伪造）。

    - 直连对端不是可信代理（公网直连后端）：一律使用 TCP 对端地址，忽略代理头；
    - 直连对端是可信代理（nginx）：优先 X-Real-IP（nginx 用 ``$remote_addr``
      覆盖写入，客户端无法伪造）；其次按可信跳数从 X-Forwarded-For **右侧**
      取真实地址——每层代理向右追加一跳，左侧内容客户端可任意伪造。
    """
    peer = request.client.host if request.client else ""
    # TRUSTED_PROXY_HOPS=0 表示前置无代理，任何代理头都不可信
    if settings.TRUSTED_PROXY_HOPS <= 0 or not _is_trusted_proxy(peer):
        return peer

    real_ip = request.headers.get("X-Real-IP", "").strip()
    if real_ip:
        return real_ip

    forwarded = request.headers.get("X-Forwarded-For", "")
    parts = [p.strip() for p in forwarded.split(",") if p.strip()]
    if parts:
        # 每层代理向右侧追加一个其直连对端地址：hops=1 时最后一跳就是
        # nginx 看到的真实客户端；hops=2 时倒数第 2 个才是，最后一个是下游代理。
        # 链长度不足（内部短链请求）时退化为最左值。
        hops = min(settings.TRUSTED_PROXY_HOPS, len(parts))
        return parts[-hops]
    return peer


def get_client_fingerprint(request: Request) -> str:
    """客户端来源指纹（IP + User-Agent 摘要）。

    用于把一次性凭证（如验证码 key）绑定到签发它的来源，避免攻击者批量预取
    凭证后再投毒给其它请求使用。UA 由客户端可控，因此这里只能提高滥用成本，
    不能替代真实的人机校验。
    """
    ua = request.headers.get("user-agent", "")
    return hashlib.sha256(f"{get_client_ip(request)}|{ua}".encode()).hexdigest()[:32]


def _get_searcher() -> xdb.Searcher | None:
    """懒加载全局 xdb 查询器（全量内存模式）。

    数据文件缺失或损坏时不阻断应用启动与登录主流程，归属地统一降级为「未知」，
    告警只打一次避免刷屏。
    """
    global _searcher, _searcher_init_failed
    if _searcher is not None:
        return _searcher
    if _searcher_init_failed:
        return None
    try:
        buffer = xdb_util.load_content_from_file(str(IP2REGION_XDB_V4))
        _searcher = xdb.new_with_buffer(xdb_util.IPv4, buffer)
        logger.info(f"IP 归属地离线库加载完成: {IP2REGION_XDB_V4}")
    except Exception:
        _searcher_init_failed = True
        logger.warning(f"IP 归属地离线库加载失败，归属地将统一降级为「未知」: {IP2REGION_XDB_V4}", exc_info=True)
    return _searcher


def _format_region(raw: str) -> str:
    """格式化 xdb 返回的五段文本 ``国家|省|城市|运营商|ISO国家码``。

    - 末段 ISO 国家码仅用于机器识别，展示时丢弃；
    - 国内地址省略冗余的「中国」前缀，如「中国|广东省|深圳市|电信|CN」→「广东省 深圳市 电信」；
    - 海外地址保留国家，如「United States|California|0|Google LLC|US」→「United States California Google LLC」；
    - 「0」为占位段，直接丢弃。
    """
    parts = [p.strip() for p in raw.split("|")[:4] if p.strip() and p.strip() != "0"]
    if not parts:
        return ""
    if parts[0] == "中国":
        parts = parts[1:]
    return " ".join(parts)


class IpLocalUtil:
    """获取 IP 归属地工具类（ip2region 离线库，同步查询、无外网依赖）。"""

    @classmethod
    def is_valid_ip(cls, ip: str | None) -> bool:
        if not ip:
            return False
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @classmethod
    def is_private_ip(cls, ip: str | None) -> bool:
        """判断是否为非公网地址（内网/回环/链路本地/保留段）。"""
        if not ip:
            return False
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        return not addr.is_global

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
        except Exception:
            pass
        return False

    @classmethod
    async def resolve_location(cls, redis, ip: str | None) -> str | None:
        """解析 IP 归属地（登录日志/会话统一入口）。

        - IP 为空或非法 → None（不写归属地）；
        - 内网/回环/保留地址 → 「内网IP」；
        - 系统参数关闭归属地查询 → 「未解析(已关闭归属地查询)」；
        - 其余公网地址 → 离线库同步查询（微秒级），查不到 → 「未知」。
        """
        if not cls.is_valid_ip(ip):
            return None
        assert ip is not None  # is_valid_ip 已确保非空
        if cls.is_private_ip(ip):
            return LOCATION_INTRANET
        if not await cls._is_location_enabled(redis):
            return LOCATION_DISABLED
        return cls._query_offline(ip)

    @staticmethod
    def _query_offline(ip: str) -> str:
        """查询离线 xdb 库。任何异常都降级为「未知」，不影响登录主流程。"""
        searcher = _get_searcher()
        if searcher is None:
            return LOCATION_UNKNOWN
        try:
            # 当前仅内置 IPv4 库；IPv6 客户端地址直接降级，避免误用 v4 查询器抛错
            if ipaddress.ip_address(ip).version == 6:
                return LOCATION_UNKNOWN
            raw = searcher.search(ip)
        except Exception:
            logger.warning(f"IP 归属地离线查询失败: {ip}", exc_info=True)
            return LOCATION_UNKNOWN
        return _format_region(raw) or LOCATION_UNKNOWN
