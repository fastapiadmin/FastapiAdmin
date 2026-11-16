"""Redis 通用键空间浏览（**只读**）。

与 ``CacheService`` 的区别：后者按应用缓存名前缀浏览（``cache_names``），只覆盖本系统自己的键；
本模块提供任意键空间的只读浏览：逻辑库清单 → SCAN 分页 → 单键详情（按类型取值）。

安全：
- 只读，不提供写入/删除；
- 键名命中敏感模式（token/session/password 等）时，**值一律脱敏**，只回类型/TTL/大小；
- 值按类型限量返回并标记 ``truncated``，避免把大值整段读进内存与响应体。

数据库切换：app 的 Redis 客户端连在默认库上；浏览其它库时按连接参数**新建短生命周期客户端**，
用完即关，避免 ``SELECT`` 污染共享连接池（与 FastHub 的做法一致）。
"""

import re
from typing import Any, cast

from redis.asyncio.client import Redis

from app.core.exceptions import CustomException

from .schema import RedisDatabaseSchema, RedisKeyMetaSchema, RedisKeyPageSchema, RedisValueSchema

# 敏感键模式：命中即对值脱敏（键名本身仍展示，便于运维定位）
_SENSITIVE_KEY_RE = re.compile(
    r"(token|secret|password|passwd|session|credential|api[_-]?key|authorization|refresh)",
    re.IGNORECASE,
)

# 单值返回上限（字符/元素数）
_MAX_TEXT = 4000
_MAX_ELEMENTS = 200
_MAX_STREAM = 50


def _text(value: Any, limit: int = _MAX_TEXT) -> tuple[str, bool]:
    """把值转成文本并截断（bytes 安全）。"""
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="backslashreplace")
    text = value if isinstance(value, str) else str(value)
    if len(text) <= limit:
        return text, False
    return text[:limit], True


def is_sensitive_key(key: str) -> bool:
    """键名是否命中敏感模式（命中则值脱敏）。"""
    return bool(_SENSITIVE_KEY_RE.search(key or ""))


class RedisBrowserService:
    """Redis 键空间只读浏览服务。"""

    @staticmethod
    def _base_db(redis: Redis) -> int:
        """当前客户端所在的逻辑库序号。"""
        try:
            return int(redis.connection_pool.connection_kwargs.get("db") or 0)
        except Exception:  # pragma: no cover - 连接参数异常时按默认库处理
            return 0

    @staticmethod
    def _client_for_db(redis: Redis, db: int) -> tuple[Redis, bool]:
        """取得指定逻辑库的客户端；返回 (client, 是否需要自行关闭)。"""
        if db == RedisBrowserService._base_db(redis):
            return redis, False
        kwargs = dict(redis.connection_pool.connection_kwargs)
        kwargs["db"] = db
        return Redis(**kwargs), True

    @staticmethod
    async def list_databases(redis: Redis) -> list[RedisDatabaseSchema]:
        """列出逻辑库与键数量（解析 ``INFO keyspace``）。"""
        raw = await redis.info("keyspace")
        result: list[RedisDatabaseSchema] = []
        for name, value in (raw or {}).items():
            if not isinstance(name, str) or not name.startswith("db") or not name[2:].isdigit():
                continue
            parsed: dict[str, int] = {}
            if isinstance(value, dict):
                # redis-py 会把 INFO keyspace 解析为 {db1: {keys, expires, avg_ttl}}
                for k, v in value.items():
                    try:
                        parsed[str(k)] = int(v)
                    except (TypeError, ValueError):
                        continue
            else:
                text = value.decode("utf-8", "ignore") if isinstance(value, bytes) else str(value)
                for part in text.split(","):
                    if "=" in part:
                        k, v = part.split("=", 1)
                        try:
                            parsed[k.strip()] = int(v)
                        except ValueError:
                            continue
            result.append(
                RedisDatabaseSchema(
                    db=int(name[2:]),
                    keys=parsed.get("keys", 0),
                    expires=parsed.get("expires", 0),
                )
            )
        result.sort(key=lambda item: item.db)
        return result

    @staticmethod
    async def scan_keys(
        redis: Redis,
        *,
        db: int = 0,
        pattern: str = "*",
        cursor: int = 0,
        count: int = 100,
    ) -> RedisKeyPageSchema:
        """SCAN 分页浏览键（附带 type/ttl）。"""
        client, owned = RedisBrowserService._client_for_db(redis, db)
        try:
            next_cursor, keys = await client.scan(cursor=cursor, match=pattern or "*", count=max(1, min(count, 500)))
            metas: list[RedisKeyMetaSchema] = []
            if keys:
                # pipeline 批量取 type/ttl，避免逐键往返
                async with client.pipeline(transaction=False) as pipe:
                    for key in keys:
                        pipe.type(key)
                        pipe.ttl(key)
                    results = await pipe.execute()
                for index, key in enumerate(keys):
                    key_type = results[index * 2]
                    ttl = results[index * 2 + 1]
                    metas.append(
                        RedisKeyMetaSchema(
                            key=_text(key, limit=512)[0],
                            type=_text(key_type, limit=32)[0] if key_type is not None else "none",
                            ttl=int(ttl) if isinstance(ttl, int) else -1,
                        )
                    )
            return RedisKeyPageSchema(cursor=int(next_cursor), keys=metas, scanned=len(metas))
        finally:
            if owned:
                await client.aclose()

    @staticmethod
    async def get_value(redis: Redis, *, db: int, key: str) -> RedisValueSchema:
        """读取单键详情（只读；敏感键脱敏；值按类型限量）。"""
        if not key:
            raise CustomException(msg="键名不能为空")
        client, owned = RedisBrowserService._client_for_db(redis, db)
        try:
            key_type = await client.type(key)
            key_type = _text(key_type, limit=32)[0] if key_type is not None else "none"
            if key_type == "none":
                raise CustomException(msg=f"键不存在: {key}")
            ttl = await client.ttl(key)
            ttl_value = int(ttl) if isinstance(ttl, int) else -1
            size: int | None = None
            try:
                raw_size = await client.memory_usage(key)
                size = int(raw_size) if isinstance(raw_size, int) else None
            except Exception:
                size = None

            if is_sensitive_key(key):
                return RedisValueSchema(
                    key=key,
                    type=key_type,
                    ttl=ttl_value,
                    size=size,
                    value="••••••（敏感键已脱敏）",
                    truncated=False,
                    masked=True,
                )

            value, truncated = await RedisBrowserService._read_typed(client, key, key_type)
            return RedisValueSchema(
                key=key,
                type=key_type,
                ttl=ttl_value,
                size=size,
                value=value,
                truncated=truncated,
            )
        finally:
            if owned:
                await client.aclose()

    @staticmethod
    async def _read_typed(client: Redis, key: str, key_type: str) -> tuple[object, bool]:
        """按类型读取值（限量）。"""
        if key_type == "string":
            raw = await client.get(key)
            return _text(raw)
        if key_type == "hash":
            raw_hash = await cast(Any, client.hgetall(key))
            items = list(raw_hash.items())[:_MAX_ELEMENTS]
            text_map = {_text(k, 512)[0]: _text(v)[0] for k, v in items}
            return text_map, len(raw_hash) > _MAX_ELEMENTS
        if key_type == "list":
            raw_list = await cast(Any, client.lrange(key, 0, _MAX_ELEMENTS - 1))
            return [_text(item)[0] for item in raw_list], len(raw_list) >= _MAX_ELEMENTS
        if key_type == "set":
            _, members = await client.sscan(key, count=_MAX_ELEMENTS)
            return [_text(item)[0] for item in members[:_MAX_ELEMENTS]], len(members) > _MAX_ELEMENTS
        if key_type == "zset":
            raw_zset = await client.zrange(key, 0, _MAX_ELEMENTS - 1, withscores=True)
            return [
                {"member": _text(member, 512)[0], "score": float(score)}
                for member, score in raw_zset[:_MAX_ELEMENTS]
            ], len(raw_zset) > _MAX_ELEMENTS
        if key_type == "stream":
            stream = await client.xrange(key, count=_MAX_STREAM)
            return [
                {"id": _text(entry_id, 128)[0], "fields": {_text(k, 128)[0]: _text(v)[0] for k, v in fields.items()}}
                for entry_id, fields in stream[:_MAX_STREAM]
            ], len(stream) >= _MAX_STREAM
        # 未知类型（如 module/自定义）：只回类型提示
        return "（该类型暂不支持详情展示）", False
