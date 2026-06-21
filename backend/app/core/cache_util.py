"""轻量 Redis 缓存工具（替代 fastapi-cache2，兼容 redis-py）"""
import hashlib
import json
from collections.abc import Callable
from functools import wraps
from typing import Any

from redis.asyncio.client import Redis
from starlette.responses import Response

_ENABLE: bool = True
_EXPIRE: int = 300
_PREFIX: str = "fastapi-admin-cache"
_REDIS: Redis | None = None


async def init(redis: Redis, prefix: str = "fastapi-admin-cache", expire: int = 300, enable: bool = True) -> None:
    global _REDIS, _PREFIX, _EXPIRE, _ENABLE
    _REDIS = redis
    _PREFIX = prefix
    _EXPIRE = expire
    _ENABLE = enable


def _build_key(namespace: str, func: Callable, *args: Any, **kwargs: Any) -> str:
    raw = f"{func.__module__}:{func.__qualname__}:{args}:{kwargs}"
    return f"{_PREFIX}:{namespace}:{hashlib.md5(raw.encode()).hexdigest()}"


def cache(expire: int | None = None, namespace: str = "default"):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not _ENABLE or _REDIS is None:
                return await func(*args, **kwargs)
            key = _build_key(namespace, func, *args, **kwargs)
            cached = await _REDIS.get(key)
            if cached:
                data = json.loads(cached)
                return Response(
                    content=json.dumps(data, ensure_ascii=False),
                    media_type="application/json; charset=utf-8",
                    status_code=200,
                )
            result = await func(*args, **kwargs)
            # 提取 Response 对象的 body 进行缓存
            if isinstance(result, Response):
                body = result.body
            else:
                body = json.dumps(result).encode()
            await _REDIS.set(key, body, ex=expire or _EXPIRE)
            return result

        return wrapper

    return decorator


async def clear(namespace: str | None = None) -> None:
    if _REDIS is None:
        return
    pattern = f"{_PREFIX}:{namespace}:*" if namespace else f"{_PREFIX}:*"
    keys = [key async for key in _REDIS.scan_iter(match=pattern)]
    if keys:
        await _REDIS.delete(*keys)
