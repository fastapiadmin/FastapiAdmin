"""租户维度的 Redis 缓存键，避免多租户下配置/字典缓存互相覆盖。"""

from app.common.enums import RedisInitKeyConfig


def param_cache_redis_key(tenant_id: int, config_key: str) -> str:
    return f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{tenant_id}:{config_key}"


def dict_cache_redis_key(tenant_id: int, dict_type: str) -> str:
    return f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{tenant_id}:{dict_type}"
