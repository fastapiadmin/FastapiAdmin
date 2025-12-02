# -*- coding: utf-8 -*- 

from typing import AsyncGenerator
from openai import AsyncOpenAI, OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import httpx

from app.config.setting import settings
from app.core.logger import log


class AIClient:
    """
    AI客户端类，用于与OpenAI API交互。
    """

    def __init__(self):
        self.model = settings.OPENAI_MODEL
        # 创建一个不带冲突参数的httpx客户端
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True
        )
        
        # 使用自定义的http客户端
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            http_client=self.http_client
        )

    def _friendly_error_message(self, e: Exception) -> str:
        """将 OpenAI 或网络异常转换为友好的中文提示。"""
        # 尝试获取状态码与错误体
        status_code = getattr(e, "status_code", None)
        body = getattr(e, "body", None)
        message = None
        error_type = None
        error_code = None
        try:
            if isinstance(body, dict) and "error" in body:
                err = body.get("error") or {}
                error_type = err.get("type")
                error_code = err.get("code")
                message = err.get("message")
        except Exception:
            # 忽略解析失败
            pass

        text = str(e)
        msg = message or text

        # 特定错误映射
        # 欠费/账户状态异常
        if (error_code == "Arrearage") or (error_type == "Arrearage") or ("in good standing" in (msg or "")):
            return "账户欠费或结算异常，访问被拒绝。请检查账号状态或更换有效的 API Key。"
        # 鉴权失败
        if status_code == 401 or "invalid api key" in msg.lower():
            return "鉴权失败，API Key 无效或已过期。请检查系统配置中的 API Key。"
        # 权限不足或被拒绝
        if status_code == 403 or error_type in {"PermissionDenied", "permission_denied"}:
            return "访问被拒绝，权限不足或账号受限。请检查账户权限设置。"
        # 配额不足或限流
        if status_code == 429 or error_type in {"insufficient_quota", "rate_limit_exceeded"}:
            return "请求过于频繁或配额已用尽。请稍后重试或提升账户配额。"
        # 客户端错误
        if status_code == 400:
            return f"请求参数错误或服务拒绝：{message or '请检查输入内容。'}"
        # 服务端错误
        if status_code in {500, 502, 503, 504}:
            return "服务暂时不可用，请稍后重试。"

        # 默认兜底
        return f"处理您的请求时出现错误：{msg}"

    async def process(self, query: str)  -> AsyncGenerator[str, None]:
        """
        处理查询并返回流式响应

        参数:
        - query (str): 用户查询。

        返回:
        - AsyncGenerator[str, None]: 流式响应内容。
        """
        system_prompt = """你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。请用中文回答用户的问题。"""

        try:
            # 使用 await 调用异步客户端
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                stream=True
            )
            
            # 流式返回响应
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            # 记录详细错误，返回友好提示
            log.error(f"AI处理查询失败: {str(e)}")
            yield self._friendly_error_message(e)

    async def close(self) -> None:
        """
        关闭客户端连接
        """
        if hasattr(self, 'client'):
            await self.client.close()
        if hasattr(self, 'http_client'):
            await self.http_client.aclose()