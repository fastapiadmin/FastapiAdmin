import json
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import ErrorResponse, SuccessResponse
from app.config.setting import settings
from app.core.dependencies import db_getter, get_current_user, redis_getter
from app.core.exceptions import CustomException
from app.core.redis_crud import RedisCURD
from app.core.logger import log
from app.core.router_class import OperationLogRoute
from app.core.security import CustomOAuth2PasswordRequestForm

from .schema import (
    AutoLoginTokenSchema,
    AutoLoginUserSchema,
    CaptchaOutSchema,
    JWTOutSchema,
    LogoutPayloadSchema,
    RefreshTokenPayloadSchema,
)
from .oauth_service import (
    STATE_PREFIX,
    build_authorize_url,
    complete_oauth_login,
    oauth_service_error_redirect,
    oauth_service_frontend_redirect_from_token,
    save_oauth_state,
    _callback_url,
)
from .service import AutoLoginService, CaptchaService, LoginService

AuthRouter = APIRouter(route_class=OperationLogRoute, prefix="/auth", tags=["认证授权"])


@AuthRouter.post(
    "/login",
    summary="登录",
    description="登录",
    response_model=JWTOutSchema,
)
async def login_for_access_token_controller(
    request: Request,
    redis: Annotated[Redis, Depends(redis_getter)],
    login_form: Annotated[CustomOAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(db_getter)],
) -> JSONResponse | dict:
    """
    用户登录

    参数:
    - request (Request): FastAPI请求对象
    - redis (Redis): Redis 客户端对象
    - login_form (CustomOAuth2PasswordRequestForm): 登录表单数据
    - db (AsyncSession): 数据库会话对象

    返回:
    - JWTOutSchema: 包含访问令牌和刷新令牌的响应模型

    异常:
    - CustomException: 认证失败时抛出异常。
    """
    login_token = await LoginService.authenticate_user_service(
        request=request, redis=redis, login_form=login_form, db=db
    )

    log.info(f"用户{login_form.username}登录成功")

    # 如果是文档请求，则不记录日志:http://localhost:8000/api/v1/docs
    if settings.DOCS_URL in request.headers.get("referer", ""):
        return login_token.model_dump()
    return SuccessResponse(data=login_token.model_dump(), msg="登录成功")


@AuthRouter.post(
    "/token/refresh",
    summary="刷新token",
    description="刷新token",
    response_model=JWTOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_new_token_controller(
    request: Request,
    payload: RefreshTokenPayloadSchema,
    db: Annotated[AsyncSession, Depends(db_getter)],
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    """
    刷新token

    参数:
    - request (Request): FastAPI请求对象
    - payload (RefreshTokenPayloadSchema): 刷新令牌负载模型
    - db (AsyncSession): 数据库会话对象
    - redis (Redis): Redis 客户端对象

    返回:
    - JWTOutSchema: 包含新的访问令牌和刷新令牌的响应模型

    异常:
    - CustomException: 刷新令牌失败时抛出异常。
    """
    # 解析当前的访问Token以获取用户名
    new_token = await LoginService.refresh_token_service(
        db=db, request=request, redis=redis, refresh_token=payload
    )
    token_dict = new_token.model_dump()
    log.info(f"刷新token成功: {token_dict}")
    return SuccessResponse(data=token_dict, msg="刷新成功")


@AuthRouter.get(
    "/captcha/get",
    summary="获取验证码",
    description="获取登录验证码",
    response_model=CaptchaOutSchema,
)
async def get_captcha_for_login_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    """
    获取登录验证码

    参数:
    - redis (Redis): Redis客户端对象

    返回:
    - CaptchaOutSchema: 包含验证码图片和key的响应模型

    异常:
    - CustomException: 获取验证码失败时抛出异常。
    """
    # 获取验证码
    captcha = await CaptchaService.get_captcha_service(redis=redis)
    log.info("获取验证码成功")
    return SuccessResponse(data=captcha, msg="获取验证码成功")


@AuthRouter.post(
    "/logout",
    summary="退出登录",
    description="退出登录",
    dependencies=[Depends(get_current_user)],
)
async def logout_controller(
    payload: LogoutPayloadSchema,
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    """
    退出登录

    参数:
    - payload (LogoutPayloadSchema): 退出登录负载模型
    - redis (Redis): Redis客户端对象

    返回:
    - JSONResponse: 包含退出登录结果的响应模型

    异常:
    - CustomException: 退出登录失败时抛出异常。
    """
    if await LoginService.logout_service(redis=redis, token=payload):
        log.info("退出成功")
        return SuccessResponse(msg="退出成功")
    return ErrorResponse(msg="退出失败")


@AuthRouter.get(
    "/auto-login/users",
    summary="获取免登录用户列表",
    description="获取可用于免登录快速登录的用户列表",
    response_model=list[AutoLoginUserSchema],
)
async def get_auto_login_users_controller(
    db: Annotated[AsyncSession, Depends(db_getter)],
) -> JSONResponse:
    """
    获取免登录用户列表

    参数:
    - db (AsyncSession): 数据库会话对象

    返回:
    - list[AutoLoginUserSchema]: 免登录用户列表
    """
    users = await AutoLoginService.get_auto_login_users_service(db=db)
    return SuccessResponse(data=users, msg="获取成功")


@AuthRouter.post(
    "/auto-login/token",
    summary="获取免登录Token",
    description="根据用户ID生成免登录Token",
    response_model=AutoLoginTokenSchema,
)
async def get_auto_login_token_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    db: Annotated[AsyncSession, Depends(db_getter)],
    user_id: int,
) -> JSONResponse:
    """
    获取免登录Token

    参数:
    - redis (Redis): Redis客户端对象
    - db (AsyncSession): 数据库会话对象
    - user_id (int): 用户ID

    返回:
    - AutoLoginTokenSchema: 免登录Token和用户信息
    """
    result = await AutoLoginService.create_auto_login_token_service(
        redis=redis, db=db, user_id=user_id
    )
    return SuccessResponse(data=result, msg="获取成功")


@AuthRouter.post(
    "/auto-login",
    summary="免登录",
    description="使用免登录Token快速登录",
    response_model=JWTOutSchema,
)
async def auto_login_controller(
    request: Request,
    redis: Annotated[Redis, Depends(redis_getter)],
    db: Annotated[AsyncSession, Depends(db_getter)],
    token: str,
) -> JSONResponse:
    """
    免登录

    参数:
    - request (Request): FastAPI请求对象
    - redis (Redis): Redis客户端对象
    - db (AsyncSession): 数据库会话对象
    - token (str): 免登录Token

    返回:
    - JWTOutSchema: JWT令牌信息
    """
    login_token = await AutoLoginService.auto_login_service(
        request=request, redis=redis, db=db, token=token
    )
    log.info("用户免登录成功")
    return SuccessResponse(data=login_token.model_dump(), msg="登录成功")


@AuthRouter.get(
    "/oauth/{provider}/login",
    summary="第三方OAuth跳转",
    description="浏览器重定向到微信/GitHub/Gitee/QQ 授权页；redirect_uri 为授权完成后回到前端的登录页地址（如 http://localhost:5173/login）。",
)
async def oauth_login_redirect_controller(
    request: Request,
    redis: Annotated[Redis, Depends(redis_getter)],
    provider: Annotated[str, Path(description="wechat | qq | github | gitee")],
    redirect_uri: Annotated[
        str | None,
        Query(description="OAuth 完成后浏览器回到的前端登录页完整 URL"),
    ] = None,
) -> RedirectResponse:
    allowed = {"wechat", "qq", "github", "gitee"}
    fe = redirect_uri or settings.OAUTH_FRONTEND_FALLBACK
    if provider not in allowed:
        return RedirectResponse(
            url=oauth_service_error_redirect(fe, "不支持的 OAuth 渠道"),
            status_code=302,
        )
    if not redirect_uri:
        return RedirectResponse(
            url=oauth_service_error_redirect(fe, "缺少 redirect_uri 参数"),
            status_code=302,
        )
    try:
        state = secrets.token_urlsafe(32)
        await save_oauth_state(
            redis=redis,
            state=state,
            provider=provider,
            frontend_redirect=redirect_uri,
        )
        cb = _callback_url(request, provider)
        url = build_authorize_url(provider=provider, callback_url=cb, state=state)
        return RedirectResponse(url=url, status_code=302)
    except CustomException as e:
        return RedirectResponse(
            url=oauth_service_error_redirect(redirect_uri, e.msg),
            status_code=302,
        )


@AuthRouter.get(
    "/oauth/{provider}/callback",
    summary="第三方OAuth回调",
    include_in_schema=False,
)
async def oauth_callback_controller(
    request: Request,
    redis: Annotated[Redis, Depends(redis_getter)],
    db: Annotated[AsyncSession, Depends(db_getter)],
    provider: Annotated[str, Path()],
    code: Annotated[str | None, Query()] = None,
    state: Annotated[str | None, Query()] = None,
) -> RedirectResponse:
    fe_fallback = settings.OAUTH_FRONTEND_FALLBACK

    async def resolve_frontend() -> str:
        if not state:
            return fe_fallback
        raw = await RedisCURD(redis).get(f"{STATE_PREFIX}{state}")
        if not raw:
            return fe_fallback
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        try:
            payload = json.loads(raw)
            return str(payload.get("frontend_redirect") or fe_fallback).strip() or fe_fallback
        except json.JSONDecodeError:
            return fe_fallback

    if provider not in {"wechat", "qq", "github", "gitee"}:
        url = oauth_service_error_redirect(await resolve_frontend(), "不支持的 OAuth 渠道")
        return RedirectResponse(url=url, status_code=302)
    if not code or not state:
        url = oauth_service_error_redirect(
            await resolve_frontend(), "授权被取消或参数不完整"
        )
        return RedirectResponse(url=url, status_code=302)
    try:
        token, fe = await complete_oauth_login(
            request=request,
            redis=redis,
            db=db,
            provider=provider,
            code=code,
            state=state,
        )
        success_url = oauth_service_frontend_redirect_from_token(fe, token)
        return RedirectResponse(url=success_url, status_code=302)
    except CustomException as e:
        fe = await resolve_frontend()
        return RedirectResponse(url=oauth_service_error_redirect(fe, e.msg), status_code=302)
