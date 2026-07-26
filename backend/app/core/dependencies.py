import json
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import Depends, Request
from redis.asyncio.client import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import RET, RedisInitKeyConfig
from app.config.setting import settings
from app.core.base_schema import AuthSchema, CoreUserSchema
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.redis_crud import RedisCURD
from app.core.security import OAuth2Schema, decode_access_token


async def db_getter() -> AsyncGenerator[AsyncSession, None]:
    """数据库会话 — 请求级生命周期管理。

    一个 HTTP 请求内所有 SQL 共享同一个事务：要么全成功，要么全失败。
    读操作也走这个事务（牺牲一点 MVCC 隔离换取读已写一致性）。
    """
    async with async_db_session() as session, session.begin():
        yield session


async def redis_getter(request: Request) -> Redis:
    """获取Redis连接

    参数:
    - request (Request): 请求对象

    返回:
    - Redis: Redis连接
    """
    return request.app.state.redis


async def get_current_user(
    db: AsyncSession = Depends(db_getter),
    redis: Redis = Depends(redis_getter),
    token: str = Depends(OAuth2Schema),
) -> AuthSchema:
    """获取当前用户"""
    return await _authenticate(token, db, redis)


async def _authenticate(
    token: str,
    db: AsyncSession,
    redis: Redis,
) -> AuthSchema:
    """核心认证逻辑（HTTP 与 WebSocket 共享）"""
    if not token:
        raise CustomException(msg="认证已失效", code=RET.UNAUTHORIZED.code, status_code=401)

    # 处理Bearer token
    if token.startswith("Bearer"):
        token = token.split(" ")[1]

    # 滑动模式下跳过 JWT exp 校验，由 Redis session TTL 决定实际有效期
    payload = decode_access_token(token, verify_exp=not settings.TOKEN_SLIDING_EXPIRE)
    if not payload or payload.is_refresh:
        raise CustomException(msg="非法凭证", code=RET.INVALID_CREDENTIALS.code, status_code=401)

    session_id = payload.sub
    if not session_id:
        raise CustomException(msg="认证已失效", code=RET.UNAUTHORIZED.code, status_code=401)

    raw = await RedisCURD(redis).get(f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}")
    if not raw:
        raise CustomException(msg="认证已失效", code=RET.UNAUTHORIZED.code, status_code=401)
    user_info = json.loads(raw)

    # 校验 session 数据完整性
    if not user_info.get("session_id"):
        raise CustomException(msg="认证已失效", code=RET.UNAUTHORIZED.code, status_code=401)

    # 滑动过期续期
    if settings.TOKEN_SLIDING_EXPIRE:
        ttl = await RedisCURD(redis).ttl(key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}")
        expire_seconds = settings.ACCESS_TOKEN_EXPIRE_SECONDS
        if ttl > 0 and ttl < expire_seconds // 2:
            await RedisCURD(redis).expire(
                key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}",
                expire=expire_seconds,
            )
            await RedisCURD(redis).expire(
                key=f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}",
                expire=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
            )

    username = user_info.get("user_name")
    if not username:
        raise CustomException(msg="认证已失效", code=RET.UNAUTHORIZED.code, status_code=401)

    user_status = user_info.get("user_status", 0)
    user_id = user_info.get("user_id")

    if user_status == 1:
        raise CustomException(msg="用户已被停用", code=RET.UNAUTHORIZED.code, status_code=401)

    if not user_id:
        raise CustomException(msg="认证已失效", code=RET.UNAUTHORIZED.code, status_code=401)

    from app.api.v1.module_system.user.model import UserModel

    stmt = select(UserModel).where(UserModel.id == user_id, UserModel.is_deleted == False)
    result = await db.execute(stmt)
    user_obj = result.scalars().first()
    if not user_obj:
        raise CustomException(msg="用户不存在", code=RET.NOT_FOUND.code, status_code=401)

    user = CoreUserSchema.model_validate(user_obj)
    return AuthSchema(
        user=user,
        permissions=user_info.get("permissions", []),
        menu_ids=user_info.get("menu_ids", []),
    )


class AuthPermission:
    """权限验证类"""

    def __init__(
        self,
        permissions: list[str] | None = None,
    ) -> None:
        """初始化权限验证

        参数:
        - permissions (list[str] | None): 权限标识列表。
        """
        self.permissions = permissions or []

    async def __call__(self, auth: AuthSchema = Depends(get_current_user), db: AsyncSession = Depends(db_getter)) -> AuthSchema:
        """调用权限验证

        参数:
        - auth (AuthSchema): 认证信息对象。

        返回:
        - AuthSchema: 已认证的权限信息对象。
        """
        user = auth.user
        if user.id is None or user.is_superuser:
            return auth

        if not self.permissions:
            return auth

        if "*" in self.permissions or "*:*:*" in self.permissions:
            return auth

        user_permissions = set[Any](auth.permissions)

        if not user_permissions:
            raise CustomException(msg="无权限操作", code=RET.FORBIDDEN.code, status_code=403)

        if not any(perm in user_permissions for perm in self.permissions):
            logger.error(f"用户缺少任何所需的权限: {self.permissions}")
            raise CustomException(msg="无权限操作", code=10403, status_code=403)

        return auth
