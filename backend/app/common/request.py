from typing import Any

from app.common.enums import RET
from app.core.base_schema import PageResultSchema
from app.core.exceptions import CustomException


class PaginationService:
    """分页服务类（仅用于无法 SQL OFFSET/LIMIT 的数据源，如 Redis、本地文件列表、ORM 反射全量表名等）。"""

    @staticmethod
    async def paginate(
        data_list: list[Any],
        page_no: int | None = None,
        page_size: int | None = None,
    ) -> Any:
        """对已在内存中的列表做切片分页。
        关系型表列表请使用 CRUDBase.page（数据库分页）。

        参数:
        - data_list (list[Any]): 原始数据列表。
        - page_no (int | None): 当前页码，默认 None。
        - page_size (int | None): 每页数据量，默认 None。

        返回:
        - PageResultSchema[Any]: 分页结果对象。

        异常:
        - CustomException: 当分页参数不合法时抛出。
        """
        total = len(data_list)

        # 设置默认值
        if page_no is None:
            page_no = 1
        if page_size is None:
            page_size = 10

        # 验证分页参数
        if page_no < 1 or page_size < 1:
            raise CustomException(code=RET.ERROR.code, msg="分页参数不合法")

        # 计算起始索引和结束索引
        start = (page_no - 1) * page_size
        end = min(start + page_size, total)

        # 根据计算得到的起始索引和结束索引对数据列表进行切片
        paginated_data = data_list[start:end]

        # 判断是否有下一页
        has_next = end < total

        return PageResultSchema(
            items=paginated_data,
            total=total,
            page_no=page_no,
            page_size=page_size,
            has_next=has_next,
        )
