from collections.abc import Sequence
from typing import TYPE_CHECKING

from sqlalchemy import Inspector, inspect, select, text

from app.api.v1.module_system.auth.schema import AuthSchema
from app.config.setting import settings
from app.core.base_crud import CRUDBase
from app.core.logger import log

from .model import GenTableColumnModel, GenTableModel
from .schema import (
    GenDBTableSchema,
    GenTableColumnOutSchema,
    GenTableColumnSchema,
    GenTableQueryParam,
    GenTableSchema,
)

if TYPE_CHECKING:
    from sqlalchemy.engine.reflection import Inspector


class GenTableCRUD(CRUDBase[GenTableModel, GenTableSchema, GenTableSchema]):
    """代码生成业务表模块数据库操作层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化CRUD操作层

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=GenTableModel, auth=auth)

    async def get_gen_table_by_id(
        self, table_id: int, preload: list | None = None
    ) -> GenTableModel | None:
        """
        根据业务表ID获取需要生成的业务表信息。

        参数:
        - table_id (int): 业务表ID。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - GenTableModel | None: 业务表信息对象。
        """
        return await self.get(id=table_id, preload=preload)

    async def get_gen_table_by_name(
        self, table_name: str, preload: list | None = None
    ) -> GenTableModel | None:
        """
        根据业务表名称获取需要生成的业务表信息。

        参数:
        - table_name (str): 业务表名称。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - GenTableModel | None: 业务表信息对象。
        """
        return await self.get(table_name=table_name, preload=preload)

    async def get_gen_table_all(self, preload: list | None = None) -> Sequence[GenTableModel]:
        """
        获取所有业务表信息。

        参数:
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[GenTableModel]: 所有业务表信息列表。
        """
        return await self.list(preload=preload)

    async def get_gen_table_list(
        self,
        search: GenTableQueryParam | None = None,
        preload: list | None = None,
    ) -> Sequence[GenTableModel]:
        """
        根据查询参数获取代码生成业务表列表信息。

        参数:
        - search (GenTableQueryParam | None): 查询参数对象。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[GenTableModel]: 业务表列表信息。
        """
        return await self.list(
            search=search.__dict__,
            order_by=[{"created_time": "desc"}],
            preload=preload,
        )

    async def add_gen_table(self, add_model: GenTableSchema) -> GenTableModel:
        """
        新增业务表信息。

        参数:
        - add_model (GenTableSchema): 新增业务表信息模型。

        返回:
        - GenTableModel: 新增的业务表信息对象。
        """
        return await self.create(data=add_model)

    async def edit_gen_table(self, table_id: int, edit_model: GenTableSchema) -> GenTableModel:
        """
        修改业务表信息。

        参数:
        - table_id (int): 业务表ID。
        - edit_model (GenTableSchema): 修改业务表信息模型。

        返回:
        - GenTableSchema: 修改后的业务表信息模型。
        """
        # 排除嵌套对象字段，避免SQLAlchemy尝试直接将字典设置到模型实例上
        return await self.update(
            id=table_id,
            data=edit_model.model_dump(exclude_unset=True, exclude={"columns"}),
        )

    async def delete_gen_table(self, ids: list[int]) -> None:
        """
        删除业务表信息。除了系统表。

        参数:
        - ids (list[int]): 业务表ID列表。
        """
        await self.delete(ids=ids)

    async def get_db_table_list(self, search: GenTableQueryParam | None = None) -> list[dict]:
        """
        根据查询参数获取数据库表列表信息。

        参数:
        - search (GenTableQueryParam | None): 查询参数对象。

        返回:
        - list[dict]: 数据库表列表信息（已转为可序列化字典）。
        """
        database_name = settings.DATABASE_NAME
        database_type = settings.DATABASE_TYPE

        from app.core.database import engine

        inspector: Inspector = inspect(engine)
        table_names = inspector.get_table_names()

        dict_data = []
        for table_name in table_names:
            try:
                table_comment = inspector.get_table_comment(table_name)
                comment = (
                    table_comment.get("text", "")
                    if isinstance(table_comment, dict)
                    else table_comment
                )
                table_comment = comment or ""
            except Exception as e:
                log.warning(f"获取表 {table_name} 的注释失败: {e}")
                table_comment = ""

            # 统一处理 search 为 None 的情况，避免重复判断
            if search:
                # 表名过滤：忽略大小写，支持模糊匹配
                if search.table_name and search.table_name.lower() not in table_name.lower():
                    continue
                # 表注释过滤：忽略大小写，支持模糊匹配；table_comment 为 None 时视为空字符串
                if search.table_comment and search.table_comment not in table_comment:
                    continue

            table_info = {
                "database_name": database_name,
                "table_name": table_name,
                "table_type": database_type,
                "table_comment": table_comment,
            }

            dict_data.append(GenDBTableSchema(**table_info).model_dump())

        return dict_data

    async def get_db_table_list_by_names(self, table_names: list[str]) -> list[GenDBTableSchema]:
        """
        根据业务表名称列表获取数据库表信息。

        参数:
        - table_names (list[str]): 业务表名称列表。

        返回:
        - list[GenDBTableSchema]: 数据库表信息对象列表。
        """
        # 处理空列表情况
        if not table_names:
            return []
        # 调用get_db_table_list获取所有表信息
        all_tables = await self.get_db_table_list()

        # 过滤出指定名称的表
        table_names_set = set(table_names)  # 转换为集合以提高查找效率
        filtered_tables = [
            GenDBTableSchema(**table)
            for table in all_tables
            if table["table_name"] in table_names_set
        ]

        return filtered_tables

    async def check_table_exists(self, table_name: str) -> bool:
        """
        检查数据库中是否已存在指定表名的表。

        参数:
        - table_name (str): 要检查的表名。

        返回:
        - bool: 如果表存在返回True，否则返回False。
        """
        from app.core.database import engine

        inspector: Inspector = inspect(engine)
        return inspector.has_table(table_name)

    async def execute_sql(self, sql: str) -> bool:
        """
        执行SQL语句。

        参数:
        - sql (str): 要执行的SQL语句。

        返回:
        - bool: 是否执行成功。
        """
        try:
            # 执行SQL但不手动提交事务，由框架管理事务生命周期
            await self.auth.db.execute(text(sql))
            return True
        except Exception as e:
            log.error(f"执行SQL时发生错误: {e}")
            return False


class GenTableColumnCRUD(CRUDBase[GenTableColumnModel, GenTableColumnSchema, GenTableColumnSchema]):
    """代码生成业务表字段模块数据库操作层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化CRUD操作层

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=GenTableColumnModel, auth=auth)

    @staticmethod
    def _sync_get_table_columns(database_type: str, table_name: str) -> list[dict]:
        """
        同步函数：获取数据库表的列信息

        参数:
        - database_type: 数据库类型
        - table_name: 表名

        返回:
        - list: 列信息列表
        """
        # 使用SQLAlchemy Inspector获取表列信息
        from app.core.database import engine

        inspector: Inspector = inspect(engine)

        # 获取列信息
        columns = inspector.get_columns(table_name)

        # 获取主键信息
        try:
            pk_constraint = inspector.get_pk_constraint(table_name)
            primary_keys = (
                set(pk_constraint.get("constrained_columns", [])) if pk_constraint else set()
            )
        except Exception:
            primary_keys = set()

        # 获取唯一约束信息
        unique_columns = set()
        unique_constraints = inspector.get_unique_constraints(table_name)
        for constraint in unique_constraints:
            unique_columns.update(constraint.get("column_names", []))

        # 处理列信息
        columns_list = []
        for idx, column in enumerate(columns):
            # 获取列的基本信息
            column_name = column["name"]
            column_type = str(column["type"])
            is_nullable = column.get("nullable", True)
            column_default = column.get("default", None)
            # 获取列注释（如果有的话）
            column_comment = column.get("comment", "")
            # 判断是否为主键
            is_pk = column_name in primary_keys
            # 判断是否为唯一约束
            is_unique = column_name in unique_columns
            # 判断是否为自增列（基于数据库类型和列类型）
            is_increment = column.get("autoincrement", False) in (True, "auto")
            # 获取列长度（如果适用）
            column_length = None
            # 使用getattr安全地获取length属性，避免访问不存在时抛出AttributeError
            column_length = getattr(column["type"], "length", None)
            if column_length is not None:
                column_length = str(getattr(column["type"], "length", ""))

            # 构造列信息字典
            column_info = {
                "column_name": column_name,
                "column_comment": column_comment or "",
                "column_type": column_type,
                "column_length": column_length or "",
                "column_default": str(column_default) if column_default is not None else "",
                "sort": idx + 1,  # 序号从1开始
                "is_pk": 1 if is_pk else 0,
                "is_increment": 1 if is_increment else 0,
                "is_nullable": 1 if is_nullable else 0,
                "is_unique": 1 if is_unique else 0,
            }

            columns_list.append(column_info)

        return columns_list

    async def get_gen_table_column_by_id(
        self, id: int, preload: list | None = None
    ) -> GenTableColumnModel | None:
        """根据业务表字段ID获取业务表字段信息。

        参数:
        - id (int): 业务表字段ID。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - GenTableColumnModel | None: 业务表字段信息对象。
        """
        return await self.get(id=id, preload=preload)

    async def get_gen_table_column_list_by_table_id(
        self, table_id: int, preload: list | None = None
    ) -> GenTableColumnModel | None:
        """根据业务表ID获取业务表字段列表信息。

        参数:
        - table_id (int): 业务表ID。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - GenTableColumnModel | None: 业务表字段列表信息对象。
        """
        return await self.get(table_id=table_id, preload=preload)

    async def list_gen_table_column_crud_by_table_id(
        self,
        table_id: int,
        order_by: list | None = None,
        preload: list | None = None,
    ) -> Sequence[GenTableColumnModel]:
        """根据业务表ID查询业务表字段列表。

        参数:
        - table_id (int): 业务表ID。
        - order_by (list | None): 排序字段列表，每个元素为{"field": "字段名", "order": "asc" | "desc"}。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[GenTableColumnModel]: 业务表字段列表信息对象序列。
        """
        return await self.list(search={"table_id": table_id}, order_by=order_by, preload=preload)

    async def get_gen_db_table_columns_by_name(
        self, table_name: str | None
    ) -> list[GenTableColumnOutSchema]:
        """
        根据业务表名称获取业务表字段列表信息。

        参数:
        - table_name (str | None): 业务表名称。

        返回:
        - list[GenTableColumnOutSchema]: 业务表字段列表信息对象。
        """
        # 检查表名是否为空
        if not table_name:
            raise ValueError("数据表名称不能为空")

        try:
            # 直接调用同步方法获取列信息
            columns_info = GenTableColumnCRUD._sync_get_table_columns(
                settings.DATABASE_TYPE, table_name
            )

            # 转换为GenTableColumnOutSchema对象列表
            columns_list = [GenTableColumnOutSchema(**column_info) for column_info in columns_info]

            return columns_list
        except Exception as e:
            log.error(f"获取表{table_name}的字段列表时出错: {e!s}")
            # 确保即使出错也返回空列表而不是None
            raise

    async def list_gen_table_column_crud(
        self,
        search: dict | None = None,
        order_by: list | None = None,
        preload: list | None = None,
    ) -> Sequence[GenTableColumnModel]:
        """根据业务表字段查询业务表字段列表。

        参数:
        - search (dict | None): 查询参数，例如{"table_id": 1}。
        - order_by (list | None): 排序字段列表，每个元素为{"field": "字段名", "order": "asc" | "desc"}。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[GenTableColumnModel]: 业务表字段列表信息对象序列。
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def create_gen_table_column_crud(
        self, data: GenTableColumnSchema
    ) -> GenTableColumnModel | None:
        """创建业务表字段。

        参数:
        - data (GenTableColumnSchema): 业务表字段模型。

        返回:
        - GenTableColumnModel | None: 业务表字段列表信息对象。
        """
        return await self.create(data=data)

    async def update_gen_table_column_crud(
        self, id: int, data: GenTableColumnSchema
    ) -> GenTableColumnModel | None:
        """更新业务表字段。

        参数:
        - id (int): 业务表字段ID。
        - data (GenTableColumnSchema): 业务表字段模型。

        返回:
        - GenTableColumnModel | None: 业务表字段列表信息对象。
        """
        # 将对象转换为字典，避免SQLAlchemy直接操作对象时出现的状态问题
        data_dict = data.model_dump(exclude_unset=True)
        return await self.update(id=id, data=data_dict)

    async def delete_gen_table_column_by_table_id_crud(self, table_ids: list[int]) -> None:
        """根据业务表ID批量删除业务表字段。

        参数:
        - table_ids (list[int]): 业务表ID列表。

        返回:
        - None
        """
        # 先查询出这些表ID对应的所有字段ID
        query = select(GenTableColumnModel.id).where(GenTableColumnModel.table_id.in_(table_ids))
        result = await self.auth.db.execute(query)
        column_ids = [row[0] for row in result.fetchall()]

        # 如果有字段ID，则删除这些字段
        if column_ids:
            await self.delete(ids=column_ids)

    async def delete_gen_table_column_by_column_id_crud(self, column_ids: list[int]) -> None:
        """根据业务表字段ID批量删除业务表字段。

        参数:
        - column_ids (list[int]): 业务表字段ID列表。

        返回:
        - None
        """
        return await self.delete(ids=column_ids)
