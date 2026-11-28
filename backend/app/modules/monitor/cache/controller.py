from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Security
from fastapi.responses import JSONResponse
from redis.asyncio.client import Redis

from app.common.enums import RET
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_schema import AuthSchema
from app.core.dependencies import AuthPermission, redis_getter
from app.core.exceptions import CustomException
from app.core.router_class import OperationLogRoute
from app.modules.monitor.cache.browser import RedisBrowserService
from app.modules.monitor.cache.schema import (
    CacheInfoSchema,
    CacheMonitorSchema,
    RedisDatabaseSchema,
    RedisKeyPageSchema,
    RedisValueSchema,
)

from .service import CacheService

CacheRouter = APIRouter(route_class=OperationLogRoute, prefix="/cache", tags=["缓存监控"])


def _require_superuser(auth: AuthSchema) -> None:
    """Redis keyspace browsing exposes raw key names/values; platform admins only."""
    if not auth.user or not auth.user.is_superuser:
        raise CustomException(msg="仅平台管理员可查看 Redis 键空间", code=RET.FORBIDDEN.code)


@CacheRouter.get("/info", summary="获取缓存监控信息", response_model=ResponseSchema[CacheMonitorSchema], dependencies=[Security(AuthPermission(["module_monitor:cache:query"]))])
async def get_monitor_cache_info_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    result: CacheMonitorSchema = await CacheService.get_monitor_statistical_info(redis=redis)
    return SuccessResponse(data=result, msg="获取缓存监控信息成功")


@CacheRouter.get("/get/names", summary="获取缓存名称列表", response_model=ResponseSchema[list[CacheInfoSchema]], dependencies=[Security(AuthPermission(["module_monitor:cache:query"]))])
async def get_monitor_cache_name_controller() -> JSONResponse:
    result: list[CacheInfoSchema] = await CacheService.get_monitor_cache_names()
    return SuccessResponse(data=result, msg="获取缓存名称列表成功")


@CacheRouter.get("/get/keys/{cache_name}", summary="获取缓存键名列表", response_model=ResponseSchema[list[CacheInfoSchema]], dependencies=[Security(AuthPermission(["module_monitor:cache:query"]))])
async def get_monitor_cache_key_controller(cache_name: Annotated[str, Path(description="缓存名称")], redis: Annotated[Redis, Depends(redis_getter)]) -> JSONResponse:
    result: list[str] = await CacheService.get_monitor_cache_keys(redis=redis, cache_name=cache_name)
    return SuccessResponse(data=result, msg=f"获取缓存{cache_name}的键名列表成功")


@CacheRouter.get("/get/value/{cache_name}/{cache_key}", summary="获取缓存值", response_model=ResponseSchema[CacheInfoSchema], dependencies=[Security(AuthPermission(["module_monitor:cache:detail"]))])
async def get_monitor_cache_value_controller(
    cache_name: Annotated[str, Path(description="缓存名称")],
    cache_key: Annotated[str, Path(description="缓存键名")],
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    result: CacheInfoSchema = await CacheService.get_monitor_cache_value(redis=redis, cache_name=cache_name, cache_key=cache_key)
    return SuccessResponse(data=result, msg=f"获取缓存{cache_name}:{cache_key}的值成功")


@CacheRouter.delete("/delete/name/{cache_name}", summary="清除指定缓存名称的所有缓存", response_model=ResponseSchema[None], dependencies=[Security(AuthPermission(["module_monitor:cache:delete"]))])
async def clear_monitor_cache_name_controller(cache_name: Annotated[str, Path(description="缓存名称")], redis: Annotated[Redis, Depends(redis_getter)]) -> JSONResponse:
    result: bool = await CacheService.clear_monitor_cache_by_name(redis=redis, cache_name=cache_name)
    return SuccessResponse(msg=f"{cache_name}对应键值清除成功", data=result)


@CacheRouter.delete("/delete/key/{cache_key}", summary="清除指定缓存键", response_model=ResponseSchema[None], dependencies=[Security(AuthPermission(["module_monitor:cache:delete"]))])
async def clear_monitor_cache_key_controller(cache_key: Annotated[str, Path(description="缓存键名")], redis: Annotated[Redis, Depends(redis_getter)]) -> JSONResponse:
    result: bool = await CacheService.clear_monitor_cache_by_key(redis=redis, cache_key=cache_key)
    return SuccessResponse(msg=f"{cache_key}清除成功", data=result)


@CacheRouter.delete("/clear", summary="清除所有缓存", response_model=ResponseSchema[None], dependencies=[Security(AuthPermission(["module_monitor:cache:delete"]))])
async def clear_monitor_cache_all_controller(
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    result: bool = await CacheService.clear_monitor_cache_all(redis=redis)
    return SuccessResponse(msg="所有缓存清除成功", data=result)


# ── Redis 通用键空间浏览（只读）───────────────────────────────────────


@CacheRouter.get(
    "/redis/databases", summary="Redis 逻辑库列表（只读）", response_model=ResponseSchema[list[RedisDatabaseSchema]], dependencies=[Security(AuthPermission(["module_monitor:cache:query"]))]
)
async def list_redis_databases_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_monitor:cache:query"]))],
    redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    _require_superuser(auth)
    result: list[RedisDatabaseSchema] = await RedisBrowserService.list_databases(redis=redis)
    return SuccessResponse(data=result, msg="查询逻辑库成功")


@CacheRouter.get("/redis/keys", summary="SCAN 浏览 Redis 键（只读）", response_model=ResponseSchema[RedisKeyPageSchema], dependencies=[Security(AuthPermission(["module_monitor:cache:query"]))])
async def scan_redis_keys_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_monitor:cache:query"]))],
    redis: Annotated[Redis, Depends(redis_getter)],
    db: Annotated[int, Query(ge=0, le=15, description="逻辑库序号")] = 0,
    pattern: Annotated[str, Query(max_length=128, description="匹配模式（支持 * ?）")] = "*",
    cursor: Annotated[int, Query(ge=0, description="SCAN 游标，首页传 0")] = 0,
    count: Annotated[int, Query(ge=1, le=500, description="单页数量提示")] = 100,
) -> JSONResponse:
    _require_superuser(auth)
    result: RedisKeyPageSchema = await RedisBrowserService.scan_keys(redis=redis, db=db, pattern=pattern, cursor=cursor, count=count)
    return SuccessResponse(data=result, msg="扫描键成功")


@CacheRouter.get(
    "/redis/value", summary="读取 Redis 单键详情（只读，敏感键脱敏）", response_model=ResponseSchema[RedisValueSchema], dependencies=[Security(AuthPermission(["module_monitor:cache:detail"]))]
)
async def get_redis_value_controller(
    auth: Annotated[AuthSchema, Security(AuthPermission(["module_monitor:cache:detail"]))],
    redis: Annotated[Redis, Depends(redis_getter)],
    key: Annotated[str, Query(min_length=1, max_length=512, description="键名")],
    db: Annotated[int, Query(ge=0, le=15, description="逻辑库序号")] = 0,
) -> JSONResponse:
    _require_superuser(auth)
    result: RedisValueSchema = await RedisBrowserService.get_value(redis=redis, db=db, key=key)
    return SuccessResponse(data=result, msg="读取键详情成功")
