import json
from collections.abc import Awaitable
from typing import Any

from redis.asyncio.client import Redis

from app.core.logger import log


class RedisCURD:
    """缓存工具类"""

    def __init__(self, redis: Redis) -> None:
        """初始化"""
        self.redis = redis

    async def mget(self, keys: list) -> list:
        """批量获取缓存

        参数:
        - keys (list): 键名列表

        返回:
        - list: 返回缓存值列表,如果获取失败则返回空列表
        """
        try:
            data = await self.redis.mget(*[str(key) for key in keys])
            return data
        except Exception as e:
            log.error(f"批量获取缓存失败: {e!s}")
            return []

    async def get_keys(self, pattern: str = "*") -> list:
        """获取缓存键名

        参数:
        - pattern (str, optional): 匹配模式,默认值为"*"。

        返回:
        - list: 返回匹配的缓存键名列表,如果获取失败则返回空列表
        """
        try:
            keys = await self.redis.keys(f"{pattern}")
            return keys
        except Exception as e:
            log.error(f"获取缓存键名失败: {e!s}")
            return []

    async def get(self, key: str) -> Any:
        """获取缓存

        参数:
        - key (str): 缓存键名

        返回:
        - Any: 返回缓存值,如果缓存不存在则返回None
        """
        try:
            data = await self.redis.get(f"{key}")

            if data is None:
                return None

            return data

        except Exception as e:
            log.error(f"获取缓存失败: {e!s}")
            return None

    async def set(self, key: str, value: Any, expire: int | None = None) -> bool:
        """设置缓存

        参数:
        - key (str): 缓存键名
        - value (Any): 缓存值
        - expire (int | None, optional): 过期时间,单位为秒,默认值为None。

        返回:
        - bool: 如果设置缓存成功则返回True,否则返回False
        """
        try:
            # 根据数据类型选择序列化方式
            if isinstance(value, (int, float, str)):
                data = str(value).encode("utf-8")
            else:
                try:
                    data = json.dumps(value).encode("utf-8")
                except Exception as e:
                    log.error(f"序列化数据失败: {e!s}")
                    return False

            await self.redis.set(name=key, value=data, ex=expire)
            return True

        except Exception as e:
            log.error(f"设置缓存失败: {e!s}")
            return False

    async def lock(self, key: str, expire: int, value: str | None = None) -> tuple[bool, str]:
        """获取分布式锁

        参数:
        - key (str): 锁键名
        - expire (int): 锁过期时间,单位为秒
        - value (str, optional): 锁值,默认值为None（自动生成UUID）。

        返回:
        - tuple[bool, str]: (获取锁是否成功, 锁值)
        """
        try:
            import uuid

            # 如果没有提供value，生成唯一的UUID
            lock_value = value or str(uuid.uuid4())
            # 使用setnx命令实现原子性锁获取
            result = await self.redis.set(
                name=key,
                value=lock_value,
                ex=expire,
                nx=True,  # 只有当键不存在时才设置
            )
            return (result is not None, lock_value)
        except Exception as e:
            log.error(f"获取分布式锁失败: {e!s}")
            return (False, "")

    async def unlock(self, key: str, value: str) -> bool:
        """释放分布式锁（安全版本，验证锁值）

        参数:
        - key (str): 锁键名
        - value (str): 锁值，用于验证锁的持有者

        返回:
        - bool: 如果释放锁成功则返回True,否则返回False
        """
        try:
            # 使用Lua脚本确保原子性验证和删除
            script = """
            if redis.call('get', KEYS[1]) == ARGV[1] then
                return redis.call('del', KEYS[1])
            else
                return 0
            end
            """
            result = await self.redis.eval(script, 1, key, value)  # pyright: ignore[reportGeneralTypeIssues]
            return result == 1
        except Exception as e:
            log.error(f"释放分布式锁失败: {e!s}")
            return False

    async def unlock_simple(self, key: str) -> bool:
        """释放分布式锁（简单版本，不验证锁值）

        参数:
        - key (str): 锁键名

        返回:
        - bool: 如果释放锁成功则返回True,否则返回False
        """
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            log.error(f"释放分布式锁失败: {e!s}")
            return False

    async def delete(self, *keys: str) -> bool:
        """删除缓存

        参数:
        - keys (str): 缓存键名

        返回:
        - bool: 如果删除缓存成功则返回True,否则返回False
        """
        try:
            await self.redis.delete(*keys)
            return True
        except Exception as e:
            log.error(f"删除缓存失败: {e!s}")
            return False

    async def clear(self, pattern: str = "*") -> bool:
        """清空缓存

        参数:
        - pattern (str, optional): 匹配模式,默认值为"*"。

        返回:
        - bool: 如果清空缓存成功则返回True,否则返回False
        """
        try:
            keys = await self.redis.keys(f"{pattern}")
            if keys:
                await self.redis.delete(*keys)
            return True
        except Exception as e:
            log.error(f"清空缓存失败: {e!s}")
            return False

    async def exists(self, key: str) -> bool:
        """判断缓存是否存在

        参数:
        - key (str): 缓存键名

        返回:
        - bool: 如果缓存存在则返回True,否则返回False
        """
        try:
            return await self.redis.exists(f"{key}")
        except Exception as e:
            log.error(f"判断缓存是否存在失败: {e!s}")
            return False

    async def ttl(self, key: str) -> int:
        """获取缓存过期时间

        参数:
        - key (str): 缓存键名

        返回:
        - int: 返回缓存过期时间,单位为秒,如果缓存没有设置过期时间则返回-1
        """
        try:
            return await self.redis.ttl(f"{key}")
        except Exception as e:
            log.error(f"获取缓存过期时间失败: {e!s}")
            return -1

    async def renew_lock(self, key: str, expire: int, value: str) -> bool:
        """续约分布式锁

        参数:
        - key (str): 锁键名
        - expire (int): 新的过期时间,单位为秒
        - value (str): 锁值，用于验证锁的持有者

        返回:
        - bool: 如果续约锁成功则返回True,否则返回False
        """
        try:
            # 使用Lua脚本确保原子性验证和续约
            script = """
            if redis.call('get', KEYS[1]) == ARGV[1] then
                return redis.call('expire', KEYS[1], ARGV[2])
            else
                return 0
            end
            """
            result = await self.redis.eval(script, 1, key, value, str(expire))  # pyright: ignore[reportGeneralTypeIssues]
            return result == 1
        except Exception as e:
            log.error(f"续约分布式锁失败: {e!s}")
            return False

    async def expire(self, key: str, expire: int) -> bool:
        """设置缓存过期时间

        参数:
        - key (str): 缓存键名
        - expire (int): 过期时间,单位为秒

        返回:
        - bool: 如果设置缓存过期时间成功则返回True,否则返回False
        """
        try:
            return await self.redis.expire(f"{key}", expire)
        except Exception as e:
            log.error(f"设置缓存过期时间失败: {e!s}")
            return False

    async def info(self) -> dict:
        """获取缓存信息

        返回:
        - dict: 返回缓存信息字典,如果获取失败则返回空字典
        """
        try:
            return await self.redis.info()
        except Exception as e:
            log.error(f"获取缓存信息失败: {e!s}")
            return {}

    async def db_size(self) -> int:
        """获取数据库大小

        返回:
        - int: 返回数据库大小,如果获取失败则返回0
        """
        try:
            return await self.redis.dbsize()
        except Exception as e:
            log.error(f"获取数据库大小失败: {e!s}")
            return 0

    async def commandstats(self) -> dict:
        """获取命令统计信息

        返回:
        - dict: 返回命令统计信息字典,如果获取失败则返回空字典
        """
        try:
            return await self.redis.info("commandstats")
        except Exception as e:
            log.error(f"获取命令统计信息失败: {e!s}")
            return {}

    async def hash_set(self, name: str, key: str, value: Any) -> bool:
        """设置哈希缓存

        参数:
        - name (str): 哈希缓存名称
        - key (str): 哈希缓存键名
        - value (Any): 哈希缓存值

        返回:
        - bool: 如果设置哈希缓存成功则返回True,否则返回False
        """
        try:
            self.redis.hset(name=name, key=key, value=value)
            return True
        except Exception as e:
            log.error(f"设置哈希缓存失败: {e!s}")
            return False

    async def hash_get(self, name: str, keys: list[str]) -> Awaitable[list[Any]] | list[Any]:
        """获取哈希缓存

        参数:
        - name (str): 哈希缓存名称
        - keys (list[str]): 哈希缓存键名列表

        返回:
        - Awaitable[list[Any]] | list[Any]: 返回哈希缓存值列表,如果获取失败则返回空列表
        """
        try:
            data = self.redis.hmget(name=name, keys=keys)
            return data
        except Exception as e:
            log.error(f"获取哈希缓存失败: {e!s}")
            return []
