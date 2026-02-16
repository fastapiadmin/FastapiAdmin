import json
import time

from fastapi import APIRouter, WebSocket

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.database import async_db_session
from app.core.dependencies import _verify_token
from app.core.logger import log
from app.core.router_class import OperationLogRoute
from app.plugin.module_ai.chat_message.schema import ChatMessageCreateSchema
from app.plugin.module_ai.chat_message.service import ChatMessageService

from .schema import ChatQuerySchema
from .service import ChatService

WS_AI = APIRouter(
    route_class=OperationLogRoute,
    prefix="/ai/chat",
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

    ws://127.0.0.1:8001/api/v1/ai/chat/ws?token=xxx
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
                        chat_result = ChatService.chat_query(query=query)
                        async for chunk in chat_result:
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
