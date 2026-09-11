import dataclasses
from datetime import datetime

from fastapi import Response


@dataclasses.dataclass
class UserAgentInfo:
    """User-Agent 解析结果（操作系统、浏览器、设备）。"""

    user_agent: str
    os: str | None
    browser: str | None
    device: str | None


@dataclasses.dataclass
class RequestCallNext:
    """请求链路 call_next 封装结果（状态码、消息、异常、响应）。"""

    code: str
    msg: str
    err: Exception | None
    response: Response


@dataclasses.dataclass
class AccessToken:
    """访问令牌及过期时间、会话 UUID。"""

    access_token: str
    access_token_expire_time: datetime
    session_uuid: str


@dataclasses.dataclass
class RefreshToken:
    """刷新令牌及过期时间。"""

    refresh_token: str
    refresh_token_expire_time: datetime


@dataclasses.dataclass
class NewToken:
    """刷新后的一对访问/刷新令牌及会话 UUID。"""

    new_access_token: str
    new_access_token_expire_time: datetime
    new_refresh_token: str
    new_refresh_token_expire_time: datetime
    session_uuid: str


@dataclasses.dataclass
class TokenPayload:
    """JWT/会话载荷中的用户与会话标识。"""

    id: int
    session_uuid: str
    expire_time: datetime


@dataclasses.dataclass
class UploadUrl:
    """上传完成后的访问 URL。"""

    url: str


@dataclasses.dataclass
class SnowflakeInfo:
    """雪花 ID 拆解后的各段信息。"""

    timestamp: int
    datetime: str
    cluster_id: int
    node_id: int
    sequence: int
