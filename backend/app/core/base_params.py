# -*- coding: utf-8 -*-

from fastapi import Query


class PaginationQueryParam:
    """分页查询参数基类"""

    def __init__(
        self,
        page_no: int = Query(default=1, description="当前页码", ge=1),
        page_size: int = Query(default=10, description="每页数量", ge=1, le=100), 
        order_by: str | None = Query(default=None, description="排序字段,格式:field1,asc;field2,desc"),
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
                self.order_by = []
                for item in order_by.split(';'):
                    if item.strip():
                        field, direction = item.split(',', 1)
                        self.order_by.append({field.strip(): direction.strip().lower()})
            except ValueError:
                # 如果解析失败，使用默认排序
                self.order_by = [{'updated_time': 'desc'}]
        else:
            self.order_by = [{'updated_time': 'desc'}]

