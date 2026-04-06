from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.common.constant import RET
from app.common.response import ErrorResponse, ResponseSchema, SuccessResponse
from app.config.setting import settings
from app.core.database import async_db_session

HealthRouter = APIRouter(prefix="/health", tags=["健康检查"])


@HealthRouter.get(
    "/",
    summary="存活探针（Liveness）",
    description="进程已启动即可返回 200；不探测外部依赖，供 K8s livenessProbe 使用。",
    response_model=ResponseSchema[dict],
)
async def health_check() -> JSONResponse:
    """轻量存活检查：避免在依赖故障时误杀进程。"""
    return SuccessResponse(data=True, msg="系统健康")


@HealthRouter.get(
    "/ready/",
    summary="就绪探针（Readiness）",
    description="探测数据库与 Redis；任一项失败返回 503，供 K8s readinessProbe 摘除流量。",
    response_model=ResponseSchema[dict[str, Any]],
)
async def readiness_check(request: Request) -> JSONResponse:
    """
    就绪检查：启动阶段已通过 lifespan 连接 Redis，此处做周期性轻量 ping。

    数据库使用 ``SELECT 1``，避免依赖具体表结构。
    """
    checks: dict[str, bool | None] = {"database": None, "redis": None}
    detail_errors: list[str] = []

    db_ok = False
    if settings.SQL_DB_ENABLE:
        try:
            async with async_db_session() as session:
                async with session.begin():
                    await session.execute(text("SELECT 1"))
            checks["database"] = True
            db_ok = True
        except Exception as e:
            checks["database"] = False
            detail_errors.append(f"database:{e!s}")
    else:
        checks["database"] = False
        detail_errors.append("database:SQL_DB_ENABLE is false")

    redis_ok = True
    if settings.REDIS_ENABLE:
        redis_ok = False
        try:
            rd = getattr(request.app.state, "redis", None)
            if rd is not None:
                await rd.ping()  # type: ignore[misc]
                checks["redis"] = True
                redis_ok = True
            else:
                checks["redis"] = False
                detail_errors.append("redis:app.state.redis missing")
        except Exception as e:
            checks["redis"] = False
            detail_errors.append(f"redis:{e!s}")
    else:
        checks["redis"] = None

    all_ok = db_ok and redis_ok and not detail_errors
    payload: dict[str, Any] = {"checks": checks, "errors": detail_errors or None}

    if all_ok:
        return SuccessResponse(data=payload, msg="依赖就绪")

    return ErrorResponse(
        data=payload,
        msg="依赖未就绪",
        code=RET.SERVICE_UNAVAILABLE.code,
        status_code=503,
        success=False,
    )
