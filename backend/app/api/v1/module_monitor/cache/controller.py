# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from redis.asyncio.client import Redis

from app.common.response import SuccessResponse
from app.core.exceptions import CustomException
from app.core.dependencies import AuthPermission, redis_getter
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .service import CacheService


CacheRouter = APIRouter(route_class=OperationLogRoute, prefix="/cache", tags=["缓存监控"])


@CacheRouter.get(
    '/info',
    dependencies=[Depends(AuthPermission(['module_monitor:cache:query']))],
    summary="获取缓存监控信息",
    description="获取缓存监控信息"
)
async def get_monitor_cache_info_controller(
    redis: Redis = Depends(redis_getter)
) -> JSONResponse:
    """
    获取缓存监控统计信息
    
    返回:
    - JSONResponse: 包含缓存监控统计信息的JSON响应
    """
    result = await CacheService.get_cache_monitor_statistical_info_service(redis=redis)
    log.info('获取缓存监控信息成功')
    return SuccessResponse(data=result, msg='获取缓存监控信息成功')


@CacheRouter.get(
    '/get/names',
    dependencies=[Depends(AuthPermission(['module_monitor:cache:query']))],
    summary="获取缓存名称列表",
    description="获取缓存名称列表"
)
async def get_monitor_cache_name_controller() -> JSONResponse:
    """
    获取缓存名称列表
    
    返回:
    - JSONResponse: 包含缓存名称列表的JSON响应
    """
    result = await CacheService.get_cache_monitor_cache_name_service()
    log.info('获取缓存名称列表成功')
    return SuccessResponse(data=result, msg='获取缓存名称列表成功')


@CacheRouter.get(
    '/get/keys/{cache_name}',
    dependencies=[Depends(AuthPermission(['module_monitor:cache:query']))],
    summary="获取缓存键名列表",
    description="获取缓存键名列表"
)
async def get_monitor_cache_key_controller(
    cache_name: str,
    redis: Redis = Depends(redis_getter)
    ) -> JSONResponse:
    """
    获取指定缓存名称下的键名列表
    
    参数:
    - cache_name (str): 缓存名称
    
    返回:
    - JSONResponse: 包含缓存键名列表的JSON响应
    """
    result = await CacheService.get_cache_monitor_cache_key_service(redis=redis, cache_name=cache_name)
    log.info(f'获取缓存{cache_name}的键名列表成功')
    return SuccessResponse(data=result, msg=f'获取缓存{cache_name}的键名列表成功')


@CacheRouter.get(
    '/get/value/{cache_name}/{cache_key}',
    dependencies=[Depends(AuthPermission(['module_monitor:cache:query']))],
    summary="获取缓存值",
    description="获取缓存值"
)
async def get_monitor_cache_value_controller(
    cache_name: str, 
    cache_key: str,
    redis: Redis = Depends(redis_getter)
)-> JSONResponse:
    """
    获取指定缓存键的值
    
    参数:
    - cache_name (str): 缓存名称
    - cache_key (str): 缓存键
    
    返回:
    - JSONResponse: 包含缓存值的JSON响应
    """
    result = await CacheService.get_cache_monitor_cache_value_service(redis=redis, cache_name=cache_name, cache_key=cache_key)
    log.info(f'获取缓存{cache_name}:{cache_key}的值成功')
    return SuccessResponse(data=result, msg=f'获取缓存{cache_name}:{cache_key}的值成功')


@CacheRouter.delete(
    '/delete/name/{cache_name}',
    dependencies=[Depends(AuthPermission(['module_monitor:cache:delete']))],
    summary="清除指定缓存名称的所有缓存",
    description="清除指定缓存名称的所有缓存"
)
async def clear_monitor_cache_name_controller(
    cache_name: str,
    redis: Redis = Depends(redis_getter)
) -> JSONResponse:
    """
    清除指定缓存名称下的所有缓存
    
    参数:
    - cache_name (str): 缓存名称
    
    返回:
    - JSONResponse: 包含清除结果的JSON响应
    """
    result = await CacheService.clear_cache_monitor_cache_name_service(redis=redis, cache_name=cache_name)
    if not result:
        raise CustomException(msg='清除缓存失败', data=result)
    log.info(f'清除缓存{cache_name}成功')
    return SuccessResponse(msg=f'{cache_name}对应键值清除成功', data=result)


@CacheRouter.delete(
    '/delete/key/{cache_key}',
    dependencies=[Depends(AuthPermission(['module_monitor:cache:delete']))],
    summary="清除指定缓存键",
    description="清除指定缓存键"
)
async def clear_monitor_cache_key_controller(
    cache_key: str,
    redis: Redis = Depends(redis_getter)
) -> JSONResponse:
    """
    清除指定缓存键
    
    参数:
    - cache_key (str): 缓存键
    
    返回:
    - JSONResponse: 包含清除结果的JSON响应
    """
    result = await CacheService.clear_cache_monitor_cache_key_service(redis=redis, cache_key=cache_key)
    if not result:
        raise CustomException(msg='清除缓存失败', data=result)
    log.info(f'清除缓存键{cache_key}成功')
    return SuccessResponse(msg=f'{cache_key}清除成功', data=result)


@CacheRouter.delete(
    '/delete/all',
    dependencies=[Depends(AuthPermission(['module_monitor:cache:delete']))],
    summary="清除所有缓存",
    description="清除所有缓存"
)
async def clear_monitor_cache_all_controller(
    redis: Redis = Depends(redis_getter)
) -> JSONResponse:
    """
    清除所有缓存
    
    返回:
    - JSONResponse: 包含清除结果的JSON响应
    """
    result = await CacheService.clear_cache_monitor_all_service(redis=redis)
    if not result:
        raise CustomException(msg='清除缓存失败', data=result)
    log.info('清除所有缓存成功')
    return SuccessResponse(msg='所有缓存清除成功', data=result)
