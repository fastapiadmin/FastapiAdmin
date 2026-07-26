import json
import uuid
from datetime import datetime, timedelta
from typing import Any, NewType

import ua_parser
from fastapi import BackgroundTasks, Request
from redis.asyncio.client import Redis
from sqlalchemy import update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.log.crud import LoginLogCRUD
from app.api.v1.module_system.log.model import LoginLogModel
from app.api.v1.module_system.log.schema import LoginLogCreateSchema
from app.api.v1.module_system.user.crud import UserCRUD
from app.api.v1.module_system.user.model import UserModel
from app.common.enums import RedisInitKeyConfig
from app.config.setting import settings
from app.core.base_schema import AuthSchema, JWTOutSchema, JWTPayloadSchema
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.redis_crud import RedisCURD
from app.core.security import (
    CustomOAuth2PasswordRequestForm,
    create_access_token,
    decode_access_token,
)
from app.utils.common_util import get_random_character
from app.utils.ip_local_util import IpLocalUtil, get_client_ip
from app.utils.password_util import PwdUtil

from .schema import (
    CaptchaOutSchema,
    LoginOutSchema,
)

CaptchaKey = NewType("CaptchaKey", str)
CaptchaBase64 = NewType("CaptchaBase64", str)


async def _write_login_log(
    username: str,
    status: int,
    login_ip: str | None = None,
    login_location: str | None = None,
    request_os: str | None = None,
    request_browser: str | None = None,
    msg: str | None = None,
) -> int | None:
    """写入登录日志；返回日志 ID（用于后台补全归属地）。"""
    try:
        async with async_db_session() as session, session.begin():
            _auth = AuthSchema()
            obj = await LoginLogCRUD(_auth, session).create(
                data=LoginLogCreateSchema(
                    username=username,
                    status=status,
                    login_ip=login_ip,
                    login_location=login_location,
                    request_os=request_os,
                    request_browser=request_browser,
                    msg=msg,
                ),
            )
            return obj.id if obj else None
    except Exception:
        return None


async def _async_fill_login_location(redis, login_log_id: int, ip: str | None) -> None:
    """后台异步补全登录日志的归属地。"""
    if not ip:
        return
    try:
        location = await IpLocalUtil.resolve_location_async(redis, ip)
        logger.info(f"异步解析IP归属地结果: ip={ip}, log_id={login_log_id}, location={location}")
        if location == "归属地查询中" or not location:
            return
        async with async_db_session() as session, session.begin():
            await session.execute(sa_update(LoginLogModel).where(LoginLogModel.id == login_log_id).values(login_location=location))
            logger.info(f"登录日志归属地已更新: log_id={login_log_id}, location={location}")
    except Exception as e:
        logger.warning(f"异步补全登录归属地失败: {e}")


class LoginService:
    """登录认证服务"""

    def __init__(self, auth: AuthSchema, db: AsyncSession) -> None:
        self.auth = auth
        self.db = db

    @staticmethod
    def _collect_permissions(
        user: UserModel,
    ) -> tuple[list[str], list[int]]:
        """收集用户角色下的权限和菜单 ID

        参数:
        - user (UserModel): 用户对象

        返回:
        - tuple[list[str], list[int]]: (permissions, menu_ids)
        """
        permissions: list[str] = []
        menu_ids: list[int] = []
        if not user.is_superuser and hasattr(user, "roles"):
            for role in user.roles:
                if role and role.status == 0:
                    if hasattr(role, "menus"):
                        for menu in role.menus:
                            if menu and menu.status == 0:
                                menu_ids.append(menu.id)
                                if menu.permission:
                                    permissions.append(menu.permission)
        return permissions, menu_ids

    @classmethod
    async def authenticate_user(
        cls,
        request: Request,
        background_tasks: BackgroundTasks,
        redis: Redis,
        login_form: CustomOAuth2PasswordRequestForm,
        db: AsyncSession,
    ) -> LoginOutSchema:
        """用户认证"""
        ua_result = ua_parser.parse(request.headers.get("user-agent") or "")
        request_ip = get_client_ip(request)
        login_location = await IpLocalUtil.resolve_location_for_log(redis, request_ip)
        _login_os = ua_result.os.family if ua_result.os else "Unknown"
        _login_browser = ua_result.user_agent.family if ua_result.user_agent else "Unknown"
        _login_username = login_form.username

        referer = request.headers.get("referer", "")
        request_from_docs = referer.endswith(("docs", "redoc"))

        if settings.CAPTCHA_ENABLE and not request_from_docs:
            if not login_form.captcha_key:
                raise CustomException(msg="验证码不能为空")
            # 滑块模式：slider_complete 已验证身份，此处仅校验状态
            await CaptchaService.check_captcha(
                redis=redis,
                key=login_form.captcha_key,
            )

        auth = AuthSchema()
        user = await UserCRUD(auth, db).get(username=login_form.username, preload=["roles", "roles.menus"])

        if not user:
            await _write_login_log(
                username=_login_username,
                status=2,
                login_ip=request_ip,
                login_location=login_location,
                request_os=_login_os,
                request_browser=_login_browser,
                msg="用户不存在",
            )
            raise CustomException(msg="用户不存在")

        if not PwdUtil.verify_password(plain_password=login_form.password, password_hash=user.password):
            await _write_login_log(
                username=_login_username,
                status=2,
                login_ip=request_ip,
                login_location=login_location,
                request_os=_login_os,
                request_browser=_login_browser,
                msg="账号或密码错误",
            )
            raise CustomException(msg="账号或密码错误")
        if user.status == 1:
            await _write_login_log(
                username=_login_username,
                status=2,
                login_ip=request_ip,
                login_location=login_location,
                request_os=_login_os,
                request_browser=_login_browser,
                msg="用户已被停用",
            )
            raise CustomException(msg="用户已被停用")

        await UserCRUD(auth, db).update_last_login(id=user.id)

        if not user:
            raise CustomException(msg="用户不存在")
        if not login_form.login_type:
            raise CustomException(msg="登录类型不能为空")

        token = await cls.create_token(
            request=request,
            redis=redis,
            user=user,
            login_type=login_form.login_type,
        )

        user_info = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "avatar": user.avatar,
            "is_superuser": user.is_superuser,
        }

        log_id = await _write_login_log(
            username=user.username,
            status=1,
            login_ip=request_ip,
            login_location=login_location,
            request_os=_login_os,
            request_browser=_login_browser,
            msg="登录成功",
        )
        # 登录成功后异步补全归属地，不阻塞返回
        if log_id and login_location == "归属地查询中":
            background_tasks.add_task(_async_fill_login_location, redis, log_id, request_ip)

        return LoginOutSchema(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            expires_in=token.expires_in,
            token_type=token.token_type,
            user_info=user_info,
        )

    @staticmethod
    def _build_session_dict(
        user: UserModel,
        session_id: str,
        permissions: list[str],
        menu_ids: list[int],
        request_ip: str,
        login_location: str | None,
        ua_result: Any,
        login_type: str,
    ) -> dict:
        """构建会话信息字典

        参数:
        - user (UserModel): 用户对象
        - session_id (str): 会话ID
        - permissions (list[str]): 权限标识列表
        - menu_ids (list[int]): 菜单ID列表
        - request_ip (str): 请求IP
        - login_location (str): 登录地点
        - ua_result: User-Agent 解析结果
        - login_type (str): 登录类型

        返回:
        - dict: 会话信息字典
        """
        return {
            "session_id": session_id,
            "user_id": user.id,
            "is_superuser": user.is_superuser,
            "user_status": user.status,
            "name": user.name,
            "user_name": user.username,
            "dept_id": user.dept_id,
            "mobile": user.mobile,
            "email": user.email,
            "gender": user.gender,
            "avatar": user.avatar,
            "permissions": permissions,
            "menu_ids": menu_ids,
            "ipaddr": request_ip,
            "login_location": login_location,
            "os": ua_result.os.family if ua_result.os else "Unknown",
            "browser": ua_result.user_agent.family if ua_result.user_agent else "Unknown",
            "login_time": user.last_login,
            "login_type": login_type,
        }

    @classmethod
    async def create_token(cls, request: Request, redis: Redis, user: UserModel, login_type: str) -> JWTOutSchema:
        """创建访问令牌和刷新令牌"""
        session_id = str(uuid.uuid4())
        ua_result = ua_parser.parse(request.headers.get("user-agent") or "")
        request_ip = get_client_ip(request)

        login_location = await IpLocalUtil.resolve_location_for_log(redis, request_ip)

        access_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        refresh_expires = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)

        now = datetime.now()

        permissions, menu_ids = LoginService._collect_permissions(user)

        session_dict = LoginService._build_session_dict(
            user=user,
            session_id=session_id,
            permissions=permissions,
            menu_ids=menu_ids,
            request_ip=request_ip,
            login_location=login_location,
            ua_result=ua_result,
            login_type=login_type,
        )
        session_info = json.dumps(session_dict, default=str)

        # 会话信息存 Redis（完整 JSON），JWT sub 仅含 session_id
        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}",
            value=session_info,
            expire=int(refresh_expires.total_seconds()),
        )

        access_token = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_id,
                is_refresh=False,
                exp=now + access_expires,
            ),
        )
        refresh_token = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_id,
                is_refresh=True,
                exp=now + refresh_expires,
            ),
        )

        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}",
            value=access_token,
            expire=int(access_expires.total_seconds()),
        )

        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}",
            value=refresh_token,
            expire=int(refresh_expires.total_seconds()),
        )

        return JWTOutSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(access_expires.total_seconds()),
            token_type=settings.TOKEN_TYPE,
        )

    @classmethod
    async def refresh_token(
        cls,
        db: AsyncSession,
        redis: Redis,
        refresh_token: str,
    ) -> JWTOutSchema:
        """刷新访问令牌"""
        token_payload: JWTPayloadSchema = decode_access_token(token=refresh_token)
        if not token_payload.is_refresh:
            raise CustomException(msg="非法凭证，请传入刷新令牌")

        session_id = token_payload.sub
        session_info = await RedisCURD(redis).get(f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}")
        if not session_info:
            raise CustomException(msg="会话已过期，请重新登录")

        user_id = json.loads(session_info).get("user_id")

        if not session_id or not user_id:
            raise CustomException(msg="非法凭证,无法获取会话编号或用户ID")

        auth = AuthSchema()
        user = await UserCRUD(auth, db).get(id=user_id)
        if not user:
            raise CustomException(msg="刷新token失败，用户不存在")
        if user.status == 1:
            raise CustomException(msg="用户已被停用")

        access_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        refresh_expires = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)
        now = datetime.now()

        # 延长会话信息 Redis TTL
        await RedisCURD(redis).expire(
            key=f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}",
            expire=int(refresh_expires.total_seconds()),
        )

        access_token = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_id,
                is_refresh=False,
                exp=now + access_expires,
            ),
        )

        refresh_token_new = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_id,
                is_refresh=True,
                exp=now + refresh_expires,
            ),
        )

        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}",
            value=access_token,
            expire=int(access_expires.total_seconds()),
        )

        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}",
            value=refresh_token_new,
            expire=int(refresh_expires.total_seconds()),
        )

        return JWTOutSchema(
            access_token=access_token,
            refresh_token=refresh_token_new,
            token_type=settings.TOKEN_TYPE,
            expires_in=int(access_expires.total_seconds()),
        )

    @staticmethod
    async def logout(redis: Redis, token: str) -> bool:
        """退出登录"""
        payload: JWTPayloadSchema = decode_access_token(token=token)
        session_id = payload.sub

        if not session_id:
            raise CustomException(msg="非法凭证,无法获取会话编号")

        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}")

        logger.info(f"用户退出登录成功,会话编号:{session_id}")

        return True

class CaptchaService:
    """验证码服务 — 滑块拖动模式"""

    @staticmethod
    async def get_captcha(redis: Redis) -> CaptchaOutSchema:
        """获取验证码（滑块模式：仅生成 key，无需算术图片）"""
        if not settings.CAPTCHA_ENABLE:
            raise CustomException(msg="未开启验证码服务")

        captcha_key = get_random_character()
        redis_key = f"{RedisInitKeyConfig.CAPTCHA_CODES.key}:{captcha_key}"
        # 存储滑块状态：pending（待验证）/ verified（已验证通过）
        await RedisCURD(redis).set(
            key=redis_key,
            value="pending",
            expire=settings.CAPTCHA_EXPIRE_SECONDS,
        )

        return CaptchaOutSchema(
            enable=settings.CAPTCHA_ENABLE,
            key=CaptchaKey(captcha_key),
            img_base=CaptchaBase64(""),
        )

    @staticmethod
    async def slider_complete(redis: Redis, captcha_key: str) -> dict:
        """标记滑块验证完成"""
        if not captcha_key:
            raise CustomException(msg="验证码标识不能为空")

        redis_key = f"{RedisInitKeyConfig.CAPTCHA_CODES.key}:{captcha_key}"
        status = await RedisCURD(redis).get(redis_key)
        if not status:
            raise CustomException(msg="验证码已过期，请刷新")

        if isinstance(status, bytes):
            status = status.decode()

        if status == "verified":
            raise CustomException(msg="验证码已使用")

        # 标记为已验证
        await RedisCURD(redis).set(
            key=redis_key,
            value="verified",
            expire=settings.CAPTCHA_EXPIRE_SECONDS,
        )

        return {"captcha_key": captcha_key, "verified": True}

    @staticmethod
    async def check_captcha(redis: Redis, key: str) -> bool:
        """校验滑块验证码：检查 key 状态是否为 verified"""
        redis_key = f"{RedisInitKeyConfig.CAPTCHA_CODES.key}:{key}"
        status = await RedisCURD(redis).get(redis_key)
        if not status:
            raise CustomException(msg="验证码已过期，请刷新")

        if isinstance(status, bytes):
            status = status.decode()

        if status != "verified":
            raise CustomException(msg="请先完成滑块验证")

        await RedisCURD(redis).delete(redis_key)
        return True
