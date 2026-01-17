from fastapi import APIRouter, WebSocket

from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import ChatQuerySchema
from .service import McpService

WS_AI = APIRouter(
    route_class=OperationLogRoute,
    prefix="/application/ai",
    tags=["MCP智能助手WebSocket"],
)


@WS_AI.websocket("/ws", name="WebSocket聊天")
async def websocket_chat_controller(
    websocket: WebSocket,
) -> None:
    """
    WebSocket聊天接口

    ws://127.0.0.1:8001/api/v1/application/ai/ws
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # 流式发送响应
            try:
                async for chunk in McpService.chat_query(query=ChatQuerySchema(message=data)):
                    if chunk:
                        await websocket.send_text(chunk)
            except Exception as e:
                log.error(f"处理聊天查询出错: {e!s}")
                await websocket.send_text(f"抱歉，处理您的请求时出现了错误: {e!s}")
    except Exception as e:
        log.error(f"WebSocket聊天出错: {e!s}")
    finally:
        try:
            # 检查WebSocket连接状态，避免重复关闭已关闭的连接
            if websocket.client_state != websocket.client_state.DISCONNECTED:
                await websocket.close()
        except Exception as e:
            log.debug(f"WebSocket关闭时发生异常(预期行为，服务可能正在关闭): {e!s}")
