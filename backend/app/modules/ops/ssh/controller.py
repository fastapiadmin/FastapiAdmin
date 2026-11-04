"""SSH 运维接口：主机/片段管理、终端会话（POST 轮询）、批量执行、日志跟踪。"""

import base64
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, Security, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_schema import AuthSchema
from app.core.dependencies import AuthPermission, db_getter
from app.core.router_class import OperationLogRoute
from app.core.validator import to_local_datetime

from .schema import (
    BatchExecResultSchema,
    BatchExecSchema,
    SshHostCreateSchema,
    SshHostOutSchema,
    SshHostTestSchema,
    SshHostUpdateSchema,
    SshSnippetCreateSchema,
    SshSnippetOutSchema,
    SshSnippetUpdateSchema,
    TerminalInputSchema,
    TerminalLogOpenSchema,
    TerminalOpenSchema,
    TerminalPollSchema,
    TerminalResizeSchema,
    TerminalSessionSchema,
)
from .service import SshHostService, SshSnippetService
from .terminal import TerminalManager

SshRouter = APIRouter(route_class=OperationLogRoute, prefix="/ssh", tags=["SSH运维"])

_QUERY = "module_ops:ssh:query"
_TERMINAL = "module_ops:ssh:terminal"
_EXEC = "module_ops:ssh:exec"


def _session_schema(session) -> TerminalSessionSchema:
    return TerminalSessionSchema(
        session_id=session.session_id,
        host_id=session.host_id,
        host_name=session.host_name,
        cols=session.cols,
        rows=session.rows,
        created_at=(to_local_datetime(datetime.fromtimestamp(session.created_at, tz=UTC)) or datetime.fromtimestamp(session.created_at, tz=UTC)).isoformat(timespec="seconds"),
    )


# ── 主机管理 ──────────────────────────────────────────────────────────


@SshRouter.get("/host/list", summary="查询 SSH 主机列表", response_model=ResponseSchema[list[SshHostOutSchema]])
async def list_ssh_host_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_QUERY]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
) -> JSONResponse:
    result = await SshHostService(auth, db).get_list()
    return SuccessResponse(data=result, msg="查询主机列表成功")


@SshRouter.get("/host/detail/{id}", summary="查询 SSH 主机详情", response_model=ResponseSchema[SshHostOutSchema])
async def detail_ssh_host_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_QUERY]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(description="主机ID", ge=1)],
) -> JSONResponse:
    result = await SshHostService(auth, db).detail(id=id)
    return SuccessResponse(data=result, msg="查询主机详情成功")


@SshRouter.post("/host/create", status_code=status.HTTP_201_CREATED, summary="新增 SSH 主机", response_model=ResponseSchema[SshHostOutSchema])
async def create_ssh_host_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ops:ssh:create"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    data: Annotated[SshHostCreateSchema, Body(description="主机配置（密码/私钥加密存储）")],
) -> JSONResponse:
    result = await SshHostService(auth, db).create(data=data)
    return SuccessResponse(data=result, msg="新增主机成功")


@SshRouter.put("/host/update/{id}", summary="修改 SSH 主机", response_model=ResponseSchema[SshHostOutSchema])
async def update_ssh_host_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ops:ssh:update"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(description="主机ID", ge=1)],
    data: Annotated[SshHostUpdateSchema, Body(description="主机配置（凭据不传表示不修改）")],
) -> JSONResponse:
    result = await SshHostService(auth, db).update(id=id, data=data)
    return SuccessResponse(data=result, msg="修改主机成功")


@SshRouter.delete("/host/delete", summary="删除 SSH 主机", response_model=ResponseSchema[None])
async def delete_ssh_host_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ops:ssh:delete"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    ids: Annotated[list[int], Body(description="主机ID列表")],
) -> JSONResponse:
    await SshHostService(auth, db).delete(ids=ids)
    return SuccessResponse(msg="删除主机成功")


@SshRouter.post("/host/test", summary="按填写中的凭据测试 SSH 连接（不落库）", response_model=ResponseSchema[bool])
async def test_ssh_host_config_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ops:ssh:update"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    data: Annotated[SshHostTestSchema, Body(description="连接配置")],
) -> JSONResponse:
    result = await SshHostService(auth, db).test_connection(data)
    return SuccessResponse(data=result, msg="连接成功")


@SshRouter.post("/host/test/{id}", summary="测试已保存的 SSH 主机", response_model=ResponseSchema[bool])
async def test_ssh_host_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_QUERY]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(description="主机ID", ge=1)],
) -> JSONResponse:
    result = await SshHostService(auth, db).test_by_id(id=id)
    return SuccessResponse(data=result, msg="连接成功")


# ── 命令片段 ──────────────────────────────────────────────────────────


@SshRouter.get("/snippet/list", summary="查询命令片段列表", response_model=ResponseSchema[list[SshSnippetOutSchema]])
async def list_ssh_snippet_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ops:snippet:query"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
) -> JSONResponse:
    result = await SshSnippetService(auth, db).get_list()
    return SuccessResponse(data=result, msg="查询片段列表成功")


@SshRouter.post("/snippet/create", status_code=status.HTTP_201_CREATED, summary="新增命令片段", response_model=ResponseSchema[SshSnippetOutSchema])
async def create_ssh_snippet_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ops:snippet:create"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    data: Annotated[SshSnippetCreateSchema, Body(description="片段内容")],
) -> JSONResponse:
    result = await SshSnippetService(auth, db).create(data=data)
    return SuccessResponse(data=result, msg="新增片段成功")


@SshRouter.put("/snippet/update/{id}", summary="修改命令片段", response_model=ResponseSchema[SshSnippetOutSchema])
async def update_ssh_snippet_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ops:snippet:update"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    id: Annotated[int, Path(description="片段ID", ge=1)],
    data: Annotated[SshSnippetUpdateSchema, Body(description="片段内容")],
) -> JSONResponse:
    result = await SshSnippetService(auth, db).update(id=id, data=data)
    return SuccessResponse(data=result, msg="修改片段成功")


@SshRouter.delete("/snippet/delete", summary="删除命令片段", response_model=ResponseSchema[None])
async def delete_ssh_snippet_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_ops:snippet:delete"]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    ids: Annotated[list[int], Body(description="片段ID列表")],
) -> JSONResponse:
    await SshSnippetService(auth, db).delete(ids=ids)
    return SuccessResponse(msg="删除片段成功")


# ── 终端会话（POST 轮询）─────────────────────────────────────────────


@SshRouter.post("/terminal/open", summary="打开终端会话", response_model=ResponseSchema[TerminalSessionSchema])
async def open_terminal_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_TERMINAL]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    data: Annotated[TerminalOpenSchema, Body(description="主机与终端尺寸")],
) -> JSONResponse:
    session = await SshHostService(auth, db).open_terminal(host_id=data.host_id, cols=data.cols, rows=data.rows)
    return SuccessResponse(data=_session_schema(session), msg="终端会话已打开")


@SshRouter.post("/log/open", summary="打开日志跟踪会话（tail -F）", response_model=ResponseSchema[TerminalSessionSchema])
async def open_log_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_TERMINAL]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    data: Annotated[TerminalLogOpenSchema, Body(description="主机与日志路径")],
) -> JSONResponse:
    session = await SshHostService(auth, db).open_log_tail(host_id=data.host_id, path=data.path, lines=data.lines)
    return SuccessResponse(data=_session_schema(session), msg="日志跟踪会话已打开")


@SshRouter.get("/terminal/{session_id}/poll", summary="轮询终端输出（长轮询）", response_model=ResponseSchema[TerminalPollSchema])
async def poll_terminal_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_TERMINAL]))],
    session_id: Annotated[str, Path(min_length=8, max_length=64, description="会话ID")],
    timeout: Annotated[float, Query(ge=0, le=5, description="长轮询等待秒数")] = 2.0,
) -> JSONResponse:
    data, closed, exit_status = TerminalManager.poll(session_id, auth.user.id or 0, timeout)
    return SuccessResponse(
        data=TerminalPollSchema(
            data=base64.b64encode(data).decode() if data else "",
            closed=closed,
            exit_status=exit_status,
        ),
        msg="轮询成功",
    )


@SshRouter.post("/terminal/{session_id}/input", summary="终端输入（base64）", response_model=ResponseSchema[None])
async def input_terminal_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_TERMINAL]))],
    session_id: Annotated[str, Path(min_length=8, max_length=64)],
    data: Annotated[TerminalInputSchema, Body(description="base64 输入")],
) -> JSONResponse:
    try:
        raw = base64.b64decode(data.data, validate=True)
    except ValueError as exc:  # binascii.Error 是 ValueError 子类：base64 非法
        from app.core.exceptions import CustomException

        raise CustomException(msg="输入内容不是合法的 base64") from exc
    TerminalManager.write(session_id, auth.user.id or 0, raw)
    return SuccessResponse(msg="输入成功")


@SshRouter.post("/terminal/{session_id}/resync", summary="重同步会话（清空积压输出）", response_model=ResponseSchema[None])
async def resync_terminal_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_TERMINAL]))],
    session_id: Annotated[str, Path(min_length=8, max_length=64)],
) -> JSONResponse:
    TerminalManager.poll(session_id, auth.user.id or 0, 0)
    return SuccessResponse(msg="已重同步")


@SshRouter.post("/terminal/{session_id}/resize", summary="同步终端尺寸", response_model=ResponseSchema[None])
async def resize_terminal_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_TERMINAL]))],
    session_id: Annotated[str, Path(min_length=8, max_length=64)],
    data: Annotated[TerminalResizeSchema, Body(description="列/行")],
) -> JSONResponse:
    TerminalManager.resize(session_id, auth.user.id or 0, data.cols, data.rows)
    return SuccessResponse(msg="尺寸已同步")


@SshRouter.delete("/terminal/{session_id}", summary="关闭终端会话", response_model=ResponseSchema[None])
async def close_terminal_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_TERMINAL]))],
    session_id: Annotated[str, Path(min_length=8, max_length=64)],
) -> JSONResponse:
    TerminalManager.close(session_id, auth.user.id or 0)
    return SuccessResponse(msg="终端会话已关闭")


# ── 批量执行 ──────────────────────────────────────────────────────────


@SshRouter.post("/batch-exec", summary="多主机批量执行命令", response_model=ResponseSchema[list[BatchExecResultSchema]])
async def batch_exec_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission([_EXEC]))],
    db: Annotated[AsyncSession, Depends(db_getter)],
    data: Annotated[BatchExecSchema, Body(description="主机列表与命令")],
) -> JSONResponse:
    results = await SshHostService(auth, db).batch_execute(
        host_ids=data.host_ids, command=data.command, timeout=data.timeout
    )
    return SuccessResponse(data=results, msg="批量执行完成")
