import json

from fastapi import Query

from app.core.validator import DateTimeStr


class PaginationQueryParam:
    """分页查询参数基类"""

    def __init__(
        self,
        page_no: int = Query(default=1, description="当前页码", ge=1),
        page_size: int = Query(default=10, description="每页数量", ge=1, le=100),
        order_by: str | None = Query(
            default=None,
            description="排序字段,格式:[{'field1': 'asc'}, {'field2': 'desc'}]",
        ),
    ) -> None:
        """
        初始化分页查询参数。

        参数:
        - page_no (int | None): 当前页码，默认 None。
        - page_size (int | None): 每页数量，默认 None，最大 100。
        - order_by (str | None): 排序字段，格式 'field,asc;field2,desc'。

        返回:
        - None
        """
        self.page_no = page_no
        self.page_size = page_size
        # 将字符串格式的order_by转换为服务层需要的List[Dict[str, str]]格式
        if order_by:
            try:
                self.order_by = json.loads(order_by)
            except ValueError:
                # 如果解析失败，使用默认排序
                self.order_by = [{"updated_time": "desc"}]
        else:
            self.order_by = [{"updated_time": "desc"}]


class BaseQueryParam:
    """公共查询参数"""

    def __init__(
        self,
        description: str | None = Query(None, description="描述"),
        status: str | None = Query(None, description="是否启用"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        updated_time: list[DateTimeStr] | None = Query(
            None,
            description="更新时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        *args,
        **kwargs,
    ) -> None:
        # 模糊查询字段
        if description:
            self.description = ("like", description)

        # 精确查询字段
        if status:
            self.status = ("eq", status)

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))


class CommonQueryParam:
    """根据用户查询参数"""

    def __init__(
        self,
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:
        if created_id:
            self.created_id = ("eq", created_id)
        if updated_id:
            self.updated_id = ("eq", updated_id)
