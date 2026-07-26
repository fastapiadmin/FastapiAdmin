"""
认证控制器 — TODO: 限流粒度细化
---------------------------------
当前登录（/login）和 OAuth 端点（/oauth/*）共享应用的通用限流配置，
缺少独立的、更严格的限流策略。建议为以下端点配置独立的 RateLimiter：

1. /auth/login — 密码登录
   - 建议: 按 IP + 用户名组合限流，如 5次/分钟/IP + 10次/15分钟/用户
   - 原因: 暴力破解防护

2. /auth/oauth/* — 第三方 OAuth 登录/回调
   - 建议: 按 IP 限流，如 10次/分钟/IP
   - 原因: OAuth 流程可能触发多次重定向，频率稍高于登录

3. /auth/captcha/* — 验证码获取/校验
   - 建议: 按 IP 限流，如 3次/分钟/IP
   - 原因: 防止验证码遍历
"""

import json
import secrets
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import ErrorResponse, RedirectContentResponse, ResponseSchema, SuccessResponse
from app.config.setting import settings
from app.core.base_schema import JWTOutSchema
from app.core.dependencies import db_getter, get_current_user, redis_getter
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.core.redis_crud import RedisCURD
from app.core.router_class import OperationLogRoute
from app.core.security import CustomOAuth2PasswordRequestForm

from .oauth_service import (
    STATE_PREFIX,
    OAuthProvider,
    _callback_url,
    build_authorize_url,
    complete_oauth_login,
    oauth_service_error_redirect,
    oauth_service_frontend_redirect_from_token,
    save_oauth_state,
)
from .schema import (
    CaptchaOutSchema,
    LoginOutSchema,
    SliderCompleteOutSchema,
    SliderCompleteSchema,
)
from .service import (
    CaptchaService,
    LoginService,
)

AuthRouter = APIRouter(route_class=OperationLogRoute, prefix="/auth", tags=["认证授权"])


@AuthRouter.post("/login", summary="登录", response_model=LoginOutSchema)
async def login_for_access_token_controller(
    request: Request,
    background_tasks: BackgroundTasks,
    redis: Annotated[Redis, Depends(redis_getter)],
    db: Annotated[AsyncSession, Depends(db_getter)],
    login_form: Annotated[CustomOAuth2PasswordRequestForm, Depends()],
) -> JSONResponse | LoginOutSchema:
    login_result = await LoginService.authenticate_user(request=request, redis=redis, login_form=login_form, db=db, background_tasks=background_tasks)

    logger.info(f"用户{login_form.username}登录成功")

    if settings.DOCS_URL in request.headers.get("referer", ""):
        return login_result
    return SuccessResponse(data=login_result, msg="登录成功")


@AuthRouter.post("/token/refresh", summary="刷新token", response_model=ResponseSchema[JWTOutSchema])
async def get_new_token_controller(
    db: Annotated[AsyncSession, Depends(db_getter)],
    redis: Annotated[Redis, Depends(redis_getter)],
    payload: Annotated[str, Body(description="刷新token参数")],
) -> JSONResponse:
    new_token = await LoginService.refresh_token(db=db, redis=redis, refresh_token=payload)
    return SuccessResponse(data=new_token, msg="刷新成功")


@AuthRouter.get("/captcha/get", summary="获取验证码", response_model=ResponseSchema[CaptchaOutSchema])
async def get_captcha_for_login_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    captcha = await CaptchaService.get_captcha(redis=redis)
    return SuccessResponse(data=captcha, msg="获取验证码成功")


@AuthRouter.post("/captcha/slider/complete", summary="滑块验证完成", response_model=ResponseSchema[SliderCompleteOutSchema])
async def slider_complete_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    body: SliderCompleteSchema,
) -> JSONResponse:
    result = await CaptchaService.slider_complete(redis=redis, captcha_key=body.captcha_key)
    return SuccessResponse(data=result, msg="滑块验证成功")


@AuthRouter.post("/logout", summary="退出登录", response_model=ResponseSchema[None], dependencies=[Depends(get_current_user)])
async def logout_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
    payload: Annotated[str, Body(description="退出登录参数")],
) -> JSONResponse:
    if await LoginService.logout(redis=redis, token=payload):
        logger.info("退出成功")
        return SuccessResponse(msg="退出成功")
    return ErrorResponse(msg="退出失败")


@AuthRouter.get("/oauth/{provider}/login", summary="第三方OAuth跳转")
async def oauth_login_redirect_controller(
    request: Request,
    redis: Annotated[Redis, Depends(redis_getter)],
    provider: Annotated[OAuthProvider, Path(description="wechat | qq | github | gitee")],
    redirect_uri: Annotated[str | None, Query(description="OAuth 完成后浏览器回到的前端登录页完整 URL")] = None,
) -> RedirectResponse:
    allowed = {"wechat", "qq", "github", "gitee"}
    fe = redirect_uri or settings.OAUTH_FRONTEND_FALLBACK
    if provider not in allowed:
        return RedirectContentResponse(
            url=oauth_service_error_redirect(fe, "不支持的 OAuth 渠道"),
            status_code=302,
        )
    if not redirect_uri:
        return RedirectContentResponse(
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
        return RedirectContentResponse(url=url, status_code=302)
    except CustomException as e:
        return RedirectContentResponse(
            url=oauth_service_error_redirect(redirect_uri, e.msg),
            status_code=302,
        )


@AuthRouter.get("/oauth/{provider}/callback", summary="第三方OAuth回调", include_in_schema=False)
async def oauth_callback_controller(
    request: Request,
    redis: Annotated[Redis, Depends(redis_getter)],
    db: Annotated[AsyncSession, Depends(db_getter)],
    provider: Annotated[OAuthProvider, Path(description="wechat | qq | github | gitee")],
    code: Annotated[str | None, Query(description="OAuth 授权码")] = None,
    state: Annotated[str | None, Query(description="OAuth 状态参数")] = None,
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
        return RedirectContentResponse(url=url, status_code=302)
    if not code or not state:
        url = oauth_service_error_redirect(await resolve_frontend(), "授权被取消或参数不完整")
        return RedirectContentResponse(url=url, status_code=302)
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
        return RedirectContentResponse(url=success_url, status_code=302)
    except CustomException as e:
        fe = await resolve_frontend()
        return RedirectContentResponse(url=oauth_service_error_redirect(fe, e.msg), status_code=302)
