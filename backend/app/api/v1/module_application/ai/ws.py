from fastapi import APIRouter, WebSocket

from app.core.logger import log
from app.core.router_class import OperationLogRoute
from .service import McpService
from .schema import ChatQuerySchema


WS_AI = APIRouter(route_class=OperationLogRoute, prefix="/application/ai", tags=["MCP智能助手WebSocket"])

@WS_AI.websocket("/ws", name="WebSocket聊天")
async def websocket_chat_controller(
    websocket: WebSocket,
):
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
                log.error(f"处理聊天查询出错: {str(e)}")
                await websocket.send_text(f"抱歉，处理您的请求时出现了错误: {str(e)}")
    except Exception as e:
        log.error(f"WebSocket聊天出错: {str(e)}")
    finally:
        await websocket.close()