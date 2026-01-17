import json

from redis.asyncio.client import Redis

from app.common.enums import RedisInitKeyConfig
from app.core.logger import log
from app.core.redis_crud import RedisCURD
from app.core.security import decode_access_token

from .schema import OnlineQueryParam


class OnlineService:
    """在线用户管理模块服务层"""

    @classmethod
    async def get_online_list_service(
        cls, redis: Redis, search: OnlineQueryParam | None = None
    ) -> list[dict]:
        """
        获取在线用户列表信息（支持分页和搜索）

        参数:
        - redis (Redis): Redis异步客户端实例。
        - search (OnlineQueryParam | None): 查询参数模型。

        返回:
        - list[dict]: 在线用户详情字典列表。
        """

        keys = await RedisCURD(redis).get_keys(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:*")
        tokens = await RedisCURD(redis).mget(keys)

        online_users = []
        for token in tokens:
            if not token:
                continue
            try:
                payload = decode_access_token(token=token)
                session_info = json.loads(payload.sub)
                if cls._match_search_conditions(session_info, search):
                    online_users.append(session_info)
            except Exception as e:
                log.error(f"解析在线用户数据失败: {e}")
                continue
        # 按照 login_time 倒序排序
        online_users.sort(key=lambda x: x.get("login_time", ""), reverse=True)

        return online_users

    @classmethod
    async def delete_online_service(cls, redis: Redis, session_id: str) -> bool:
        """
        强制下线指定在线用户

        参数:
        - redis (Redis): Redis异步客户端实例。
        - session_id (str): 在线用户会话ID。

        返回:
        - bool: 如果操作成功则返回True，否则返回False。
        """
        # 删除 token
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}")

        log.info(f"强制下线用户会话: {session_id}")
        return True

    @classmethod
    async def clear_online_service(cls, redis: Redis) -> bool:
        """
        强制下线所有在线用户

        参数:
        - redis (Redis): Redis异步客户端实例。

        返回:
        - bool: 如果操作成功则返回True，否则返回False。
        """
        # 删除 token
        await RedisCURD(redis).clear(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:*")
        await RedisCURD(redis).clear(f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:*")

        log.info("清除所有在线用户会话成功")
        return True

    @staticmethod
    def _match_search_conditions(online_info: dict, search: OnlineQueryParam | None = None) -> bool:
        """
        检查是否匹配搜索条件

        参数:
        - online_info (dict): 在线用户信息字典。
        - search (OnlineQueryParam | None): 查询参数模型。

        返回:
        - bool: 如果匹配则返回True，否则返回False。
        """
        if not search:
            return True

        if search.name and search.name[1]:
            keyword = search.name[1].strip("%")
            if keyword.lower() not in online_info.get("name", "").lower():
                return False

        if search.ipaddr and search.ipaddr[1]:
            keyword = search.ipaddr[1].strip("%")
            if keyword not in online_info.get("ipaddr", ""):
                return False

        if search.login_location and search.login_location[1]:
            keyword = search.login_location[1].strip("%")
            if keyword.lower() not in online_info.get("login_location", "").lower():
                return False

        return True
