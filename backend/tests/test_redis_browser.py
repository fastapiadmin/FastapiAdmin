"""Redis 通用键空间浏览（只读）回归测试。

用假 Redis 客户端验证：INFO keyspace 解析、SCAN 分页与 type/ttl 批量获取、
按类型取值与截断、敏感键脱敏、缺失键报错、跨库客户端创建与释放。
"""

from types import SimpleNamespace
from typing import Any

import pytest

from app.core.exceptions import CustomException
from app.modules.monitor.cache import browser as browser_module
from app.modules.monitor.cache.browser import RedisBrowserService, is_sensitive_key


class _FakePipeline:
    def __init__(self, redis: "_FakeRedis") -> None:
        self._redis = redis
        self._ops: list[tuple[str, str]] = []

    async def __aenter__(self) -> "_FakePipeline":
        return self

    async def __aexit__(self, *args: Any) -> bool:
        return False

    def type(self, key: str) -> None:
        self._ops.append(("type", key))

    def ttl(self, key: str) -> None:
        self._ops.append(("ttl", key))

    async def execute(self) -> list[Any]:
        results: list[Any] = []
        for op, key in self._ops:
            results.append(self._redis.types.get(key, "none") if op == "type" else self._redis.ttls.get(key, -1))
        return results


class _FakeRedis:
    def __init__(
        self,
        *,
        keyspace: dict[str, Any] | None = None,
        scan_result: tuple[int, list[str]] = (0, []),
        types: dict[str, str] | None = None,
        ttls: dict[str, int] | None = None,
        values: dict[str, Any] | None = None,
        sizes: dict[str, int] | None = None,
        db: int = 0,
        memory_usage_error: bool = False,
    ) -> None:
        self.keyspace = keyspace or {}
        self.scan_result = scan_result
        self.types = types or {}
        self.ttls = ttls or {}
        self.values = values or {}
        self.sizes = sizes or {}
        self.memory_usage_error = memory_usage_error
        self.connection_pool = SimpleNamespace(connection_kwargs={"db": db})
        self.closed = False
        self.ops: list[tuple[str, Any]] = []

    async def info(self, section: str | None = None) -> dict[str, Any]:
        self.ops.append(("info", section))
        return self.keyspace

    async def scan(self, cursor: int = 0, match: str = "*", count: int = 100) -> tuple[int, list[str]]:
        self.ops.append(("scan", (cursor, match, count)))
        return self.scan_result

    def pipeline(self, transaction: bool = False) -> _FakePipeline:
        self.ops.append(("pipeline", transaction))
        return _FakePipeline(self)

    async def type(self, key: str) -> str:
        self.ops.append(("type", key))
        return self.types.get(key, "none")

    async def ttl(self, key: str) -> int:
        self.ops.append(("ttl", key))
        return self.ttls.get(key, -1)

    async def memory_usage(self, key: str) -> int | None:
        self.ops.append(("memory_usage", key))
        if self.memory_usage_error:
            raise RuntimeError("MEMORY USAGE disabled")
        return self.sizes.get(key)

    async def get(self, key: str) -> Any:
        self.ops.append(("get", key))
        return self.values[key]

    async def hgetall(self, key: str) -> dict[str, Any]:
        self.ops.append(("hgetall", key))
        return self.values[key]

    async def lrange(self, key: str, start: int, end: int) -> list[Any]:
        self.ops.append(("lrange", (key, start, end)))
        return self.values[key][start : end + 1]

    async def sscan(self, key: str, count: int = 200) -> tuple[int, list[Any]]:
        self.ops.append(("sscan", (key, count)))
        return 0, self.values[key]

    async def zrange(self, key: str, start: int, end: int, withscores: bool = False) -> list[Any]:
        self.ops.append(("zrange", (key, start, end)))
        return self.values[key][start : end + 1]

    async def xrange(self, key: str, count: int | None = None) -> list[Any]:
        self.ops.append(("xrange", (key, count)))
        return self.values[key]

    async def aclose(self) -> None:
        self.closed = True


async def test_list_databases_parses_keyspace() -> None:
    redis = _FakeRedis(
        keyspace={
            "db0": "keys=12,expires=3,avg_ttl=0",
            "db1": {"keys": 218, "expires": 22, "avg_ttl": 39276698},
            "db2": "keys=4,expires=0",
            "other": "x",
        }
    )
    result = await RedisBrowserService.list_databases(redis)  # type: ignore[arg-type]
    assert [(item.db, item.keys, item.expires) for item in result] == [
        (0, 12, 3),
        (1, 218, 22),
        (2, 4, 0),
    ]


async def test_scan_keys_returns_meta_and_cursor() -> None:
    redis = _FakeRedis(
        scan_result=(42, ["a:1", "b:2"]),
        types={"a:1": "string", "b:2": "hash"},
        ttls={"a:1": -1, "b:2": 300},
    )
    page = await RedisBrowserService.scan_keys(redis, db=0, pattern="a*", cursor=7, count=50)  # type: ignore[arg-type]
    assert page.cursor == 42
    assert [(item.key, item.type, item.ttl) for item in page.keys] == [("a:1", "string", -1), ("b:2", "hash", 300)]
    assert page.scanned == 2
    assert ("scan", (7, "a*", 50)) in redis.ops


async def test_scan_keys_other_db_uses_temp_client_and_closes(monkeypatch: pytest.MonkeyPatch) -> None:
    created: list[tuple[dict[str, Any], _FakeRedis]] = []

    def _fake_redis_ctor(**kwargs: Any) -> _FakeRedis:
        client = _FakeRedis(scan_result=(0, ["k"]), types={"k": "string"}, ttls={"k": -1}, db=kwargs.get("db", 0))
        created.append((kwargs, client))
        return client

    monkeypatch.setattr(browser_module, "Redis", _fake_redis_ctor)
    base = _FakeRedis(db=0)
    page = await RedisBrowserService.scan_keys(base, db=3, pattern="*")  # type: ignore[arg-type]
    assert page.keys and page.keys[0].key == "k"
    assert created and created[0][0]["db"] == 3, "跨库浏览应按 db=3 新建客户端"
    assert created[0][1].closed is True, "临时客户端用完后必须关闭"


async def test_get_value_string_and_truncation() -> None:
    redis = _FakeRedis(
        types={"plain": "string", "long": "string"},
        ttls={"plain": -1, "long": 60},
        sizes={"plain": 5},
        values={"plain": "hello", "long": "x" * 5000},
    )
    value = await RedisBrowserService.get_value(redis, db=0, key="plain")  # type: ignore[arg-type]
    assert value.value == "hello" and value.truncated is False and value.masked is False
    assert value.size == 5

    long_value = await RedisBrowserService.get_value(redis, db=0, key="long")  # type: ignore[arg-type]
    assert long_value.truncated is True
    assert isinstance(long_value.value, str) and len(long_value.value) <= 4000


async def test_get_value_masks_sensitive_keys() -> None:
    redis = _FakeRedis(
        types={"fastapiadmin:access_token:1": "string"},
        ttls={"fastapiadmin:access_token:1": 120},
        values={"fastapiadmin:access_token:1": "real-token"},
    )
    value = await RedisBrowserService.get_value(redis, db=0, key="fastapiadmin:access_token:1")  # type: ignore[arg-type]
    assert value.masked is True
    assert "real-token" not in str(value.value)
    assert value.ttl == 120
    assert ("get", "fastapiadmin:access_token:1") not in redis.ops, "敏感键不应读取值"


async def test_get_value_missing_key_raises() -> None:
    redis = _FakeRedis(types={})
    with pytest.raises(CustomException):
        await RedisBrowserService.get_value(redis, db=0, key="nope")  # type: ignore[arg-type]


async def test_get_value_hash_list_zset_stream() -> None:
    redis = _FakeRedis(
        types={"h": "hash", "l": "list", "z": "zset", "s": "stream"},
        ttls={"h": -1, "l": -1, "z": -1, "s": -1},
        values={
            "h": {"name": "alice", "role": "admin"},
            "l": ["a", "b", "c"],
            "z": [("m1", 1.5), ("m2", 2)],
            "s": [("1-0", {"level": "INFO"})],
        },
    )
    hash_value = await RedisBrowserService.get_value(redis, db=0, key="h")  # type: ignore[arg-type]
    assert hash_value.value == {"name": "alice", "role": "admin"}
    list_value = await RedisBrowserService.get_value(redis, db=0, key="l")  # type: ignore[arg-type]
    assert list_value.value == ["a", "b", "c"]
    zset_value = await RedisBrowserService.get_value(redis, db=0, key="z")  # type: ignore[arg-type]
    assert zset_value.value == [{"member": "m1", "score": 1.5}, {"member": "m2", "score": 2.0}]
    stream_value = await RedisBrowserService.get_value(redis, db=0, key="s")  # type: ignore[arg-type]
    assert stream_value.value == [{"id": "1-0", "fields": {"level": "INFO"}}]


async def test_get_value_memory_usage_failure_is_tolerated() -> None:
    redis = _FakeRedis(types={"k": "string"}, values={"k": "v"}, memory_usage_error=True)
    value = await RedisBrowserService.get_value(redis, db=0, key="k")  # type: ignore[arg-type]
    assert value.size is None
    assert value.value == "v"


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("fastapiadmin:access_token:1", True),
        ("fastapiadmin:secret:db", True),
        ("user:session:9", True),
        ("sys:config:site_name", False),
        ("task:cronjob:list", False),
    ],
)
def test_is_sensitive_key(key: str, expected: bool) -> None:
    assert is_sensitive_key(key) is expected
