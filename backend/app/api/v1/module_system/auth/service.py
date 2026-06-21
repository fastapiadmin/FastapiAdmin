
import json
import secrets
import uuid
from datetime import datetime, timedelta
from typing import NewType

import ua_parser
from fastapi import Request
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_monitor.online.schema import OnlineOutSchema
from app.api.v1.module_system.user.crud import UserCRUD
from app.api.v1.module_system.user.model import UserModel
from app.common.enums import RedisInitKeyConfig
from app.config.setting import settings
from app.core.base_schema import (
    AuthSchema,
    JWTOutSchema,
    JWTPayloadSchema,
    LogoutPayloadSchema,
    RefreshTokenPayloadSchema,
)
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.redis_crud import RedisCURD
from app.core.security import (
    CustomOAuth2PasswordRequestForm,
    create_access_token,
    decode_access_token,
)
from app.utils.captcha_util import CaptchaUtil
from app.utils.common_util import get_random_character
from app.utils.hash_bcrpy_util import PwdUtil
from app.utils.ip_local_util import IpLocalUtil

from .schema import (
    AutoLoginTokenSchema,
    AutoLoginUserSchema,
    CaptchaOutSchema,
    LoginWithTenantsSchema,
    SelectTenantOutSchema,
    TenantOptionSchema,
    TenantRegisterOutSchema,
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
) -> None:
    """写入登录日志（独立 session，避免事务回滚时丢失失败记录）"""
    from app.api.v1.module_system.log.crud import LoginLogCRUD
    from app.api.v1.module_system.log.schema import LoginLogCreateSchema
    from app.core.base_schema import AuthSchema
    from app.core.database import async_db_session

    try:
        async with async_db_session() as session:
            async with session.begin():
                _auth = AuthSchema(db=session, check_data_scope=False)
                await LoginLogCRUD(_auth).create(data=LoginLogCreateSchema(
                    username=username,
                    status=status,
                    login_ip=login_ip,
                    login_location=login_location,
                    request_os=request_os,
                    request_browser=request_browser,
                    msg=msg,
                ))
    except Exception:
        pass  # 登录日志写入失败不影响登录主流程


def _resolve_request_ip(request: Request) -> str:
    """从请求中解析客户端真实 IP"""
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


class LoginService:
    """登录认证服务"""

    def __init__(self, auth: AuthSchema | None = None) -> None:
        self.auth = auth

    @classmethod
    async def authenticate_user(
        cls,
        request: Request,
        redis: Redis,
        login_form: CustomOAuth2PasswordRequestForm,
        db: AsyncSession,
    ) -> LoginWithTenantsSchema:
        """用户认证"""
        ua_result = ua_parser.parse(request.headers.get("user-agent"))
        request_ip = _resolve_request_ip(request)
        login_location = await IpLocalUtil.resolve_location_for_log(request_ip)
        _login_os = ua_result.os.family if ua_result.os else "Unknown"
        _login_browser = ua_result.user_agent.family if ua_result.user_agent else "Unknown"
        _login_username = login_form.username

        referer = request.headers.get("referer", "")
        request_from_docs = referer.endswith(("docs", "redoc"))

        if settings.CAPTCHA_ENABLE and not request_from_docs:
            if not login_form.captcha_key or not login_form.captcha:
                raise CustomException(msg="验证码不能为空")
            await CaptchaService.check_captcha(
                redis=redis,
                key=login_form.captcha_key,
                captcha=login_form.captcha,
            )

        auth = AuthSchema(db=db, check_data_scope=False)
        user = await UserCRUD(auth).get(username=login_form.username)

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

        from sqlalchemy import select

        from app.api.v1.module_platform.tenant.model import TenantModel

        tenant_stmt = select(TenantModel).where(TenantModel.id == user.tenant_id, TenantModel.status == 0, TenantModel.is_deleted.is_(False)).limit(1)
        tenant_result = await auth.db.execute(tenant_stmt)
        if not tenant_result.scalar_one_or_none():
            await _write_login_log(
                username=_login_username,
                status=2,
                login_ip=request_ip,
                login_location=login_location,
                request_os=_login_os,
                request_browser=_login_browser,
                msg="所属租户已被禁用",
            )
            raise CustomException(msg="所属租户已被禁用，请联系平台管理员")

        await UserCRUD(auth).update_last_login(id=user.id)

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

        tenants_auth = AuthSchema(db=db, user=user, tenant_id=user.tenant_id, check_data_scope=False)
        tenants = await LoginService(tenants_auth).get_user_tenants(user_id=user.id)

        user_info = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "avatar": user.avatar,
            "is_superuser": user.is_superuser,
        }

        await _write_login_log(
            username=user.username,
            status=1,
            login_ip=request_ip,
            login_location=login_location,
            request_os=_login_os,
            request_browser=_login_browser,
            msg="登录成功",
        )

        return LoginWithTenantsSchema(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            expires_in=token.expires_in,
            token_type=token.token_type,
            tenants=tenants,
            user_info=user_info,
        )

    @classmethod
    async def create_token(cls, request: Request, redis: Redis, user: UserModel, login_type: str) -> JWTOutSchema:
        """创建访问令牌和刷新令牌"""
        session_id = str(uuid.uuid4())
        ua_result = ua_parser.parse(request.headers.get("user-agent"))
        request_ip = _resolve_request_ip(request)

        login_location = await IpLocalUtil.resolve_location_for_log(request_ip)

        from dataclasses import replace

        from app.core.request_context import RequestContext

        base_ctx = getattr(request.state, "ctx", None) or RequestContext()
        request.state.ctx = replace(
            base_ctx,
            session_id=session_id,
            user_username=user.username,
            login_location=login_location,
        )

        access_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        now = datetime.now()

        session_info = OnlineOutSchema(
            session_id=session_id,
            user_id=user.id,
            tenant_id=user.tenant_id,
            is_superuser=user.is_superuser,
            name=user.name,
            user_name=user.username,
            ipaddr=request_ip,
            login_location=login_location,
            os=ua_result.os.family if ua_result.os else "Unknown",
            browser=ua_result.user_agent.family if ua_result.user_agent else "Unknown",
            login_time=user.last_login,
            login_type=login_type,
        ).model_dump_json()

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
            )
        )
        refresh_token = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_id,
                is_refresh=True,
                exp=now + refresh_expires,
            )
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
        refresh_token: RefreshTokenPayloadSchema,
    ) -> JWTOutSchema:
        """刷新访问令牌"""
        token_payload: JWTPayloadSchema = decode_access_token(token=refresh_token.refresh_token)
        if not token_payload.is_refresh:
            raise CustomException(msg="非法凭证，请传入刷新令牌")

        session_id = token_payload.sub
        session_info = await RedisCURD(redis).get(
            f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}"
        )
        if not session_info:
            raise CustomException(msg="会话已过期，请重新登录")

        user_id = json.loads(session_info).get("user_id")

        if not session_id or not user_id:
            raise CustomException(msg="非法凭证,无法获取会话编号或用户ID")

        auth = AuthSchema(db=db, check_data_scope=False)
        user = await UserCRUD(auth).get(id=user_id)
        if not user:
            raise CustomException(msg="刷新token失败，用户不存在")
        if user.status == 1:
            raise CustomException(msg="用户已被停用")

        access_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
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
            )
        )

        refresh_token_new = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_id,
                is_refresh=True,
                exp=now + refresh_expires,
            )
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
    async def logout(redis: Redis, token: LogoutPayloadSchema) -> bool:
        """退出登录"""
        payload: JWTPayloadSchema = decode_access_token(token=token.token)
        session_id = payload.sub

        if not session_id:
            raise CustomException(msg="非法凭证,无法获取会话编号")

        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}")

        logger.info(f"用户退出登录成功,会话编号:{session_id}")

        return True

    async def get_user_tenants(
        self,
        user_id: int | None = None,
    ) -> list[TenantOptionSchema]:
        """获取用户关联的租户列表"""
        from sqlalchemy import select

        from app.api.v1.module_platform.tenant.model import TenantModel, TenantUserModel

        uid = user_id or (self.auth.user.id if self.auth.user else None)
        if not uid:
            return []

        if self.auth.user and self.auth.user.is_superuser:
            stmt = select(TenantModel).where(TenantModel.status == 0, TenantModel.is_deleted.is_(False)).order_by(TenantModel.sort, TenantModel.id)
            result = await self.auth.db.execute(stmt)
            tenant_objs = result.scalars().all()
            return [TenantOptionSchema(id=t.id, name=t.name, code=t.code) for t in tenant_objs]

        stmt = (
            select(TenantModel)
            .join(TenantUserModel, TenantUserModel.tenant_id == TenantModel.id)
            .where(
                TenantUserModel.user_id == uid,
                TenantModel.status == 0,
                TenantModel.is_deleted.is_(False),
            )
            .order_by(TenantUserModel.is_default.desc(), TenantModel.sort, TenantModel.id)
        )
        result = await self.auth.db.execute(stmt)
        tenant_objs = result.scalars().all()
        return [TenantOptionSchema(id=t.id, name=t.name, code=t.code) for t in tenant_objs]

    async def select_tenant(
        self,
        request: Request,
        redis: Redis,
        tenant_id: int,
    ) -> SelectTenantOutSchema:
        """选择租户：验证用户归属并签发含租户上下文的新 JWT Token"""
        from sqlalchemy import select

        from app.api.v1.module_platform.tenant.model import TenantModel, TenantUserModel

        if not self.auth.user:
            raise CustomException(msg="未认证用户")

        if not self.auth.user.is_superuser:
            exist_stmt = (
                select(TenantUserModel)
                .where(
                    TenantUserModel.user_id == self.auth.user.id,
                    TenantUserModel.tenant_id == tenant_id,
                )
                .limit(1)
            )
            result = await self.auth.db.execute(exist_stmt)
            if not result.scalar_one_or_none():
                raise CustomException(msg="您不属于该租户，无法切换")

        tenant_stmt = select(TenantModel).where(TenantModel.id == tenant_id, TenantModel.status == 0).limit(1)
        result = await self.auth.db.execute(tenant_stmt)
        tenant = result.scalar_one_or_none()
        if not tenant:
            raise CustomException(msg="租户不存在或已被禁用")

        ctx = getattr(request.state, "ctx", None)
        session_id = ctx.session_id if ctx else None
        session_info = ctx.session_info if ctx else None

        if not session_id or not session_info:
            raise CustomException(msg="会话已失效")

        # 更新会话中的租户 ID 并写回 Redis
        session_info["tenant_id"] = tenant_id
        refresh_expires = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        from app.core.redis_crud import RedisCURD
        from app.core.security import create_access_token

        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}",
            value=json.dumps(session_info) if isinstance(session_info, dict) else session_info,
            expire=int(refresh_expires.total_seconds()),
        )

        access_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        now = datetime.now()

        new_access_token = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_id,
                is_refresh=False,
                exp=now + access_expires,
            )
        )

        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}",
            value=new_access_token,
            expire=int(access_expires.total_seconds()),
        )

        new_refresh_token = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_id,
                is_refresh=True,
                exp=now + refresh_expires,
            )
        )
        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}",
            value=new_refresh_token,
            expire=int(refresh_expires.total_seconds()),
        )

        from app.core.request_context import set_current_tenant

        set_current_tenant(tenant_id)

        logger.info(f"用户 {self.auth.user.username}(id={self.auth.user.id}) 切换到租户 {tenant.name}(id={tenant_id})")

        return SelectTenantOutSchema(
            access_token=new_access_token,
            token_type=settings.TOKEN_TYPE,
            expires_in=int(access_expires.total_seconds()),
        )


class CaptchaService:
    """验证码服务"""

    @staticmethod
    async def get_captcha(redis: Redis) -> CaptchaOutSchema:
        """获取验证码"""
        if not settings.CAPTCHA_ENABLE:
            raise CustomException(msg="未开启验证码服务")

        captcha_base64, captcha_value = CaptchaUtil.captcha_arithmetic()
        captcha_key = get_random_character()

        redis_key = f"{RedisInitKeyConfig.CAPTCHA_CODES.key}:{captcha_key}"
        await RedisCURD(redis).set(
            key=redis_key,
            value=captcha_value,
            expire=settings.CAPTCHA_EXPIRE_SECONDS,
        )

        return CaptchaOutSchema(
            enable=settings.CAPTCHA_ENABLE,
            key=CaptchaKey(captcha_key),
            img_base=CaptchaBase64(f"data:image/png;base64,{captcha_base64}"),
        )

    @staticmethod
    async def check_captcha(redis: Redis, key: str, captcha: str) -> bool:
        """校验验证码"""
        if not captcha:
            raise CustomException(msg="验证码不能为空")

        redis_key = f"{RedisInitKeyConfig.CAPTCHA_CODES.key}:{key}"
        captcha_value = await RedisCURD(redis).get(redis_key)
        if not captcha_value:
            raise CustomException(msg="验证码已过期")

        if captcha.lower() != captcha_value.lower():
            raise CustomException(msg="验证码错误")

        await RedisCURD(redis).delete(redis_key)
        return True


class AutoLoginService:
    """免登录服务"""

    AUTO_LOGIN_PREFIX = "fastapiadmin:auto_login:"
    TOKEN_EXPIRE = 300

    @classmethod
    async def get_auto_login_users(cls, db: AsyncSession, tenant_id: int | None = None) -> list[AutoLoginUserSchema]:
        """获取免登录用户列表"""
        from sqlalchemy import select

        from app.api.v1.module_system.user.model import UserModel

        stmt = select(UserModel).where(UserModel.status == 0)
        if tenant_id is not None:
            stmt = stmt.where(UserModel.tenant_id == tenant_id)
        stmt = stmt.order_by(UserModel.id)
        result = await db.execute(stmt)
        users = result.scalars().all()

        return [
            AutoLoginUserSchema(
                id=user.id,
                username=user.username,
                name=user.name,
                avatar=user.avatar,
            )
            for user in users
        ]

    @classmethod
    async def create_auto_login_token(
        cls,
        redis: Redis,
        db: AsyncSession,
        user_id: int,
        tenant_id: int | None = None,
    ) -> AutoLoginTokenSchema:
        """创建免登录Token"""
        from sqlalchemy import select

        from app.api.v1.module_system.user.model import UserModel

        stmt = select(UserModel).where(UserModel.id == user_id)
        if tenant_id is not None:
            stmt = stmt.where(UserModel.tenant_id == tenant_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise CustomException(msg="用户不存在")

        if user.status == 1:
            raise CustomException(msg="用户已被停用")

        import uuid

        token = str(uuid.uuid4())
        token_key = f"{cls.AUTO_LOGIN_PREFIX}{token}"

        token_data = {
            "user_id": user.id,
            "username": user.username,
            "tenant_id": user.tenant_id,
            "created_at": datetime.now().isoformat(),
        }
        await RedisCURD(redis).set(
            key=token_key,
            value=json.dumps(token_data),
            expire=cls.TOKEN_EXPIRE,
        )

        logger.info(f"创建免登录Token成功,用户:{user.username}")

        return AutoLoginTokenSchema(
            token=token,
            user=AutoLoginUserSchema(
                id=user.id,
                username=user.username,
                name=user.name,
                avatar=user.avatar,
            ),
        )

    @classmethod
    async def auto_login(
        cls,
        request: Request,
        redis: Redis,
        db: AsyncSession,
        token: str,
        tenant_id: int | None = None,
    ) -> JWTOutSchema:
        """免登录"""
        from sqlalchemy import select

        from app.api.v1.module_system.user.model import UserModel

        token_key = f"{cls.AUTO_LOGIN_PREFIX}{token}"
        token_data_str = await RedisCURD(redis).get(token_key)

        if not token_data_str:
            raise CustomException(msg="免登录Token已过期或无效")

        if isinstance(token_data_str, bytes):
            token_data_str = token_data_str.decode("utf-8")

        token_data = json.loads(token_data_str)
        user_id = token_data.get("user_id")
        token_tenant_id = token_data.get("tenant_id")

        stmt = select(UserModel).where(UserModel.id == user_id)
        effective_tenant_id = tenant_id if tenant_id is not None else token_tenant_id
        if effective_tenant_id is not None:
            stmt = stmt.where(UserModel.tenant_id == effective_tenant_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise CustomException(msg="用户不存在")

        if user.status == 1:
            raise CustomException(msg="用户已被停用")

        await RedisCURD(redis).delete(token_key)

        jwt_token = await LoginService.create_token(request=request, redis=redis, user=user, login_type="PC端")

        logger.info(f"用户{user.username}免登录成功")

        return jwt_token


class TenantRegisterService:
    """PRD §4.5 租户自助注册：一次性创建租户 + 管理员 + owner 角色 + 菜单分配"""

    DEFAULT_TRIAL_DAYS = 7

    @classmethod
    async def register(
        cls,
        db: AsyncSession,
        username: str,
        password: str,
        email: str,
        tenant_name: str | None = None,
    ) -> TenantRegisterOutSchema:
        """租户自助注册：一次性创建租户 + 管理员 + owner 角色 + 菜单分配"""
        from sqlalchemy import func, select
        from sqlalchemy.exc import IntegrityError

        from app.api.v1.module_platform.package.model import PackageMenuModel, PackageModel
        from app.api.v1.module_platform.tenant.model import TenantModel
        from app.api.v1.module_system.role.model import RoleMenusModel, RoleModel
        from app.api.v1.module_system.user.model import UserModel, UserRolesModel

        exists_stmt = (
            select(func.count())
            .select_from(UserModel)
            .where(
                UserModel.is_deleted.is_(False),
                (UserModel.username == username) | (UserModel.email == email),
            )
        )
        cnt = (await db.execute(exists_stmt)).scalar() or 0
        if cnt > 0:
            raise CustomException(msg="用户名或邮箱已被占用")

        pkg_stmt = select(PackageModel).where(PackageModel.status == 0).order_by(PackageModel.id).limit(1)
        default_pkg = (await db.execute(pkg_stmt)).scalar_one_or_none()

        now = datetime.now()
        trial_end = now + timedelta(days=cls.DEFAULT_TRIAL_DAYS)

        base = tenant_name or username
        code_suffix = base.encode("utf-8").hex()[:6].upper()
        tenant_code = f"T{code_suffix}"

        tenant = TenantModel(
            name=tenant_name or f"{username}的租户",
            code=tenant_code,
            contact_name=username,
            package_id=default_pkg.id if default_pkg else None,
            start_time=now,
            end_time=trial_end,
            status=0,
        )
        db.add(tenant)
        await db.flush()

        user = UserModel(
            username=username,
            password=PwdUtil.hash_password(password),
            email=email,
            tenant_id=tenant.id,
            status=0,
        )
        db.add(user)
        await db.flush()

        owner_role = RoleModel(
            name="租户管理员",
            code="owner",
            tenant_id=tenant.id,
            order=1,
            data_scope=4,
            description="自助注册创建的管理员角色",
        )
        db.add(owner_role)
        await db.flush()

        user_role = UserRolesModel(user_id=user.id, role_id=owner_role.id)
        db.add(user_role)

        if default_pkg:
            pkg_menu_stmt = select(PackageMenuModel).where(
                PackageMenuModel.package_id == default_pkg.id,
            )
            pkg_menus = (await db.execute(pkg_menu_stmt)).scalars().all()
            for pm in pkg_menus:
                db.add(RoleMenusModel(role_id=owner_role.id, menu_id=pm.menu_id))

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise CustomException(msg="租户编码或用户名已被占用，请重试")

        try:
            await cls._send_welcome_email(email, username, tenant.name, trial_end)
        except Exception:
            logger.warning(f"注册欢迎邮件发送失败: {email}")

        return TenantRegisterOutSchema(
            user_id=user.id,
            username=username,
            tenant_id=tenant.id,
            tenant_name=tenant.name,
            tenant_code=tenant_code,
            package=default_pkg.name if default_pkg else None,
            trial_end=trial_end.strftime("%Y-%m-%d"),
            message="注册成功",
        )

    @classmethod
    async def _send_welcome_email(cls, to_email: str, username: str, tenant_name: str, trial_end: datetime) -> None:
        """发送欢迎邮件（不阻塞注册流程）。"""
        from app.api.v1.module_platform.email.crud import EmailConfigCRUD
        from app.core.base_schema import AuthSchema
        from app.core.database import async_db_session
        from app.utils.email_util import render_template_file, send_email

        async with async_db_session() as _db:
            cfg = await EmailConfigCRUD(AuthSchema(db=_db, check_data_scope=False)).get_active_default()

        if not cfg:
            logger.info("无可用 SMTP 配置，跳过欢迎邮件")
            return

        html_body = render_template_file("emails/welcome.jinja2", {
            "tenant_name": tenant_name,
            "username": username,
            "trial_end": trial_end.strftime("%Y-%m-%d"),
        })

        await send_email(
            smtp_host=cfg.smtp_host,
            smtp_port=cfg.smtp_port,
            smtp_user=cfg.smtp_user,
            smtp_password=cfg.smtp_password,
            use_tls=cfg.use_tls,
            from_name=cfg.from_name,
            to_email=to_email,
            to_name=username,
            subject=f"欢迎加入 {tenant_name}！",
            body_html=html_body,
        )
        logger.info(f"欢迎邮件已发送至 {to_email}")


class PasswordResetService:
    """PRD §4.6 忘记密码：邮箱重置令牌 + 密码更新"""

    RESET_TOKEN_PREFIX = "pwd_reset:"
    TOKEN_EXPIRE_SECONDS = 1800  # 30 分钟

    @classmethod
    async def forgot_password(cls, redis: Redis, db: AsyncSession, email: str) -> str:
        """忘记密码：根据邮箱查找用户，生成重置令牌并尝试发送邮件。"""
        from sqlalchemy import select

        from app.api.v1.module_system.user.model import UserModel

        stmt = select(UserModel).where(
            UserModel.email == email,
            UserModel.is_deleted.is_(False),
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            logger.info(f"忘记密码：邮箱 {email} 未注册，静默返回")
            return "若邮箱已注册，重置邮件已发送"

        token = secrets.token_urlsafe(32)
        key = f"{cls.RESET_TOKEN_PREFIX}{token}"
        await RedisCURD(redis).set(key=key, value=str(user.id), expire=cls.TOKEN_EXPIRE_SECONDS)

        try:
            await cls._send_reset_email(email, user.username, token)
        except Exception:
            logger.warning(f"密码重置邮件发送失败: {email}")

        return "若邮箱已注册，重置邮件已发送"

    @classmethod
    async def reset_password_with_token(cls, redis: Redis, db: AsyncSession, token: str, new_password: str) -> str:
        """使用令牌重置密码。校验令牌 → 更新密码 → 删除令牌。"""
        from app.api.v1.module_system.user.model import UserModel

        key = f"{cls.RESET_TOKEN_PREFIX}{token}"
        user_id_str = await RedisCURD(redis).get(key)

        if not user_id_str:
            raise CustomException(msg="重置链接已失效，请重新申请")

        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError):
            await RedisCURD(redis).delete(key)
            raise CustomException(msg="无效的重置链接")

        user = await db.get(UserModel, user_id)
        if not user or user.is_deleted:
            await RedisCURD(redis).delete(key)
            raise CustomException(msg="用户不存在")

        user.password = PwdUtil.hash_password(new_password)
        await db.commit()
        await RedisCURD(redis).delete(key)

        logger.info(f"用户 {user.username}(id={user_id}) 密码已重置")
        return "密码重置成功，请使用新密码登录"

    @classmethod
    async def _send_reset_email(cls, to_email: str, username: str, token: str) -> None:
        """发送密码重置邮件。"""
        from app.api.v1.module_platform.email.crud import EmailConfigCRUD
        from app.core.base_schema import AuthSchema
        from app.core.database import async_db_session
        from app.utils.email_util import render_template_file, send_email

        async with async_db_session() as _db:
            cfg = await EmailConfigCRUD(AuthSchema(db=_db, check_data_scope=False)).get_active_default()

        if not cfg:
            logger.info("无可用 SMTP 配置，跳过重置邮件")
            return

        reset_url = f"{getattr(settings, 'SITE_URL', '')}/reset-password?token={token}"
        html_body = render_template_file("emails/reset_password.jinja2", {
            "username": username,
            "reset_url": reset_url,
            "expire_minutes": cls.TOKEN_EXPIRE_SECONDS // 60,
        })

        await send_email(
            smtp_host=cfg.smtp_host,
            smtp_port=cfg.smtp_port,
            smtp_user=cfg.smtp_user,
            smtp_password=cfg.smtp_password,
            use_tls=cfg.use_tls,
            from_name=cfg.from_name,
            to_email=to_email,
            to_name=username,
            subject="密码重置 - FastapiAdmin",
            body_html=html_body,
        )
        logger.info(f"密码重置邮件已发送至 {to_email}")
