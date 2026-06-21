import json
from dataclasses import dataclass

from fastapi import Query

from app.common.enums import QueueEnum
from app.core.validator import DateTimeStr


@dataclass
class QueryParam:
    """公共基类 —— 自动按 MRO 链式调用所有 __post_init__，子类无需 super()"""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        # 收集 MRO 中除 QueryParam 自身外所有显式定义的 __post_init__
        hooks: list = [_unwrap_query_defaults]
        for base in cls.__mro__:
            fn = base.__dict__.get("__post_init__")
            if callable(fn) and fn is not QueryParam.__post_init__:
                hooks.append(fn)

        hooks.reverse()  # MRO 顺序（_unwrap → 父类 → 子类）

        def chained_post_init(self: object) -> None:
            for hook in hooks:
                hook(self)

        cls.__post_init__ = chained_post_init

    def __post_init__(self) -> None:
        pass


def _unwrap_query_defaults(self: object) -> None:
    """将 @dataclass 字段中残留的 FastAPI Query(...) 默认值替换为 None"""
    for f in self.__dataclass_fields__:  # type: ignore[attr-defined]
        raw = getattr(self, f)
        if raw is not None and type(raw).__name__ == "Query":
            setattr(self, f, None)


@dataclass
class PaginationQueryParam(QueryParam):
    """分页 —— 自动继承 page_no / page_size / order_by，子类无需重复声明"""

    page_no: int = Query(default=1, description="当前页码", ge=1)
    page_size: int = Query(default=10, description="每页数量", ge=1, le=100)
    order_by: str | None = Query(
        default=None,
        description="排序字段,格式:[{'field1': 'asc'}, {'field2': 'desc'}]",
    )

    def __post_init__(self) -> None:
        if self.order_by and isinstance(self.order_by, str):
            try:
                self.order_by = json.loads(self.order_by)
            except ValueError:
                self.order_by = [{"id": "desc"}]
        else:
            self.order_by = [{"id": "desc"}]


@dataclass
class BaseQueryParam(QueryParam):
    """created_time + updated_time —— 子类自动继承"""

    created_time: list[DateTimeStr] | None = Query(
        None,
        description="创建时间范围",
        examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
    )
    updated_time: list[DateTimeStr] | None = Query(
        None,
        description="更新时间范围",
        examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
    )

    def __post_init__(self) -> None:
        ct = self.created_time
        if isinstance(ct, list) and len(ct) == 2:
            self.created_time = (QueueEnum.between.value, (ct[0], ct[1]))
        ut = self.updated_time
        if isinstance(ut, list) and len(ut) == 2:
            self.updated_time = (QueueEnum.between.value, (ut[0], ut[1]))


@dataclass
class UserByQueryParam(QueryParam):
    """created_id + updated_id —— 子类自动继承"""

    created_id: int | None = Query(None, description="创建人")
    updated_id: int | None = Query(None, description="更新人")

    def __post_init__(self) -> None:
        if isinstance(self.created_id, int):
            self.created_id = (QueueEnum.eq.value, self.created_id)
        if isinstance(self.updated_id, int):
            self.updated_id = (QueueEnum.eq.value, self.updated_id)


@dataclass
class TenantByQueryParam(QueryParam):
    """tenant_id —— 子类自动继承"""

    tenant_id: int | None = Query(None, description="租户ID")

    def __post_init__(self) -> None:
        if isinstance(self.tenant_id, int):
            self.tenant_id = (QueueEnum.eq.value, self.tenant_id)
