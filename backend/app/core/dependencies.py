# -*- coding: utf-8 -*-

import json
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import AsyncGenerator
from fastapi import Depends, Request
from fastapi import Depends

from app.common.enums import RedisInitKeyConfig
from app.core.exceptions import CustomException
from app.core.database import async_db_session
from app.core.redis_crud import RedisCURD
from app.core.security import OAuth2Schema, decode_access_token
from app.core.logger import log

from app.api.v1.module_system.user.model import UserModel
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.user.crud import UserCRUD
from app.api.v1.module_system.auth.schema import AuthSchema


async def db_getter() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话连接
    
    返回:
    - AsyncSession: 数据库会话连接
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

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(db_getter),
    redis: Redis = Depends(redis_getter),
    token: str = Depends(OAuth2Schema),
) -> AuthSchema:
    """获取当前用户
    
    参数:
    - request (Request): 请求对象
    - db (AsyncSession): 数据库会话
    - redis (Redis): Redis连接
    - token (str): 访问令牌
    
    返回:
    - AuthSchema: 认证信息模型
    """
    if not token:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)
    
    # 处理Bearer token
    if token.startswith('Bearer'):
        token = token.split(' ')[1]

    payload = decode_access_token(token)
    if not payload or not hasattr(payload, 'is_refresh') or payload.is_refresh:
        raise CustomException(msg="非法凭证", code=10401, status_code=401)
        
    online_user_info = payload.sub
    # 从Redis中获取用户信息
    user_info = json.loads(online_user_info)  # 确保是字典类型
    
    session_id = user_info.get("session_id")
    if not session_id:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)

    # 检查用户是否在线
    online_ok = await RedisCURD(redis).exists(key=f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}')
    if not online_ok:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)

    # 关闭数据权限过滤，避免当前用户查询被拦截
    auth = AuthSchema(db=db, check_data_scope=False)
    username = user_info.get("user_name")
    if not username:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)
    # 获取用户信息，使用深层预加载确保RoleModel.creator被正确加载
    user = await UserCRUD(auth).get_by_username_crud(
        username=username, 
        preload=[
            "dept", 
            selectinload(UserModel.roles).selectinload(RoleModel.created_by),
            "positions", 
            "created_by"
        ]
    )
    if not user:
        raise CustomException(msg="用户不存在", code=10401, status_code=401)
    if not user.status:
        raise CustomException(msg="用户已被停用", code=10401, status_code=401)
    
    # 设置请求上下文
    request.scope["user_id"] = user.id
    request.scope["user_username"] = user.username
    
    # 过滤可用的角色和职位
    if hasattr(user, 'roles'):
        user.roles = [role for role in user.roles if role and role.status]
    if hasattr(user, 'positions'):
        user.positions = [pos for pos in user.positions if pos and pos.status]

    auth.user = user
    return auth


class AuthPermission:
    """权限验证类"""
    
    def __init__(self, permissions: list[str] | None = None, check_data_scope: bool = True) -> None:
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
        auth.check_data_scope = self.check_data_scope

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
        
        # 获取用户权限集合
        user_permissions = {
            menu.permission 
            for role in auth.user.roles
            for menu in role.menus 
            if role.status and menu.permission and menu.status
        }

        # 权限验证 - 满足任一权限即可
        if not any(perm in user_permissions for perm in self.permissions):
            log.error(f"用户缺少任何所需的权限: {self.permissions}")
            raise CustomException(msg="无权限操作", code=10403, status_code=403)

        return auth
