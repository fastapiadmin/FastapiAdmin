"""健康检查端点

提供三级健康检查：
- /health: 基础健康检查（负载均衡器用）
- /health/ready: 就绪检查（所有依赖就绪才算 ready）
- /health/live: 存活检查（进程存活即可）
"""

import asyncio
import shutil
import time
from datetime import datetime

from fastapi import APIRouter, Request
from sqlalchemy import text

from app.common.constant import RET
from app.common.response import ErrorResponse, ResponseSchema, SuccessResponse
from app.config.setting import settings
from app.core.database import async_db_session
from app.core.logger import logger

from .schema import DependencyStatus, HealthOut, ReadinessOut

HealthRouter = APIRouter(prefix="/health", tags=["公共模块", "健康检查"])


async def _check_database() -> DependencyStatus:
    """检查数据库连接"""
    try:
        if not settings.SQL_DB_ENABLE:
            return DependencyStatus(status="disabled")

        start = time.perf_counter()
        async with async_db_session() as session:
            await session.execute(text("SELECT 1"))
        latency = (time.perf_counter() - start) * 1000
        return DependencyStatus(status="up", latency_ms=round(latency, 2))
    except Exception as e:
        logger.warning(f"数据库健康检查失败: {e}")
        return DependencyStatus(status="down")


async def _check_redis(request: Request) -> DependencyStatus:
    """检查 Redis 连接"""
    try:
        if not settings.REDIS_ENABLE:
            return DependencyStatus(status="disabled")

        redis = getattr(request.app.state, "redis", None)
        if not redis:
            return DependencyStatus(status="down")

        start = time.perf_counter()
        await redis.ping()
        latency = (time.perf_counter() - start) * 1000
        return DependencyStatus(status="up", latency_ms=round(latency, 2))
    except Exception as e:
        logger.warning(f"Redis 健康检查失败: {e}")
        return DependencyStatus(status="down")


def _get_disk_usage() -> float:
    """获取磁盘使用率"""
    try:
        usage = shutil.disk_usage("/")
        return round(usage.used / usage.total * 100, 1)
    except Exception:
        return -1.0


# 应用启动时间戳
_start_time = datetime.now()


@HealthRouter.get(
    "",
    summary="基础健康检查",
    description="仅检查进程是否存活，用于负载均衡器探测",
    response_model=ResponseSchema[HealthOut],
)
async def health_check():
    """
    基础健康检查

    参数:
    - 无

    返回:
    - SuccessResponse: 包含进程存活状态、启动时间、版本号的 JSON 响应。
    """
    uptime = (datetime.now() - _start_time).total_seconds()
    return SuccessResponse(
        data=HealthOut(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version=settings.VERSION,
            uptime_seconds=uptime,
        ),
        msg="系统健康",
    )


@HealthRouter.get(
    "/live",
    summary="存活探针",
    description="进程已启动即可返回 200，供 K8s livenessProbe 使用",
    response_model=ResponseSchema[HealthOut],
)
async def liveness_check():
    """
    存活探针

    参数:
    - 无

    返回:
    - SuccessResponse: 包含进程存活状态、启动时间、版本号的 JSON 响应。
    """
    uptime = (datetime.now() - _start_time).total_seconds()
    return SuccessResponse(
        data=HealthOut(
            status="alive",
            timestamp=datetime.now().isoformat(),
            version=settings.VERSION,
            uptime_seconds=uptime,
        ),
        msg="进程存活",
    )


@HealthRouter.get(
    "/ready",
    summary="就绪探针",
    description="探测数据库与 Redis；任一项失败返回 503，供 K8s readinessProbe 使用",
    response_model=ResponseSchema[ReadinessOut],
)
async def readiness_check(request: Request):
    """
    就绪探针

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
        return d.status in ("up", "disabled")

    all_ok = all(is_ok(d) for d in dependencies.values())

    payload = ReadinessOut(
        status="ready" if all_ok else "not_ready",
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
