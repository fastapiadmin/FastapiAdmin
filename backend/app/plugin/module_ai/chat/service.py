from collections.abc import AsyncGenerator
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log

from .schema import ChatQuerySchema


class ChatService:
    """
    聊天会话管理模块服务层
    """

    @classmethod
    async def chat_query(cls, query: ChatQuerySchema) -> AsyncGenerator[str, Any]:
        """
        处理聊天查询

        参数:
        - query (ChatQuerySchema): 聊天查询模型
        - config (AgentConfigSchema | None): 智能体配置模型

        返回:
        - AsyncGenerator[str, None]: 异步生成器,每次返回一个聊天响应
        """

        llm = ChatOpenAI(
            api_key=lambda: settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            base_url=settings.OPENAI_BASE_URL,
            streaming=True,
        )

        system_prompt = (
            """你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。请用中文回答用户的问题。"""
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query.message),
        ]

        try:
            async for chunk in llm.astream(messages):
                yield chunk.text

        except Exception as e:
            log.debug(f"关闭 LLM 客户端时发生异常(预期行为，服务可能正在关闭): {e}")

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

            if (
                (error_code == "Arrearage")
                or (error_type == "Arrearage")
                or ("in good standing" in (msg or ""))
            ):
                raise ValueError(
                    "账户欠费或结算异常，访问被拒绝。请检查账号状态或更换有效的 API Key。"
                )
            if status_code == 401 or "invalid api key" in msg.lower():
                raise ValueError("鉴权失败，API Key 无效或已过期。请检查系统配置中的 API Key。")
            if status_code == 403 or error_type in {
                "PermissionDenied",
                "permission_denied",
            }:
                raise ValueError("访问被拒绝，权限不足或账号受限。请检查账户权限设置。")
            if status_code == 429 or error_type in {
                "insufficient_quota",
                "rate_limit_exceeded",
            }:
                raise ValueError("请求过于频繁或配额已用尽。请稍后重试或提升账户配额。")
            if status_code == 400:
                raise ValueError(f"请求参数错误或服务拒绝：{message or '请检查输入内容。'}")
            if status_code in {500, 502, 503, 504}:
                raise ValueError("服务暂时不可用，请稍后重试。")

            raise CustomException(f"处理您的请求时出现错误：{msg}")
