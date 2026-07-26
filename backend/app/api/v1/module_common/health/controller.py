import asyncio
import shutil
import time
from collections.abc import AsyncIterable
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent
from sqlalchemy import text

from app.common.enums import RET
from app.common.response import ErrorResponse, ResponseSchema, SuccessResponse
from app.config.setting import settings
from app.core.database import async_db_session
from app.core.logger import logger
from app.core.router_class import OperationLogRoute

from .schema import DependencyStatus, HealthOut, ReadinessOut

HealthRouter = APIRouter(route_class=OperationLogRoute, prefix="/health", tags=["健康检查"])

# ── 健康检查时间间隔 ──
_HEALTH_STREAM_INTERVAL = 30  # 秒


async def _check_database() -> DependencyStatus:
    """检查数据库连接"""
    try:
        start = time.perf_counter()
        async with async_db_session() as session:
            await session.execute(text("SELECT 1"))
        latency = (time.perf_counter() - start) * 1000
        return DependencyStatus(status=1, latency_ms=round(latency, 2))
    except Exception as e:
        logger.warning(f"数据库健康检查失败: {e}")
        return DependencyStatus(status=0)


async def _check_redis(request: Request) -> DependencyStatus:
    """检查 Redis 连接"""
    try:
        redis = getattr(request.app.state, "redis", None)
        if not redis:
            return DependencyStatus(status=0)

        start = time.perf_counter()
        await redis.ping()
        latency = (time.perf_counter() - start) * 1000
        return DependencyStatus(status=1, latency_ms=round(latency, 2))
    except Exception as e:
        logger.warning(f"Redis 健康检查失败: {e}")
        return DependencyStatus(status=0)


def _get_disk_usage() -> float:
    """获取磁盘使用率"""
    try:
        usage = shutil.disk_usage("/")
        return round(usage.used / usage.total * 100, 1)
    except Exception:
        return -1.0


# 应用启动时间戳
_start_time = datetime.now()


@HealthRouter.get("/check", summary="健康检查", response_model=ResponseSchema[HealthOut])
async def health_check() -> JSONResponse:
    """基础健康检查

    参数:
    - 无

    返回:
    - SuccessResponse: 包含进程存活状态、启动时间、版本号的 JSON 响应。
    """
    uptime = (datetime.now() - _start_time).total_seconds()
    return SuccessResponse(
        data=HealthOut(
            status=1,
            timestamp=datetime.now().isoformat(),
            version=settings.VERSION,
            uptime_seconds=uptime,
        ),
        msg="系统健康",
    )


@HealthRouter.get("/live", summary="存活探针", response_model=ResponseSchema[HealthOut])
async def liveness_check() -> JSONResponse:
    """存活探针

    参数:
    - 无

    返回:
    - SuccessResponse: 包含进程存活状态、启动时间、版本号的 JSON 响应。
    """
    uptime = (datetime.now() - _start_time).total_seconds()
    return SuccessResponse(
        data=HealthOut(
            status=1,
            timestamp=datetime.now().isoformat(),
            version=settings.VERSION,
            uptime_seconds=uptime,
        ),
        msg="进程存活",
    )


@HealthRouter.get("/ready", summary="就绪探针", response_model=ResponseSchema[ReadinessOut])
async def readiness_check(request: Request) -> JSONResponse:
    """就绪探针

    参数:
    - request (Request): FastAPI 请求对象，用于获取 Redis 客户端。

    返回:
    - SuccessResponse | ErrorResponse: 依赖就绪时返回 200，未就绪返回 503。
    """
    uptime = (datetime.now() - _start_time).total_seconds()

    db_status, redis_status = await asyncio.gather(
        _check_database(),
        _check_redis(request),
    )

    dependencies = {
        "database": db_status,
        "redis": redis_status,
    }

    # 判断总体状态
    def is_ok(d: DependencyStatus) -> bool:
        return d.status == 1

    all_ok = all(is_ok(d) for d in dependencies.values())

    payload = ReadinessOut(
        status=1 if all_ok else 0,
        timestamp=datetime.now().isoformat(),
        version=settings.VERSION,
        uptime_seconds=uptime,
        dependencies=dependencies,
        disk_usage=_get_disk_usage(),
    )

    if all_ok:
        return SuccessResponse(data=payload, msg="依赖就绪")

    return ErrorResponse(
        data=payload,
        msg="依赖未就绪",
        code=RET.SERVICE_UNAVAILABLE.code,
        status_code=503,
        success=False,
    )


# ============================================================
# SSE 健康状态实时推送
# ============================================================


async def _build_health_payload(request: Request) -> dict:
    """采集当前健康状态"""
    db_status, redis_status = await asyncio.gather(
        _check_database(),
        _check_redis(request),
    )
    return {
        "status": 1 if db_status.status and redis_status.status else 0,
        "dependencies": {
            "database": db_status.model_dump(),
            "redis": redis_status.model_dump(),
        },
        "disk_usage": _get_disk_usage(),
        "uptime_seconds": (datetime.now() - _start_time).total_seconds(),
        "timestamp": datetime.now().isoformat(),
    }


@HealthRouter.get("/stream", summary="健康状态实时推送", response_class=EventSourceResponse)
async def health_stream(request: Request) -> AsyncIterable[ServerSentEvent]:
    """SSE 实时推送健康状态，每 30 秒推送一次，客户端无需轮询 /ready。"""
    yield ServerSentEvent(data=await _build_health_payload(request), event="health")

    while True:
        await asyncio.sleep(_HEALTH_STREAM_INTERVAL)
        yield ServerSentEvent(data=await _build_health_payload(request), event="health")
