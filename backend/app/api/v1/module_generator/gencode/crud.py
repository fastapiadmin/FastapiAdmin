# -*- coding: utf-8 -*-

from sqlalchemy.engine.row import Row
from sqlalchemy import and_, select, text
from typing import Sequence
from sqlglot.expressions import Expression

from app.core.logger import log
from app.config.setting import settings
from app.core.base_crud import CRUDBase

from app.api.v1.module_system.auth.schema import AuthSchema
from .model import GenTableModel, GenTableColumnModel
from .schema import (
    GenTableSchema,
    GenTableColumnSchema,
    GenTableColumnOutSchema,
    GenDBTableSchema,
    GenTableQueryParam
)


class GenTableCRUD(CRUDBase[GenTableModel, GenTableSchema, GenTableSchema]):
    """代码生成业务表模块数据库操作层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化CRUD操作层

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=GenTableModel, auth=auth)

    async def get_gen_table_by_id(self, table_id: int, preload: list | None = None) -> GenTableModel | None:
        """
        根据业务表ID获取需要生成的业务表信息。

        参数:
        - table_id (int): 业务表ID。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - GenTableModel | None: 业务表信息对象。
        """
        return await self.get(id=table_id, preload=preload)

    async def get_gen_table_by_name(self, table_name: str, preload: list | None = None) -> GenTableModel | None:
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

    async def get_gen_table_list(self, search: GenTableQueryParam | None = None, preload: list | None = None) -> Sequence[GenTableModel]:
        """
        根据查询参数获取代码生成业务表列表信息。

        参数:
        - search (GenTableQueryParam | None): 查询参数对象。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[GenTableModel]: 业务表列表信息。
        """
        return await self.list(search=search.__dict__, order_by=[{"created_time": "desc"}], preload=preload)

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
        return await self.update(id=table_id, data=edit_model.model_dump(exclude_unset=True, exclude={"columns"}))

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

        # 使用更健壮的方式检测数据库方言
        if settings.DATABASE_TYPE == "postgres":
            query_sql = (
                select(
                    text("t.table_catalog as database_name"),
                    text("t.table_name as table_name"),
                    text("t.table_type as table_type"),
                    text("pd.description as table_comment"),
                )
                .select_from(text(
                    "information_schema.tables t \n"
                    "LEFT JOIN pg_catalog.pg_class c ON c.relname = t.table_name \n"
                    "LEFT JOIN pg_catalog.pg_namespace n ON n.nspname = t.table_schema AND c.relnamespace = n.oid \n"
                    "LEFT JOIN pg_catalog.pg_description pd ON pd.objoid = c.oid AND pd.objsubid = 0"
                ))
                .where(
                    and_(
                        text("t.table_catalog = (select current_database())"),
                        text("t.is_insertable_into = 'YES'"),
                        text("t.table_schema = 'public'"),
                    )
                )
            )
        else:
            query_sql = (
                select(
                    text("table_schema as database_name"),
                    text("table_name as table_name"),
                    text("table_type as table_type"),
                    text("table_comment as table_comment"),
                )
                .select_from(text("information_schema.tables"))
                .where(
                    and_(
                        text("table_schema = (select database())"),
                    )
                )
            )
        
        # 动态条件构造
        params = {}
        if search and search.table_name:
            query_sql = query_sql.where(
                text("lower(table_name) like lower(:table_name)")
            )
            params['table_name'] = f"%{search.table_name}%"
        if search and search.table_comment:
            # 对于PostgreSQL，表注释字段是pd.description，而不是table_comment
            if settings.DATABASE_TYPE == "postgres":
                query_sql = query_sql.where(
                    text("lower(pd.description) like lower(:table_comment)")
                )
            else:
                query_sql = query_sql.where(
                    text("lower(table_comment) like lower(:table_comment)")
                )
            params['table_comment'] = f"%{search.table_comment}%"

        # 执行查询并绑定参数
        all_data = (await self.auth.db.execute(query_sql, params)).fetchall()

        # 将Row对象转换为字典列表，解决JSON序列化问题
        dict_data = []
        for row in all_data:
            # 检查row是否为Row对象
            if isinstance(row, Row):
                # 使用._mapping获取字典
                dict_row = GenDBTableSchema(**dict(row._mapping)).model_dump()
                dict_data.append(dict_row)
            else:
                dict_row = GenDBTableSchema(**dict(row)).model_dump()
                dict_data.append(dict_row)
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
            
        # 使用更健壮的方式检测数据库方言
        if settings.DATABASE_TYPE == "postgres":
            # PostgreSQL使用ANY操作符和正确的参数绑定
            query_sql = """
            SELECT
                t.table_catalog as database_name,
                t.table_name as table_name,
                t.table_type as table_type,
                pd.description as table_comment
            FROM
                information_schema.tables t
            LEFT JOIN pg_catalog.pg_class c ON c.relname = t.table_name
            LEFT JOIN pg_catalog.pg_namespace n ON n.nspname = t.table_schema AND c.relnamespace = n.oid
            LEFT JOIN pg_catalog.pg_description pd ON pd.objoid = c.oid AND pd.objsubid = 0
            WHERE
                t.table_catalog = (select current_database()) 
                AND t.is_insertable_into = 'YES'
                AND t.table_schema = 'public'
                AND t.table_name = ANY(:table_names)
            """
        else:
            query_sql = """
            SELECT
                table_schema as database_name,
                table_name as table_name,
                table_type as table_type,
                table_comment as table_comment
            FROM
                information_schema.tables
            WHERE
                table_schema = (select database())
                AND table_name IN :table_names
            """
        
        # 创建新的数据库会话上下文来执行查询，避免受外部事务状态影响
        try:
            # 去重表名列表，避免重复查询
            unique_table_names = list(set(table_names))
            
            # 使用只读事务执行查询，不影响主事务
            if settings.DATABASE_TYPE == "postgres":
                gen_db_table_list = (await self.auth.db.execute(text(query_sql), {"table_names": unique_table_names})).fetchall()
            else:
                gen_db_table_list = (await self.auth.db.execute(text(query_sql), {"table_names": tuple(unique_table_names)})).fetchall()
        except Exception as e:
            log.error(f"查询表信息时发生错误: {e}")
            # 查询错误时直接抛出，不需要事务处理
            raise
        
        # 将Row对象转换为字典列表，解决JSON序列化问题
        dict_data = []
        for row in gen_db_table_list:
            # 检查row是否为Row对象
            if isinstance(row, Row):
                # 使用._mapping获取字典
                dict_row = GenDBTableSchema(**dict(row._mapping))
                dict_data.append(dict_row)
            else:
                dict_row = GenDBTableSchema(**dict(row))
                dict_data.append(dict_row)
        return dict_data

    async def check_table_exists(self, table_name: str) -> bool:
        """
        检查数据库中是否已存在指定表名的表。
        
        参数:
        - table_name (str): 要检查的表名。
        
        返回:
        - bool: 如果表存在返回True，否则返回False。
        """
        try:
            # 根据不同数据库类型使用不同的查询方式
            if settings.DATABASE_TYPE.lower() == 'mysql':
                query = text("SELECT 1 FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = :table_name")
            else:
                query = text("SELECT 1 FROM pg_tables WHERE tablename = :table_name")
            
            result = await self.auth.db.execute(query, {"table_name": table_name})
            return result.scalar() is not None
        except Exception as e:
            log.error(f"检查表格存在性时发生错误: {e}")
            # 出错时返回False，避免误报表已存在
            return False
            
    async def create_table_by_sql(self, sql_statements: list[Expression | None]) -> bool:
        """
        根据SQL语句创建表结构。

        参数:
        - sql (str): 创建表的SQL语句。

        返回:
        - bool: 是否创建成功。
        """
        try:
            # 执行SQL但不手动提交事务，由框架管理事务生命周期
            for sql_statement in sql_statements:
                if not sql_statement:
                    continue
                sql = sql_statement.sql(dialect=settings.DATABASE_TYPE)
                await self.auth.db.execute(text(sql))
            return True
        except Exception as e:
            log.error(f"创建表时发生错误: {e}")
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

    async def get_gen_table_column_by_id(self, id: int, preload: list | None = None) -> GenTableColumnModel | None:
        """根据业务表字段ID获取业务表字段信息。

        参数:
        - id (int): 业务表字段ID。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - GenTableColumnModel | None: 业务表字段信息对象。
        """
        return await self.get(id=id, preload=preload)
    
    async def get_gen_table_column_list_by_table_id(self, table_id: int, preload: list | None = None) -> GenTableColumnModel | None:
        """根据业务表ID获取业务表字段列表信息。

        参数:
        - table_id (int): 业务表ID。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - GenTableColumnModel | None: 业务表字段列表信息对象。
        """
        return await self.get(table_id=table_id, preload=preload)
    
    async def list_gen_table_column_crud_by_table_id(self, table_id: int, order_by: list | None = None, preload: list | None = None) -> Sequence[GenTableColumnModel]:
        """根据业务表ID查询业务表字段列表。

        参数:
        - table_id (int): 业务表ID。
        - order_by (list | None): 排序字段列表，每个元素为{"field": "字段名", "order": "asc" | "desc"}。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[GenTableColumnModel]: 业务表字段列表信息对象序列。
        """
        return await self.list(search={"table_id": table_id}, order_by=order_by, preload=preload)

    async def get_gen_db_table_columns_by_name(self, table_name: str | None) -> list[GenTableColumnOutSchema]:
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
            if settings.DATABASE_TYPE == "mysql":
                query_sql = """
                    SELECT
                        c.column_name AS column_name,
                        c.column_comment AS column_comment,
                        c.column_type AS column_type,
                        c.character_maximum_length AS column_length,
                        c.column_default AS column_default,
                        c.ordinal_position AS sort,
                        (CASE WHEN c.column_key = 'PRI' THEN 1 ELSE 0 END) AS is_pk,
                        (CASE WHEN c.extra = 'auto_increment' THEN 1 ELSE 0 END) AS is_increment,
                        (CASE WHEN (c.is_nullable = 'NO' AND c.column_key != 'PRI') THEN 1 ELSE 0 END) AS is_nullable,
                        (CASE 
                            WHEN c.column_name IN (
                                SELECT k.column_name
                                FROM information_schema.key_column_usage k
                                JOIN information_schema.table_constraints t
                                ON k.constraint_name = t.constraint_name
                                WHERE k.table_schema = c.table_schema
                                AND k.table_name = c.table_name
                                AND t.constraint_type = 'UNIQUE'
                            ) THEN 1 ELSE 0 
                        END) AS is_unique
                    FROM 
                        information_schema.columns c
                    WHERE c.table_schema = (SELECT DATABASE())
                        AND c.table_name = :table_name
                    ORDER BY 
                        c.ordinal_position
                """
            else:
                query_sql = """
                    SELECT
                        c.column_name AS column_name,
                        COALESCE(pgd.description, '') AS column_comment,
                        c.udt_name AS column_type,
                        c.character_maximum_length AS column_length,
                        c.column_default AS column_default,
                        c.ordinal_position AS sort,
                        (CASE WHEN EXISTS (
                            SELECT 1 FROM information_schema.table_constraints tc
                            JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
                            WHERE tc.table_name = c.table_name
                            AND tc.constraint_type = 'PRIMARY KEY'
                            AND ccu.column_name = c.column_name
                        ) THEN 1 ELSE 0 END) AS is_pk,
                        (CASE WHEN c.column_default LIKE 'nextval%' THEN 1 ELSE 0 END) AS is_increment,
                        (CASE WHEN c.is_nullable = 'NO' THEN 1 ELSE 0 END) AS is_nullable,
                        (CASE WHEN EXISTS (
                            SELECT 1 FROM information_schema.table_constraints tc
                            JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
                            WHERE tc.table_name = c.table_name
                            AND tc.constraint_type = 'UNIQUE'
                            AND ccu.column_name = c.column_name
                        ) THEN 1 ELSE 0 END) AS is_unique
                    FROM
                        information_schema.columns c
                    LEFT JOIN pg_catalog.pg_description pgd ON 
                        pgd.objoid = (SELECT oid FROM pg_class WHERE relname = c.table_name)
                        AND pgd.objsubid = c.ordinal_position
                    WHERE c.table_catalog = current_database()
                        AND c.table_schema = 'public'
                        AND c.table_name = :table_name
                    ORDER BY 
                        c.ordinal_position
                """
            
            query = text(query_sql).bindparams(table_name=table_name)
            result = await self.auth.db.execute(query)
            rows = result.fetchall() if result else []
            
            # 确保rows是可迭代对象
            if not rows:
                return []
            
            columns_list = []
            for row in rows:
                # 防御性编程：检查row是否有足够的元素
                if len(row) >= 10:
                    columns_list.append(
                        GenTableColumnOutSchema(
                            column_name=row[0],
                            column_comment=row[1],
                            column_type=row[2],
                            column_length=str(row[3]) if row[3] is not None else '',
                            column_default=str(row[4]) if row[4] is not None else '',
                            sort=row[5],
                            is_pk=row[6],
                            is_increment=row[7],
                            is_nullable=row[8],
                            is_unique=row[9],
                        )
                    )
            return columns_list
        except Exception as e:
            log.error(f"获取表{table_name}的字段列表时出错: {str(e)}")
            # 确保即使出错也返回空列表而不是None
            raise

    async def list_gen_table_column_crud(self, search: dict | None = None, order_by: list | None = None, preload: list | None = None) -> Sequence[GenTableColumnModel]:
        """根据业务表字段查询业务表字段列表。

        参数:
        - search (dict | None): 查询参数，例如{"table_id": 1}。
        - order_by (list | None): 排序字段列表，每个元素为{"field": "字段名", "order": "asc" | "desc"}。
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[GenTableColumnModel]: 业务表字段列表信息对象序列。
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def create_gen_table_column_crud(self, data: GenTableColumnSchema) -> GenTableColumnModel | None:
        """创建业务表字段。

        参数:
        - data (GenTableColumnSchema): 业务表字段模型。

        返回:
        - GenTableColumnModel | None: 业务表字段列表信息对象。
        """
        return await self.create(data=data)

    async def update_gen_table_column_crud(self, id: int, data: GenTableColumnSchema) -> GenTableColumnModel | None:
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