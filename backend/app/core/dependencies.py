import json
import time
from collections.abc import AsyncGenerator
from dataclasses import replace

from fastapi import Depends, Query, Request
from redis.asyncio.client import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.common.enums import RedisInitKeyConfig
from app.config.setting import settings
from app.core.base_schema import AuthSchema
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.redis_crud import RedisCURD
from app.core.request_context import RequestContext
from app.core.request_context import get_current_tenant_id as _get_ctx_tenant_id
from app.core.security import OAuth2Schema, decode_access_token

# 套餐菜单权限缓存: {tenant_id: (timestamp, [menu_ids])}
_package_menu_cache: dict[int, tuple[float, list[int]]] = {}


async def db_getter() -> AsyncGenerator[AsyncSession, None]:
    """数据库会话 — 请求级生命周期管理。

    一个 HTTP 请求内所有 SQL 共享同一个事务：要么全成功，要么全失败。
    读操作也走这个事务（牺牲一点 MVCC 隔离换取读已写一致性）。
    """
    async with async_db_session() as session:
        async with session.begin():
            yield session


async def redis_getter(request: Request) -> Redis:
    """获取Redis连接

    参数:
    - request (Request): 请求对象

    返回:
    - Redis: Redis连接
    """
    return request.app.state.redis


async def get_current_tenant_id() -> int | None:
    """获取当前请求的租户 ID 依赖注入函数。

    从 ContextVar 中读取租户 ID（由 TenantMiddleware 设置）。
    非认证路径（白名单）返回 None。

    返回:
        int | None: 当前租户 ID，未设置时返回 None。
    """
    return _get_ctx_tenant_id()

async def _decode_token_info(token: str, redis: Redis) -> tuple[dict, str]:
    """解码 JWT token 返回 (user_info, session_id)

    JWT sub 现为纯 session_id，完整会话信息从 Redis 读取。

    参数:
        token: JWT token 字符串
        redis: Redis 连接

    返回:
        (user_info, session_id): 用户信息字典和会话 ID
    """
    payload = decode_access_token(token)
    if not payload or not hasattr(payload, "is_refresh") or payload.is_refresh:
        raise CustomException(msg="非法凭证", code=10401, status_code=401)

    session_id = payload.sub
    raw = await RedisCURD(redis).get(
        f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}"
    )
    if not raw:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)

    user_info = json.loads(raw)
    if not session_id:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)

    return user_info, session_id


async def _check_token_online(redis: Redis, session_id: str) -> None:
    """检查 token 是否在线（Redis 中存在对应 session）

    参数:
        redis: Redis 连接
        session_id: 会话 ID
    """
    online_ok = await RedisCURD(redis).exists(
        key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}"
    )
    if not online_ok:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)


async def _try_sliding_refresh(redis: Redis, session_id: str) -> None:
    """滑动过期续期（仅在 token 剩余不足一半时触发）

    参数:
        redis: Redis 连接
        session_id: 会话 ID
    """
    if not settings.TOKEN_SLIDING_EXPIRE:
        return

    ttl = await RedisCURD(redis).ttl(
        key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}"
    )
    if ttl > 0 and ttl < settings.ACCESS_TOKEN_EXPIRE_MINUTES // 2:
        await RedisCURD(redis).expire(
            key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}",
            expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        await RedisCURD(redis).expire(
            key=f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}",
            expire=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )

async def _load_user_from_db(db: AsyncSession, username: str):
    """从数据库加载用户（含角色、菜单、部门、职位全量预加载）

    使用原始查询以绕过 CRUDBase 的权限过滤，确保用户认证阶段不受数据权限影响。
    所有关系链均 eager-loaded，调用方可在会话关闭后安全访问对象属性。

    参数:
        db: 数据库会话
        username: 用户名

    返回:
        UserModel: 已全量加载的用户 ORM 对象
    """
    from app.api.v1.module_system.role.model import RoleModel
    from app.api.v1.module_system.user.model import UserModel

    stmt = (
        select(UserModel)
        .options(
            selectinload(UserModel.dept),
            selectinload(UserModel.roles).selectinload(RoleModel.menus),
            selectinload(UserModel.positions),
            selectinload(UserModel.created_by),
        )
        .where(UserModel.username == username, UserModel.is_deleted == False)  # noqa: E712
    )
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise CustomException(msg="用户不存在", code=10401, status_code=401)
    if user.status == 1:
        raise CustomException(msg="用户已被停用", code=10401, status_code=401)

    # 过滤不可用的角色和职位（在会话内完成，确保关联数据已加载）
    if hasattr(user, "roles"):
        user.roles = [role for role in user.roles if role and role.status]
    if hasattr(user, "positions"):
        user.positions = [pos for pos in user.positions if pos and pos.status]

    return user

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(db_getter),
    redis: Redis = Depends(redis_getter),
    token: str = Depends(OAuth2Schema),
) -> AuthSchema:
    """获取当前用户

    用户查询使用独立的只读数据库会话（不参与请求事务，查询完成后立即释放快照），
    返回的 auth.db 指向请求级事务会话供后续写操作使用。

    参数:
    - request (Request): 请求对象
    - db (AsyncSession): 请求级事务会话
    - redis (Redis): Redis连接
    - token (str): 访问令牌

    返回:
    - AuthSchema: 认证信息模型
    """
    if not token:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)

    # 处理Bearer token
    if token.startswith("Bearer"):
        token = token.split(" ")[1]

    # 优先使用 TenantMiddleware 缓存在 request.state.ctx 中的会话信息（避免重复 Redis 读取）
    ctx = getattr(request.state, "ctx", None)
    cached_user_info = ctx.jwt_user_info if ctx else None

    if cached_user_info:
        user_info = cached_user_info
    else:
        # 降级路径：自行从 Redis 读取会话信息
        user_info, _ = await _decode_token_info(token, redis)

    session_id = user_info.get("session_id")
    if not session_id:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)

    # Redis 在线检查 + 滑动续期
    await _check_token_online(redis, session_id)
    await _try_sliding_refresh(redis, session_id)

    username = user_info.get("user_name")
    if not username:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)
    tenant_id = user_info.get("tenant_id")

    # 用户查询使用独立只读会话（不参与请求事务，查询后立即释放快照）
    async with async_db_session() as lookup_db:
        user = await _load_user_from_db(lookup_db, username)

    # 设置请求上下文（仅在当前 request 对象上，业务方通过 request.state.ctx 读取）
    request.state.ctx = replace(
        (getattr(request.state, "ctx", None) or RequestContext()),
        user_id=user.id,
        user_username=user.username,
        session_id=session_id,
        session_info=user_info,
    )

    # 返回的 auth.db 指向请求级事务会话，供后续读写操作使用
    auth = AuthSchema(db=db, tenant_id=tenant_id, check_data_scope=False)
    auth.user = user
    return auth


async def get_current_user_ws(
    token: str = Query(..., description="认证token"),
    db: AsyncSession = Depends(db_getter),
    redis: Redis = Depends(redis_getter),
) -> AuthSchema:
    """获取当前用户（WebSocket专用，从查询参数获取token）

    参数:
    - token (str): 认证token
    - db (AsyncSession): 数据库会话
    - redis (Redis): Redis连接

    返回:
    - AuthSchema: 认证信息模型
    """
    return await _verify_token(token, db, redis)


async def _verify_token(
    token: str,
    db: AsyncSession,
    redis: Redis,
) -> AuthSchema:
    """验证token并返回用户信息（共享核心逻辑）

    参数:
    - token (str): 认证token
    - db (AsyncSession): 数据库会话
    - redis (Redis): Redis连接

    返回:
    - AuthSchema: 认证信息模型
    """
    if not token:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)

    # 处理Bearer token（如果通过查询参数传递时包含Bearer前缀）
    if token.startswith("Bearer"):
        token = token.split(" ")[1]

    user_info, session_id = await _decode_token_info(token, redis)
    await _check_token_online(redis, session_id)
    await _try_sliding_refresh(redis, session_id)

    username = user_info.get("user_name")
    if not username:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)
    tenant_id = user_info.get("tenant_id")

    user = await _load_user_from_db(db, username)

    auth = AuthSchema(db=db, tenant_id=tenant_id, check_data_scope=False)
    auth.user = user
    return auth

async def _get_cached_tenant_menu_ids(auth: AuthSchema, tenant_id: int) -> list[int]:
    """获取租户可用菜单 ID，带 60s 进程级缓存

    套餐菜单变更频率极低，缓存可大幅减少 AuthPermission 的 DB 查询次数。

    参数:
        auth: 认证信息
        tenant_id: 租户 ID

    返回:
        可用菜单 ID 列表
    """
    cached = _package_menu_cache.get(tenant_id)
    if cached and time.time() - cached[0] < 60:
        return cached[1]

    from app.api.v1.module_platform.package.service import PackageService

    result = await PackageService.get_tenant_available_menu_ids(auth, tenant_id)
    _package_menu_cache[tenant_id] = (time.time(), result)
    return result


class AuthPermission:
    """权限验证类"""

    def __init__(
        self,
        permissions: list[str] | None = None,
        check_data_scope: bool = True,
    ) -> None:
        """
        初始化权限验证

        参数:
        - permissions (list[str] | None): 权限标识列表。
        - check_data_scope (bool): 是否启用严格模式校验。
        """
        self.permissions = permissions or []
        self.check_data_scope = check_data_scope

    async def __call__(self, auth: AuthSchema = Depends(get_current_user)) -> AuthSchema:
        """
        调用权限验证

        参数:
        - auth (AuthSchema): 认证信息对象。

        返回:
        - AuthSchema: 认证信息对象。
        """
        # 用 model_copy 派生一份带正确 check_data_scope 的新实例（不修改原实例）
        auth = auth.model_copy(update={"check_data_scope": self.check_data_scope})

        # 超级管理员直接通过
        if auth.user and auth.user.is_superuser:
            return auth

        # 无需验证权限
        if not self.permissions:
            return auth

        # 超级管理员权限标识
        if "*" in self.permissions or "*:*:*" in self.permissions:
            return auth

        # 检查用户是否有角色
        if not auth.user or not auth.user.roles:
            raise CustomException(msg="无权限操作", code=10403, status_code=403)

        # 收集角色权限（附带 menu_id 用于套餐过滤）
        role_perms: dict[str, int] = {}
        for role in auth.user.roles:
            if role.status != 0:
                continue
            for menu in role.menus:
                if menu.status == 0 and menu.permission:
                    role_perms[menu.permission] = menu.id

        if not role_perms:
            raise CustomException(msg="无权限操作", code=10403, status_code=403)

        # 租户用户：权限必须受套餐菜单约束（带 60s 进程级缓存）
        if auth.tenant_id:
            allowed_ids = set(await _get_cached_tenant_menu_ids(auth, auth.tenant_id))
            user_permissions = {p for p, mid in role_perms.items() if mid in allowed_ids}
        else:
            user_permissions = set(role_perms.keys())

        # 权限验证 - 满足任一权限即可
        if not any(perm in user_permissions for perm in self.permissions):
            logger.error(f"用户缺少任何所需的权限: {self.permissions}")
            raise CustomException(msg="无权限操作", code=10403, status_code=403)

        return auth


def require_superadmin(func):
    """
    装饰器：仅超级管理员可调用 Service 方法。

    自动校验 ``self.auth.user.is_superuser`` 属性，非超管直接抛出 403。
    适用于实例方法（``Service(auth).xxx(...)``），由 ``self.auth`` 取认证上下文。

    用法:
        class XxxService:
            def __init__(self, auth: AuthSchema) -> None:
                self.auth = auth

            @require_superadmin
            async def create(self, data: ...) -> ...:
                ...
    """
    from functools import wraps

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self.auth.user or not self.auth.user.is_superuser:
            raise CustomException(msg="仅平台管理员可操作")
        return await func(self, *args, **kwargs)

    return wrapper
