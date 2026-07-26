import asyncio
import json
from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Path, Query, Security, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_schema import AuthSchema, PaginationQueryParam
from app.core.database import async_db_session
from app.core.dependencies import AuthPermission, _authenticate, redis_getter
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.router_class import OperationLogRoute

from .schema import (
    AiChatRequestSchema,
    AiChatResponseSchema,
    AiModelConfigListResponse,
    AiModelConfigSchema,
    AiModelConfigUpdateSchema,
    ChatQuerySchema,
    ChatSessionCreateSchema,
    ChatSessionQueryParam,
    ChatSessionUpdateSchema,
)
from .service import AiModelConfigService, ChatService, get_user_model_config

ChatRouter = APIRouter(route_class=OperationLogRoute, prefix="/chat", tags=["AI管理"])


@ChatRouter.get("/detail/{session_id}", summary="获取会话详情", response_model=ResponseSchema[dict[str, Any]])
async def get_session_detail_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:detail"]))],
    session_id: Annotated[str, Path(description="会话ID")],
) -> JSONResponse:
    service = ChatService(auth)
    result = await service.get_session(session_id=session_id)
    return SuccessResponse(data=result, msg="获取会话详情成功")


@ChatRouter.get("/list", summary="查询会话列表", response_model=ResponseSchema[dict])
async def get_session_list_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:query"]))],
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ChatSessionQueryParam, Query()],
) -> JSONResponse:
    service = ChatService(auth)
    result_dict = await service.page(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询会话列表成功")


@ChatRouter.post("/create", status_code=status.HTTP_201_CREATED, summary="创建会话", response_model=ResponseSchema[dict[str, Any]])
async def create_session_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:create"]))],
    data: Annotated[ChatSessionCreateSchema, Body(description="会话创建参数")],
) -> JSONResponse:
    service = ChatService(auth)
    result = await service.create(data=data)
    return SuccessResponse(data=result, msg="创建会话成功")


@ChatRouter.put("/update/{session_id}", summary="更新会话", response_model=ResponseSchema[None])
async def update_session_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:update"]))],
    session_id: Annotated[str, Path(description="会话ID")],
    data: Annotated[ChatSessionUpdateSchema, Body(description="会话更新参数")],
) -> JSONResponse:
    service = ChatService(auth)
    await service.update(session_id=session_id, data=data)
    return SuccessResponse(data=None, msg="更新会话成功")


@ChatRouter.delete("/delete", summary="删除会话", response_model=ResponseSchema[None])
async def delete_session_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:delete"]))],
    session_ids: Annotated[list[str], Body(description="会话ID列表")],
) -> JSONResponse:
    service = ChatService(auth)
    await service.delete(session_ids=session_ids)
    return SuccessResponse(data=None, msg="删除会话成功")


@ChatRouter.post("/ai-chat", summary="AI 对话（非流式）", response_model=ResponseSchema[AiChatResponseSchema])
async def ai_chat_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:query"]))],
    data: Annotated[AiChatRequestSchema, Body(description="对话请求")],
) -> JSONResponse:
    service = ChatService(auth)
    result = await service.chat_non_stream(
        message=data.message,
        session_id=data.session_id,
    )
    return SuccessResponse(
        data=AiChatResponseSchema(
            response=result["response"],
            session_id=result["session_id"],
            function_calls=result.get("function_calls"),
            action=result.get("action"),
        ),
        msg="对话成功",
    )


@ChatRouter.get("/model", summary="获取 AI 模型配置列表", response_model=ResponseSchema[AiModelConfigListResponse])
async def list_model_config_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:query"]))],
) -> JSONResponse:
    service = AiModelConfigService(auth, redis)
    result = await service.list()
    return SuccessResponse(data=result, msg="获取模型配置列表成功")


@ChatRouter.post("/model", status_code=status.HTTP_201_CREATED, summary="新增一个 AI 模型配置", response_model=ResponseSchema[dict[str, Any]])
async def create_model_config_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:update"]))],
    data: Annotated[AiModelConfigUpdateSchema, Body(description="模型配置参数")],
) -> JSONResponse:
    service = AiModelConfigService(auth, redis)
    payload = AiModelConfigSchema(**data.model_dump())
    result = await service.create(payload)
    return SuccessResponse(data=result, msg="模型配置已新增")


@ChatRouter.put("/model/{config_id}", summary="更新指定 ID 的 AI 模型配置", response_model=ResponseSchema[dict[str, Any]])
async def update_model_config_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:update"]))],
    config_id: Annotated[str, Path(description="配置项 ID")],
    data: Annotated[AiModelConfigUpdateSchema, Body(description="模型配置参数")],
) -> JSONResponse:
    service = AiModelConfigService(auth, redis)
    payload = AiModelConfigSchema(**data.model_dump())
    result = await service.update(config_id, payload)
    return SuccessResponse(data=result, msg="模型配置已更新")


@ChatRouter.delete("/model/{config_id}", summary="删除指定 ID 的 AI 模型配置", response_model=ResponseSchema[None])
async def delete_model_config_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:update"]))],
    config_id: Annotated[str, Path(description="配置项 ID")],
) -> JSONResponse:
    service = AiModelConfigService(auth, redis)
    await service.delete(config_id)
    return SuccessResponse(data=None, msg="模型配置已删除")


@ChatRouter.post("/model/{config_id}/activate", summary="切换激活的 AI 模型配置", response_model=ResponseSchema[None])
async def activate_model_config_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ai:chat:update"]))],
    config_id: Annotated[str, Path(description="配置项 ID；传 __default__ 使用系统默认")],
) -> JSONResponse:
    service = AiModelConfigService(auth, redis)
    await service.set_active(config_id)
    return SuccessResponse(data=None, msg="已切换模型")


async def _send_error_and_close(websocket: WebSocket, message: str) -> None:
    """发送错误消息并关闭连接"""
    try:
        await websocket.send_text(f"错误: {message}")
    except RuntimeError:
        pass
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            pass


@ChatRouter.websocket("/ws", name="WebSocket聊天")
async def websocket_chat_controller(websocket: WebSocket) -> None:
    """WebSocket 聊天接口。

    支持的消息格式（JSON）：
    - 对话：{"message": "...", "session_id": "...", "files": [...]}
    - 停止：{"action": "stop", "session_id": "..."}

    ws://127.0.0.1:8001/api/v1/ai/chat/ws?token=xxx
    """
    # 接收客户端 subprotocol：约定客户端在 Sec-WebSocket-Protocol 中以 "access_token.<jwt>" 携带
    # 推荐方式：subprotocol 不会进 URL，不出现在 Nginx access log / 浏览器历史 / 抓包日志
    # 同时兼容旧版：用 query_params 传 token（不推荐，仅作向后兼容）
    #
    # 浏览器侧示例：
    #   new WebSocket(url, ["access_token", "access_token." + jwt])
    # Python websocket-client 示例：
    #   websockets.connect(url, subprotocols=["access_token", f"access_token.{jwt}"])
    token = None
    use_subprotocol = False
    if websocket.headers.get("sec-websocket-protocol"):
        for proto in websocket.headers["sec-websocket-protocol"].split(","):
            proto = proto.strip()
            if proto.startswith("access_token."):
                token = proto[len("access_token.") :]
                use_subprotocol = True
                break
    if not token:
        # 旧版/非浏览器客户端兼容：保留 query ?token=
        token = websocket.query_params.get("token")

    if not token:
        await _send_error_and_close(websocket, "未提供认证token，请重新登录")
        return

    if use_subprotocol:
        await websocket.accept(subprotocol="access_token")
    else:
        await websocket.accept()

    # 跨消息循环共享的停止信号：客户端发送 stop 时 set，生成器检测到后退出
    stop_event = asyncio.Event()
    # 标记当前是否在生成中，便于 stop 校验
    is_generating = asyncio.Event()

    try:
        redis = websocket.app.state.redis
        async with async_db_session() as db:
            auth = await _authenticate(token, db, redis)

            logger.info("WebSocket连接已建立: {} - 用户: {}", websocket.client, auth.user.username or "未认证")

            chat_service = ChatService(auth)

            # 消息循环
            while True:
                try:
                    data = await websocket.receive_text()
                    try:
                        message_data = json.loads(data)
                        query = ChatQuerySchema(**message_data)
                    except json.JSONDecodeError:
                        logger.warning("收到非JSON消息: {}", data)
                        await websocket.send_text("消息格式错误，请发送JSON格式的消息")
                        continue
                    except Exception as e:
                        logger.warning("消息校验失败: {}", e)
                        await websocket.send_text(f"消息格式错误: {e}")
                        continue

                    # 处理停止指令
                    if query.action == "stop":
                        if is_generating.is_set():
                            stop_event.set()
                            logger.info("收到停止指令: session={}", query.session_id)
                            await websocket.send_text("[STOPPED]")
                        else:
                            await websocket.send_text("当前没有正在进行的生成任务")
                        continue

                    # 对话指令
                    logger.info("收到聊天查询: session_id={}", query.session_id)

                    is_generating.set()
                    stop_event.clear()
                    # 读取用户的 AI 模型配置（每次可动态切换）
                    model_config = await get_user_model_config(redis, auth.user.id)
                    try:
                        async for chunk in chat_service.chat_query(
                            query=query,
                            stop_event=stop_event,
                            model_config=model_config,
                        ):
                            if not chunk:
                                continue
                            try:
                                await websocket.send_text(chunk)
                            except RuntimeError:
                                logger.warning("WebSocket连接已关闭，停止发送消息")
                                return
                    finally:
                        is_generating.clear()
                        stop_event.clear()

                    # 告知前端生成结束
                    try:
                        await websocket.send_text("[DONE]")
                    except RuntimeError:
                        return

                except WebSocketDisconnect:
                    logger.info("WebSocket连接已断开: {}", websocket.client)
                    return

    except CustomException as e:
        # 认证失败等业务异常
        logger.warning("WebSocket认证失败: {}", e.msg)
        await _send_error_and_close(websocket, e.msg)
    except Exception as e:
        # 未知异常
        logger.exception("WebSocket未知异常: {}", e)
        await _send_error_and_close(websocket, "服务器内部错误")
