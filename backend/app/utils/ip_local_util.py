import re

import httpx

from app.config.setting import settings
from app.core.logger import log


class IpLocalUtil:
    """
    获取IP归属地工具类
    """

    @classmethod
    def is_valid_ip(cls, ip: str) -> bool:
        """
        校验IP格式是否合法。

        参数:
        - ip (str): IP地址。

        返回:
        - bool: 是否合法。
        """
        ip_pattern = (
            r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        )
        return bool(re.match(ip_pattern, ip))

    @classmethod
    def is_private_ip(cls, ip: str) -> bool:
        """
        判断是否为内网IP。

        参数:
        - ip (str): IP地址。

        返回:
        - bool: 是否为内网IP。
        """
        priv_pattern = r"^(127\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)"
        return bool(re.match(priv_pattern, ip))

    @classmethod
    async def resolve_location_for_log(cls, ip: str | None) -> str | None:
        """
        登录与操作日志写入 ``login_location`` 时的统一解析入口。

        与 ``settings.DEBUG`` 联动：如果 ``DEBUG`` 为 ``False`` 时，关闭解析，不请求外网，仅返回占位描述，
        避免登录 POST 在 ``OperationLogRoute`` 收尾阶段因外网查询变慢。

        参数:
        - ip (str | None): 客户端 IP，可为空。

        返回:
        - str | None: 展示用归属地文案；无需解析时可能为 ``None``。
        """
        if not ip:
            return None
        if settings.DEBUG or not settings.IP_LOCATION_ENABLE:
            return (
                "内网IP"
                if cls.is_private_ip(ip)
                else "未解析(已关闭归属地查询)"
            )
        return await cls.get_ip_location(ip)

    @classmethod
    async def get_ip_location(cls, ip: str) -> str | None:
        """
        获取IP归属地信息。

        参数:
        - ip (str): IP地址。

        返回:
        - str | None: IP归属地信息，失败时返回"未知"或None。
        """
        # 校验IP格式
        if not cls.is_valid_ip(ip):
            log.error(f"IP格式不合法: {ip}")
            return "未知"

        # 内网IP直接返回
        if cls.is_private_ip(ip):
            return "内网IP"

        try:
            async with httpx.AsyncClient(timeout=settings.HTTPX_DEFAULT_TIMEOUT) as client:
                # 首选：ip9.com.cn API
                url = f"https://ip9.com.cn/get?ip={ip}"
                response = await cls._make_api_request(client, url)
                if response and response.json().get("ret") == 200:
                    result = response.json().get("data", {})
                    return f"{result.get('country', '')}-{result.get('prov', '')}-{result.get('city', '')}-{result.get('area', '')}-{result.get('isp', '')}"

                # 备用：ip-api.com（免费，无需 Key，45次/分钟）
                url = f"http://ip-api.com/json/{ip}?lang=zh-CN"
                response = await cls._make_api_request(client, url)
                if response and response.json().get("status") == "success":
                    data = response.json()
                    return f"{data.get('country', '')}-{data.get('regionName', '')}-{data.get('city', '')}-{data.get('isp', '')}"

        except Exception as e:
            log.error(f"获取IP归属地失败: {e}")
            return "未知"

    @classmethod
    async def _make_api_request(cls, client: httpx.AsyncClient, url: str):
        """
        单独的 API 请求方法，包含重试机制。

        参数:
        - client (AsyncClient): httpx 异步客户端。
        - url (str): 请求 URL。

        返回:
        - Response | None: 响应对象，失败时返回None。
        """
        try:
            response = await client.get(url)
            if response.status_code == 200:
                return response
        except Exception as e:
            log.error(f"IP 归属地 API 请求失败: {url} - {e}")
        return None
