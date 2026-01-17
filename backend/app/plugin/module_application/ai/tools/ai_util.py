from collections.abc import AsyncGenerator
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log


class AIClient:
    """
    AI客户端类，用于与OpenAI API交互。
    """

    def __init__(self) -> None:
        # 使用LangChain的ChatOpenAI类
        self.model = ChatOpenAI(
            api_key=lambda: settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            base_url=settings.OPENAI_BASE_URL,
            temperature=0.7,
            streaming=True,
        )

    async def process(self, query: str) -> AsyncGenerator[str, Any]:
        """
        处理查询并返回流式响应

        参数:
        - query (str): 用户查询。

        返回:
        - AsyncGenerator[str, Any]: 流式响应内容。
        """
        system_prompt = (
            """你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。请用中文回答用户的问题。"""
        )

        try:
            # 使用LangChain的异步流式生成
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query),
            ]

            # 使用LangChain的流式响应
            async for chunk in self.model.astream(messages):
                yield chunk.text

        except Exception as e:
            # 记录详细错误，返回友好提示
            log.error(f"AI处理查询失败: {e!s}")
            yield self._friendly_error_message(e)

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
            raise CustomException(f"解析 OpenAI 错误失败: {e!s}")

        text = str(e)
        msg = message or text

        # 特定错误映射
        # 欠费/账户状态异常
        if (
            (error_code == "Arrearage")
            or (error_type == "Arrearage")
            or ("in good standing" in (msg or ""))
        ):
            return "账户欠费或结算异常，访问被拒绝。请检查账号状态或更换有效的 API Key。"
        # 鉴权失败
        if status_code == 401 or "invalid api key" in msg.lower():
            return "鉴权失败，API Key 无效或已过期。请检查系统配置中的 API Key。"
        # 权限不足或被拒绝
        if status_code == 403 or error_type in {
            "PermissionDenied",
            "permission_denied",
        }:
            return "访问被拒绝，权限不足或账号受限。请检查账户权限设置。"
        # 配额不足或限流
        if status_code == 429 or error_type in {
            "insufficient_quota",
            "rate_limit_exceeded",
        }:
            return "请求过于频繁或配额已用尽。请稍后重试或提升账户配额。"
        # 客户端错误
        if status_code == 400:
            return f"请求参数错误或服务拒绝：{message or '请检查输入内容。'}"
        # 服务端错误
        if status_code in {500, 502, 503, 504}:
            return "服务暂时不可用，请稍后重试。"

        # 默认兜底
        return f"处理您的请求时出现错误：{msg}"
