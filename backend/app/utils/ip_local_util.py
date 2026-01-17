import re

import httpx

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
            # 使用ip-api.com API获取IP归属地信息
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 尝试使用 ip9.com.cn API
                url = f"https://ip9.com.cn/get?ip={ip}"
                response = await cls._make_api_request(client, url)
                if response and response.json().get("ret") == 200:
                    result = response.json().get("data", {})
                    return f"{result.get('country', '')}-{result.get('prov', '')}-{result.get('city', '')}-{result.get('area', '')}-{result.get('isp', '')}"

                # 尝试使用百度 API
                url = f"https://qifu-api.baidubce.com/ip/geo/v1/district?ip={ip}"
                response = await cls._make_api_request(client, url)
                if response and response.json().get("code") == "Success":
                    data = response.json().get("data", {})
                    # 修正原代码中的格式错误
                    return f"{data.get('country', '')}-{data.get('prov', '')}-{data.get('city', '')}-{data.get('district', '')}-{data.get('isp', '')}"

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
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await client.get(url, timeout=10)
                if response.status_code == 200:
                    return response
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                log.error(f"API 请求失败: {e}")
        return None
