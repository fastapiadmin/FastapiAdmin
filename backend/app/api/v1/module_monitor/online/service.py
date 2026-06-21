import json

from redis.asyncio.client import Redis

from app.common.enums import RedisInitKeyConfig
from app.core.logger import logger
from app.core.redis_crud import RedisCURD
from app.core.security import decode_access_token

from .schema import OnlineQueryParam


class OnlineService:
    """在线用户管理模块服务层"""

    @staticmethod
    async def get_online_list(redis: Redis, search: OnlineQueryParam | None = None) -> list[dict]:
        keys = await RedisCURD(redis).get_keys(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:*")
        tokens = await RedisCURD(redis).mget(keys)

        online_users = []
        for token in tokens:
            if not token:
                continue
            try:
                payload = decode_access_token(token=token)
                session_id = payload.sub

                # 从 Redis 读取完整会话信息
                raw = await RedisCURD(redis).get(
                    f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}"
                )
                if not raw:
                    continue
                session_info = json.loads(raw)

                # 内联搜索匹配逻辑
                if search:
                    if search.name and search.name[1]:
                        kw = search.name[1].strip("%")
                        if kw.lower() not in session_info.get("name", "").lower():
                            continue
                    if search.ipaddr and search.ipaddr[1]:
                        kw = search.ipaddr[1].strip("%")
                        if kw not in session_info.get("ipaddr", ""):
                            continue
                    if search.login_location and search.login_location[1]:
                        kw = search.login_location[1].strip("%")
                        if kw.lower() not in session_info.get("login_location", "").lower():
                            continue

                online_users.append(session_info)
            except Exception as e:
                logger.error(f"解析在线用户数据失败: {e}")
                continue

        online_users.sort(key=lambda x: x.get("login_time", ""), reverse=True)
        return online_users

    @staticmethod
    async def delete_online(redis: Redis, session_id: str) -> None:
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.USER_SESSION.key}:{session_id}")
        logger.info(f"强制下线用户会话: {session_id}")

    @staticmethod
    async def clear_online(redis: Redis) -> None:
        await RedisCURD(redis).clear(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:*")
        await RedisCURD(redis).clear(f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:*")
        await RedisCURD(redis).clear(f"{RedisInitKeyConfig.USER_SESSION.key}:*")
        logger.info("清除所有在线用户会话成功")

