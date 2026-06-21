from collections.abc import AsyncGenerator
from typing import Any

from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter, WebSocketRateLimiter

from app.core import cache_util

from .config.setting import settings
from .core.exceptions import handle_exception
from .core.http_limit import http_limit_callback, ws_limit_callback
from .core.logger import logger
from .scripts.initialize import InitializeData
from .utils.common_util import import_module, import_modules_async
from .utils.console import console_end, console_start


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    from app.api.v1.module_platform.tenant.service import TenantService
    from app.api.v1.module_system.dict.service import DictDataService
    from app.api.v1.module_system.params.service import ParamsService
    from app.core.ap_scheduler import SchedulerUtil

    try:
        await InitializeData().init_db()
        logger.info("✅ {}数据库初始化完成", settings.DATABASE_TYPE)
        await import_modules_async(modules=settings.EVENT_LIST, desc="全局事件", app=app, status=True)
        logger.info("✅ 全局事件模块加载完成")
        await ParamsService.init_cache(redis=app.state.redis)
        logger.info("✅ Redis系统参数初始化完成")
        await DictDataService.init_cache(redis=app.state.redis)
        logger.info("✅ Redis数据字典初始化完成")
        await TenantService.init_cache(redis=app.state.redis)
        logger.info("✅ Redis租户配置初始化完成")
        await SchedulerUtil.init_scheduler(redis=app.state.redis)
        logger.info("✅ 定时任务调度器初始化完成")
        await cache_util.init(redis=app.state.redis)
        logger.info("✅ fastapi-admin-cache 初始化完成")
        await FastAPILimiter.init(
            redis=app.state.redis,
            prefix=settings.REQUEST_LIMITER_REDIS_PREFIX,
            http_callback=http_limit_callback,
            ws_callback=ws_limit_callback,
        )
        logger.info("✅ 请求限流器初始化完成")

        console_start(
            host=settings.SERVER_HOST, port=settings.SERVER_PORT,
            reload=settings.ENVIRONMENT,
            database_ready=True, redis_ready=True,
            scheduler_ready=SchedulerUtil.is_running(), limiter_ready=True,
        )
    except Exception as e:
        logger.error("❌ 应用初始化失败: {}", e)
        raise SystemExit(1)

    yield

    try:
        await SchedulerUtil.shutdown(wait=True)
        logger.info("✅ 定时任务调度器已关闭")
        await cache_util.clear()
        logger.info("✅ fastapi-admin-cache 已关闭")
        await FastAPILimiter.close()
        logger.info("✅ 请求限制器已关闭")
        await import_modules_async(modules=settings.EVENT_LIST, desc="全局事件", app=app, status=False)
        logger.info("✅ 全局事件模块卸载完成")
        from app.core.database import async_engine
        await async_engine.dispose()
        logger.info("✅ 数据库引擎连接池已释放")
        console_end()
    except Exception as e:
        logger.error("❌ 应用关闭过程中发生错误: {}", e)
        raise SystemExit(1)


def register_middlewares(app: FastAPI) -> None:
    for middleware in settings.MIDDLEWARE_LIST[::-1]:
        if not middleware:
            continue
        middleware = import_module(middleware, desc="中间件")
        app.add_middleware(middleware)


def register_exceptions(app: FastAPI) -> None:
    handle_exception(app)


def register_routers(app: FastAPI) -> None:
    from app.api.v1.module_common import common_router
    from app.api.v1.module_monitor import monitor_router
    from app.api.v1.module_platform import platform_router
    from app.api.v1.module_system import system_router

    app.include_router(common_router, dependencies=[Depends(RateLimiter(times=200, seconds=10))])
    app.include_router(monitor_router, dependencies=[Depends(RateLimiter(times=200, seconds=10))])
    app.include_router(platform_router, dependencies=[Depends(RateLimiter(times=200, seconds=10))])
    app.include_router(system_router, dependencies=[Depends(RateLimiter(times=200, seconds=10))])

    from app.plugin.module_ai.chat.ws import WS_AI
    app.include_router(router=WS_AI, dependencies=[Depends(WebSocketRateLimiter(times=200, seconds=10))])
    
    from app.core.discover import get_dynamic_router, set_app_ref
    app.include_router(router=get_dynamic_router(), dependencies=[Depends(RateLimiter(times=200, seconds=10))])
    set_app_ref(app)

def register_files(app: FastAPI) -> None:
    if settings.STATIC_ENABLE:
        settings.STATIC_ROOT.mkdir(parents=True, exist_ok=True)
        app.mount(path=settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT), name=settings.STATIC_DIR)


def reset_api_docs(app: FastAPI) -> None:
    swagger_ui_redirect_url = str(app.swagger_ui_oauth2_redirect_url)
    root_openapi_url = str(app.root_path) + str(app.openapi_url)

    @app.get(swagger_ui_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(settings.DOCS_URL, include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=root_openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=settings.SWAGGER_JS_URL,
            swagger_css_url=settings.SWAGGER_CSS_URL,
            swagger_favicon_url=settings.FAVICON_URL,
        )

    @app.get(settings.REDOC_URL, include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=root_openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url=settings.REDOC_JS_URL,
            redoc_favicon_url=settings.FAVICON_URL,
        )
