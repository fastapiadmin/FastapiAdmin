# -*- coding: utf-8 -*-

from re import T
from starlette.responses import HTMLResponse
from typing import Any, AsyncGenerator
from fastapi import Depends, FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter, WebSocketRateLimiter
from starlette.websockets import WebSocket
from math import ceil

from app.config.setting import settings
from app.core.logger import log
from app.core.discover import router
from app.core.exceptions import CustomException, handle_exception
from app.utils.common_util import import_module, import_modules_async
from app.scripts.initialize import InitializeData

from app.api.v1.module_application.job.tools.ap_scheduler import SchedulerUtil
from app.api.v1.module_system.params.service import ParamsService
from app.api.v1.module_system.dict.service import DictDataService

# 导入WebSocket路由器
from app.api.v1.module_application.ai.ws import WS_AI

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    """
    自定义 FastAPI 应用生命周期。
    
    参数:
    - app (FastAPI): FastAPI 应用实例。
    
    返回:
    - AsyncGenerator[Any, Any]: 生命周期上下文生成器。
    """
    try:
        await InitializeData().init_db()
        log.info(f"✅ {settings.DATABASE_TYPE}数据库初始化完成")
        await import_modules_async(modules=settings.EVENT_LIST, desc="全局事件", app=app, status=True)
        log.info("✅ 全局事件模块加载完成")
        await ParamsService().init_config_service(redis=app.state.redis)
        log.info("✅ Redis系统配置初始化完成")
        await DictDataService().init_dict_service(redis=app.state.redis)
        log.info("✅ Redis数据字典初始化完成")
        await SchedulerUtil.init_system_scheduler()
        scheduler_jobs_count = len(SchedulerUtil.get_all_jobs())
        scheduler_status = SchedulerUtil.get_job_status()
        log.info(f"✅ 定时任务调度器初始化完成 ({scheduler_jobs_count} 个任务)")

        # 6. 初始化请求限制器
        await FastAPILimiter.init(
            redis=app.state.redis,
            prefix=settings.REQUEST_LIMITER_REDIS_PREFIX,
            http_callback=http_limit_callback,
        )
        log.info("✅ 请求限制器初始化完成")
        
        # 导入并显示最终的启动信息面板
        from app.utils.console import run as console_run
        from app.common.enums import EnvironmentEnum
        console_run(
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=True if settings.ENVIRONMENT == EnvironmentEnum.DEV else False,
            redis_ready=True,
            scheduler_jobs=scheduler_jobs_count,
            scheduler_status=scheduler_status,
        )
        
    except Exception as e:
        log.error(f"❌ 应用初始化失败: {str(e)}")
        raise

    yield
    
    try:
        await import_modules_async(modules=settings.EVENT_LIST, desc="全局事件", app=app, status=False)
        log.info("✅ 全局事件模块卸载完成")
        await SchedulerUtil.close_system_scheduler()
        log.info("✅ 定时任务调度器已关闭")
        await FastAPILimiter.close()
        log.info("✅ 请求限制器已关闭")

    except Exception as e:
        log.error(f"❌ 应用关闭过程中发生错误: {str(e)}")
        

def register_middlewares(app: FastAPI) -> None:
    """
    注册全局中间件。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    for middleware in settings.MIDDLEWARE_LIST[::-1]:
        if not middleware:
            continue
        middleware = import_module(middleware, desc="中间件")
        app.add_middleware(middleware)

def register_exceptions(app: FastAPI) -> None:
    """
    统一注册异常处理器。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    handle_exception(app)

def register_routers(app: FastAPI) -> None:
    """
    注册根路由。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    # 手动注册WebSocket路由，不使用速率限制器
    app.include_router(router=WS_AI, dependencies=[Depends(WebSocketRateLimiter(times=1, seconds=5))])
    # 先将动态路由注册到应用，使用速率限制器
    app.include_router(router=router, dependencies=[Depends(RateLimiter(times=5, seconds=10))])

def register_files(app: FastAPI) -> None:
    """
    注册静态资源挂载和文件相关配置。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    # 挂载静态文件目录
    if settings.STATIC_ENABLE:
        # 确保日志目录存在
        settings.STATIC_ROOT.mkdir(parents=True, exist_ok=True)
        app.mount(path=settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT), name=settings.STATIC_DIR)

def reset_api_docs(app: FastAPI) -> None:
    """
    使用本地静态资源自定义 API 文档页面（Swagger UI 与 ReDoc）。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """

    @app.get(settings.DOCS_URL, include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=str(app.root_path) + str(app.openapi_url),
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=settings.SWAGGER_JS_URL,
            swagger_css_url=settings.SWAGGER_CSS_URL,
            swagger_favicon_url=settings.FAVICON_URL,
        )

    @app.get(str(app.swagger_ui_oauth2_redirect_url), include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(settings.REDOC_URL, include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=str(app.root_path) + str(app.openapi_url),
            title=app.title + " - ReDoc",
            redoc_js_url=settings.REDOC_JS_URL,
            redoc_favicon_url=settings.FAVICON_URL,
        )

async def http_limit_callback(request: Request, response: Response, expire: int):
    """
    请求限制时的默认回调函数

    :param request: FastAPI 请求对象
    :param response: FastAPI 响应对象
    :param expire: 剩余毫秒数
    :return:
    """
    expires = ceil(expire / 30)
    raise CustomException(
        status_code=429,
        msg='请求过于频繁，请稍后重试！',
        data={'Retry-After': str(expires)},
    )

# 为WebSocket添加默认的回调函数
async def ws_limit_callback(ws: WebSocket, expire: int):
    """
    WebSocket请求限制时的默认回调函数

    :param ws: WebSocket连接对象
    :param expire: 剩余毫秒数
    :return:
    """
    expires = ceil(expire / 30)
    await ws.close(code=1008, reason=f'请求过于频繁，请稍后重试！{expires} 秒后重试')
