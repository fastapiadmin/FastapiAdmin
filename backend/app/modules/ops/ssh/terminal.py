"""SSH 终端会话管理（进程内、**POST 轮询**、不依赖 WebSocket）。

为什么用 POST 轮询：Web 端已有一条 WebSocket 聊天连接，终端再开一条 WS 会多一套握手/鉴权分支；
轮询在局域网/内网管理场景足够（延迟 ~200ms），实现与排障都更简单（FastHub 也采用同样取舍）。

资源与安全：
- 会话归创建者所有（跨用户访问返回 403）；
- 单用户最多 3 个、全局最多 50 个；空闲 30 分钟自动回收；
- 主机凭据只在建连时解密使用，不存入会话对象；
- 读取线程只做一件事：把通道输出塞进无界队列（单会话输出量由终端自身流量决定）。
"""

import queue
import threading
import time
import uuid
from dataclasses import dataclass, field

import paramiko

from app.common.enums import RET
from app.core.exceptions import CustomException
from app.core.logger import logger

MAX_SESSIONS_PER_USER = 3
MAX_SESSIONS_TOTAL = 50
IDLE_TIMEOUT = 30 * 60
_READ_CHUNK = 4096
_POLL_INTERVAL = 0.15


@dataclass
class TerminalSession:
    """一个交互终端会话"""

    session_id: str
    user_id: int
    host_id: int
    host_name: str
    client: paramiko.SSHClient
    channel: paramiko.Channel
    cols: int
    rows: int
    created_at: float
    last_active: float
    output: "queue.Queue[bytes]" = field(default_factory=queue.Queue)
    closed: bool = False
    exit_status: int | None = None


class TerminalManager:
    """进程内终端会话表（单进程假设：多 worker 部署时会话仅落在处理请求的进程）。"""

    _sessions: dict[str, TerminalSession] = {}

    @classmethod
    def _close_impl(cls, session_id: str) -> None:
        sess = cls._sessions.pop(session_id, None)
        if sess is None:
            return
        sess.closed = True
        for closer in (sess.channel.close, sess.client.close):
            try:
                closer()
            except Exception:  # noqa: BLE001 - 关闭失败不影响后续清理
                continue

    @classmethod
    def _reap(cls) -> None:
        now = time.monotonic()
        for session_id, sess in list(cls._sessions.items()):
            if sess.closed or now - sess.last_active > IDLE_TIMEOUT:
                logger.info(f"回收终端会话: {session_id}（closed={sess.closed}）")
                cls._close_impl(session_id)

    @classmethod
    def open(
        cls,
        *,
        user_id: int,
        host_id: int,
        host_name: str,
        client: paramiko.SSHClient,
        channel: paramiko.Channel,
        cols: int,
        rows: int,
    ) -> TerminalSession:
        """登记一个已建连的终端会话并启动读取线程。"""
        cls._reap()
        owned = [item for item in cls._sessions.values() if item.user_id == user_id]
        if len(owned) >= MAX_SESSIONS_PER_USER:
            raise CustomException(msg=f"单用户最多同时打开 {MAX_SESSIONS_PER_USER} 个终端会话，请先关闭空闲会话")
        if len(cls._sessions) >= MAX_SESSIONS_TOTAL:
            raise CustomException(msg="终端会话数已达上限，请稍后再试")

        session_id = uuid.uuid4().hex
        now = time.monotonic()
        sess = TerminalSession(
            session_id=session_id,
            user_id=user_id,
            host_id=host_id,
            host_name=host_name,
            client=client,
            channel=channel,
            cols=cols,
            rows=rows,
            created_at=now,
            last_active=now,
        )
        try:
            channel.settimeout(0.0)
        except Exception:  # noqa: BLE001 - 部分通道不支持 settimeout
            pass
        threading.Thread(target=cls._reader, args=(sess,), daemon=True).start()
        cls._sessions[session_id] = sess
        return sess

    @staticmethod
    def _reader(sess: TerminalSession) -> None:
        """读取线程：把通道输出塞进队列；通道结束即标记 closed。"""
        while not sess.closed:
            try:
                data = sess.channel.recv(_READ_CHUNK)
            except (TimeoutError, BlockingIOError):
                # 通道为 setblocking(False)：无数据时抛超时/阻塞异常，不能当作 EOF
                time.sleep(_POLL_INTERVAL)
                continue
            except Exception:  # noqa: BLE001 - 通道关闭视为结束
                break
            if not data:
                break
            sess.output.put(data)
        sess.closed = True
        try:
            sess.exit_status = sess.channel.recv_exit_status()
        except Exception:  # noqa: BLE001 - 已关闭时拿不到退出码
            sess.exit_status = None

    @classmethod
    def get(cls, session_id: str, user_id: int) -> TerminalSession:
        """取会话并做归属校验（非本人 403）。"""
        sess = cls._sessions.get(session_id)
        if sess is None or sess.closed:
            raise CustomException(msg="终端会话不存在或已关闭")
        if sess.user_id != user_id:
            raise CustomException(msg="无权访问该终端会话", code=RET.FORBIDDEN.code)
        sess.last_active = time.monotonic()
        return sess

    @classmethod
    def poll(cls, session_id: str, user_id: int, timeout: float = 2.0) -> tuple[bytes, bool, int | None]:
        """长轮询：最多等 timeout 秒，返回累计输出。"""
        sess = cls.get(session_id, user_id)
        chunks: list[bytes] = []
        deadline = time.monotonic() + max(0.0, min(timeout, 5.0))
        while True:
            while True:
                try:
                    chunks.append(sess.output.get_nowait())
                except queue.Empty:
                    break
            if chunks or sess.closed or time.monotonic() >= deadline:
                break
            time.sleep(_POLL_INTERVAL)
        return b"".join(chunks), sess.closed, sess.exit_status

    @classmethod
    def write(cls, session_id: str, user_id: int, data: bytes) -> None:
        sess = cls.get(session_id, user_id)
        try:
            sess.channel.sendall(data)
        except CustomException:
            raise
        except Exception as exc:  # noqa: BLE001 - 通道关闭时统一转业务异常
            raise CustomException(msg=f"终端写入失败: {type(exc).__name__}") from exc

    @classmethod
    def resize(cls, session_id: str, user_id: int, cols: int, rows: int) -> None:
        sess = cls.get(session_id, user_id)
        try:
            sess.channel.resize_pty(width=cols, height=rows)
            sess.cols, sess.rows = cols, rows
        except CustomException:
            raise
        except Exception as exc:  # noqa: BLE001
            raise CustomException(msg=f"终端尺寸同步失败: {type(exc).__name__}") from exc

    @classmethod
    def close(cls, session_id: str, user_id: int | None = None) -> None:
        """关闭会话；传 user_id 时校验归属（内部回收不传）。"""
        if user_id is not None:
            cls.get(session_id, user_id)
        cls._close_impl(session_id)

    @classmethod
    def count(cls) -> int:
        return len(cls._sessions)
