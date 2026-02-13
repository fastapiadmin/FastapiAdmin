import json
import time
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, WebSocket
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.api.v1.module_system.auth.schema import AuthSchema
from app.config.setting import settings
from app.core.database import async_db_session
from app.core.dependencies import _verify_token
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import ChatMessageCreateSchema, ChatQuerySchema
from .service import ChatMessageService

WS_AI = APIRouter(
    route_class=OperationLogRoute,
    prefix="/application/ai",
    tags=["智能助手WebSocket"],
)


@WS_AI.websocket("/ws", name="WebSocket聊天")
async def websocket_chat_controller(
    websocket: WebSocket,
) -> None:
    """
    WebSocket聊天接口

    支持两种消息格式：
    1. 纯文本：直接发送消息内容
    2. JSON格式：{"message": "消息内容", "session_id": "会话ID", "files": [...]}

    ws://127.0.0.1:8001/api/v1/application/ai/ws?token=xxx
    """
    await websocket.accept()

    # 从查询参数获取token并认证
    token = websocket.query_params.get("token")
    auth = None
    if token:
        try:
            # 获取数据库和redis连接
            async with async_db_session() as db:
                redis = websocket.app.state.redis
                auth = await _verify_token(token, db, redis)
                user_info = f"用户: {auth.user.username}" if auth and auth.user else "未认证用户"
                log.info(f"WebSocket连接已建立: {websocket.client} - {user_info}")

                # 保存用户信息到websocket状态
                websocket.state.auth = auth

                # 进入消息循环
                while True:
                    data = await websocket.receive_text()
                    try:
                        message_data = json.loads(data)
                        query = ChatQuerySchema(**message_data)
                        log.info(f"收到聊天查询: {query}- 会话ID: {query.session_id}")

                        # 保存用户消息到数据库（使用独立的事务）
                        if query.session_id:
                            async with async_db_session() as msg_db:
                                async with msg_db.begin():
                                    msg_auth = AuthSchema(db=msg_db, check_data_scope=False)
                                    msg_auth.user = auth.user
                                    user_message_data = ChatMessageCreateSchema(
                                        session_id=query.session_id,
                                        type="user",
                                        content=query.message,
                                        timestamp=int(time.time()),
                                        files=query.files
                                    )
                                    log.info(f"准备保存用户消息: session_id={query.session_id}, content={query.message[:50]}...")
                                    await ChatMessageService.create_service(auth=msg_auth, data=user_message_data)
                                    log.info("用户消息保存成功")
                        else:
                            log.warning("未提供会话ID，跳过保存用户消息")

                        # 处理AI回复并保存
                        full_response = ""
                        async for chunk in chat_query(query=query):
                            if chunk:
                                await websocket.send_text(chunk)
                                full_response += chunk

                        # 保存AI回复到数据库（使用独立的事务）
                        if query.session_id and full_response:
                            async with async_db_session() as msg_db:
                                async with msg_db.begin():
                                    msg_auth = AuthSchema(db=msg_db, check_data_scope=False)
                                    msg_auth.user = auth.user
                                    assistant_message_data = ChatMessageCreateSchema(
                                        session_id=query.session_id,
                                        type="assistant",
                                        content=full_response,
                                        timestamp=int(time.time()),
                                        files=None
                                    )
                                    log.info(f"准备保存AI回复: session_id={query.session_id}, content={full_response[:50]}...")
                                    await ChatMessageService.create_service(auth=msg_auth, data=assistant_message_data)
                                    log.info("AI回复保存成功")
                        else:
                            log.warning(f"未提供会话ID或AI回复为空，跳过保存AI回复: session_id={query.session_id}, full_response_length={len(full_response)}")
                    except json.JSONDecodeError:
                        log.warning(f"收到非JSON消息: {data}")
                        await websocket.send_text("消息格式错误，请发送JSON格式的消息")
                    except Exception as e:
                        log.error(f"处理消息时出错: {e}")
                        await websocket.send_text(f"处理消息时出错: {str(e)}")
        except Exception as e:
            log.warning(f"WebSocket认证失败或聊天出错: {e}")
            await websocket.send_text(f"错误: {str(e)}")
            await websocket.close()
            return
    else:
        log.warning(f"WebSocket连接未提供token: {websocket.client}")
        await websocket.send_text("未提供认证token，请重新登录")
        await websocket.close()
        return


async def chat_query(
    query: ChatQuerySchema
) -> AsyncGenerator[str, Any]:
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
