import io
import os
import zipfile
from collections.abc import Callable
from typing import Any

import anyio
import sqlglot
from sqlglot.expressions import (
    Add,
    Alter,
    Create,
    Delete,
    Drop,
    Insert,
    Table,
    TruncateTable,
    Update,
)

from app.api.v1.module_system.auth.schema import AuthSchema
from app.config.path_conf import BASE_DIR
from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import GenTableColumnCRUD, GenTableCRUD
from .schema import (
    GenTableColumnOutSchema,
    GenTableColumnSchema,
    GenTableOutSchema,
    GenTableQueryParam,
    GenTableSchema,
)
from .tools.gen_util import GenUtils
from .tools.jinja2_template_util import Jinja2TemplateUtil


def handle_service_exception(func: Callable) -> Callable:
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"{func.__name__}执行失败: {e!s}")

    return wrapper


class GenTableService:
    """代码生成业务表服务层"""

    @classmethod
    @handle_service_exception
    async def get_gen_table_detail_service(cls, auth: AuthSchema, table_id: int) -> dict:
        """获取详细信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_id (int): 业务表ID。

        返回:
        - dict: 包含业务表详细信息的字典。
        """
        gen_table = await cls.get_gen_table_by_id_service(auth, table_id)
        return GenTableOutSchema.model_validate(gen_table).model_dump()

    @classmethod
    @handle_service_exception
    async def get_gen_table_list_service(
        cls, auth: AuthSchema, search: GenTableQueryParam
    ) -> list[dict]:
        """
        获取代码生成业务表列表信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - search (GenTableQueryParam): 查询参数模型。

        返回:
        - list[dict]: 包含业务表列表信息的字典列表。
        """
        gen_table_list_result = await GenTableCRUD(auth=auth).get_gen_table_list(search)
        return [GenTableOutSchema.model_validate(obj).model_dump() for obj in gen_table_list_result]

    @classmethod
    @handle_service_exception
    async def get_gen_db_table_list_service(
        cls, auth: AuthSchema, search: GenTableQueryParam
    ) -> list[Any]:
        """获取数据库表列表。

        参数:
        - auth (AuthSchema): 认证信息。
        - search (GenTableQueryParam): 查询参数模型。

        返回:
        - list[Any]: 包含数据库表列表信息的任意类型列表。
        """
        gen_db_table_list_result = await GenTableCRUD(auth=auth).get_db_table_list(search)
        return gen_db_table_list_result

    @classmethod
    @handle_service_exception
    async def get_gen_db_table_list_by_name_service(
        cls, auth: AuthSchema, table_names: list[str]
    ) -> list[GenTableOutSchema]:
        """根据表名称组获取数据库表信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_names (list[str]): 业务表名称列表。

        返回:
        - list[GenTableOutSchema]: 包含业务表详细信息的模型列表。
        """
        gen_db_table_list_result = await GenTableCRUD(auth).get_db_table_list_by_names(table_names)

        # 修复：将GenDBTableSchema对象转换为字典后再传递给GenTableOutSchema
        result = [
            GenTableOutSchema(**gen_table.model_dump()) for gen_table in gen_db_table_list_result
        ]

        return result

    @classmethod
    @handle_service_exception
    async def import_gen_table_service(
        cls, auth: AuthSchema, gen_table_list: list[GenTableOutSchema]
    ) -> bool:
        """导入表结构到生成器。

        参数:
        - auth (AuthSchema): 认证信息。
        - gen_table_list (list[GenTableOutSchema]): 包含业务表详细信息的模型列表。

        返回:
        - bool: 成功时返回True，失败时抛出异常。
        """
        # 检查是否有表需要导入
        if not gen_table_list:
            raise CustomException(msg="导入的表结构不能为空")
        try:
            for table in gen_table_list:
                table_name = table.table_name
                # 检查表是否已存在
                existing_table = await GenTableCRUD(auth).get_gen_table_by_name(table_name)
                if existing_table:
                    raise CustomException(msg=f"以下表已存在，不能重复导入: {table_name}")
                GenUtils.init_table(table)
                if not table.columns:
                    table.columns = []
                add_gen_table = await GenTableCRUD(auth).add_gen_table(
                    GenTableSchema.model_validate(table.model_dump())
                )
                gen_table_columns = await GenTableColumnCRUD(auth).get_gen_db_table_columns_by_name(
                    table_name
                )
                if len(gen_table_columns) > 0:
                    table.id = add_gen_table.id
                    for column in gen_table_columns:
                        column_schema = GenTableColumnSchema(
                            table_id=table.id,
                            column_name=column.column_name,
                            column_comment=column.column_comment,
                            column_type=column.column_type,
                            column_length=column.column_length,
                            column_default=column.column_default,
                            is_pk=column.is_pk,
                            is_increment=column.is_increment,
                            is_nullable=column.is_nullable,
                            is_unique=column.is_unique,
                            sort=column.sort,
                            python_type=column.python_type,
                            python_field=column.python_field,
                        )
                        GenUtils.init_column_field(column_schema, table)
                        await GenTableColumnCRUD(auth).create_gen_table_column_crud(column_schema)
            return True
        except Exception as e:
            raise CustomException(msg=f"导入失败, {e!s}")

    @classmethod
    @handle_service_exception
    async def create_table_service(cls, auth: AuthSchema, sql: str) -> bool | None:
        """创建表结构并导入至代码生成模块。

        参数:
        - auth (AuthSchema): 认证信息。
        - sql (str): 包含`CREATE TABLE`语句的SQL字符串。

        返回:
        - bool | None: 成功时返回True，失败时抛出异常。
        """
        # 验证SQL非空
        if not sql or not sql.strip():
            raise CustomException(msg="SQL语句不能为空")
        try:
            # 解析SQL语句
            sql_statements = sqlglot.parse(sql, dialect=settings.DATABASE_TYPE)
            if not sql_statements:
                raise CustomException(msg="无法解析SQL语句，请检查SQL语法")

            # 校验sql语句是否为合法的建表语句
            validate_create = [
                isinstance(sql_statement, Create) for sql_statement in sql_statements
            ]
            validate_forbidden_keywords = [
                isinstance(
                    sql_statement,
                    (Add, Alter, Delete, Drop, Insert, TruncateTable, Update),
                )
                for sql_statement in sql_statements
            ]
            if not any(validate_create) or any(validate_forbidden_keywords):
                raise CustomException(msg="sql语句不是合法的建表语句")

            # 获取要创建的表名
            table_names = []
            for sql_statement in sql_statements:
                if isinstance(sql_statement, Create):
                    table = sql_statement.find(Table)
                    if table and table.name:
                        table_names.append(table.name)
            table_names = list(set(table_names))

            # 创建CRUD实例
            gen_table_crud = GenTableCRUD(auth=auth)

            # 检查每个表是否已存在
            for table_name in table_names:
                # 检查数据库中是否已存在该表
                if await gen_table_crud.check_table_exists(table_name):
                    raise CustomException(msg=f"表 {table_name} 已存在，请检查并修改表名后重试")

                # 检查代码生成模块中是否已导入该表
                existing_table = await gen_table_crud.get_gen_table_by_name(table_name)
                if existing_table:
                    raise CustomException(
                        msg=f"表 {table_name} 已在代码生成模块中存在，请检查并修改表名后重试"
                    )

            # 表不存在，执行SQL语句创建表
            for sql_statement in sql_statements:
                if not isinstance(sql_statement, Create):
                    continue
                exc_sql = sql_statement.sql(dialect=settings.DATABASE_TYPE)
                log.info(f"执行SQL语句: {exc_sql}")
                if not await gen_table_crud.execute_sql(exc_sql):
                    raise CustomException(msg=f"执行SQL语句 {exc_sql} 失败，请检查数据库")
            return True

        except Exception as e:
            raise CustomException(msg=f"创建表结构失败: {e!s}")

    @classmethod
    @handle_service_exception
    async def update_gen_table_service(
        cls, auth: AuthSchema, data: GenTableSchema, table_id: int
    ) -> dict[str, Any]:
        """编辑业务表信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - data (GenTableSchema): 包含业务表详细信息的模型。
        - table_id (int): 业务表ID。

        返回:
        - dict[str, Any]: 更新后的业务表信息。
        """
        # 处理params为None的情况
        gen_table_info = await cls.get_gen_table_by_id_service(auth, table_id)
        if gen_table_info.id:
            try:
                # 直接调用edit_gen_table方法，它会在内部处理排除嵌套字段的逻辑
                result = await GenTableCRUD(auth).edit_gen_table(table_id, data)

                # 处理data.columns为None的情况
                if data.columns:
                    for gen_table_column in data.columns:
                        # 确保column有id字段
                        if hasattr(gen_table_column, "id") and gen_table_column.id:
                            column_schema = GenTableColumnSchema(**gen_table_column.model_dump())
                            await GenTableColumnCRUD(auth).update_gen_table_column_crud(
                                gen_table_column.id, column_schema
                            )
                return GenTableOutSchema.model_validate(result).model_dump()
            except Exception as e:
                raise CustomException(msg=str(e))
        else:
            raise CustomException(msg="业务表不存在")

    @classmethod
    @handle_service_exception
    async def delete_gen_table_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除业务表信息（先删字段，再删表）。

        参数:
        - auth (AuthSchema): 认证信息。
        - ids (list[int]): 业务表ID列表。

        返回:
        - None
        """
        # 验证ID列表非空
        if not ids:
            raise CustomException(msg="ID列表不能为空")

        try:
            # 先删除相关的字段信息
            await GenTableColumnCRUD(auth=auth).delete_gen_table_column_by_table_id_crud(ids)
            # 再删除表信息
            await GenTableCRUD(auth=auth).delete_gen_table(ids)
        except Exception as e:
            raise CustomException(msg=str(e))

    @classmethod
    @handle_service_exception
    async def get_gen_table_by_id_service(
        cls, auth: AuthSchema, table_id: int
    ) -> GenTableOutSchema:
        """获取需要生成代码的业务表详细信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_id (int): 业务表ID。

        返回:
        - GenTableOutSchema: 业务表详细信息模型。
        """
        gen_table = await GenTableCRUD(auth=auth).get_gen_table_by_id(table_id)
        if not gen_table:
            raise CustomException(msg="业务表不存在")

        result = GenTableOutSchema.model_validate(gen_table)
        return result

    @classmethod
    @handle_service_exception
    async def get_gen_table_all_service(cls, auth: AuthSchema) -> list[GenTableOutSchema]:
        """获取所有业务表信息（列表）。

        参数:
        - auth (AuthSchema): 认证信息。

        返回:
        - list[GenTableOutSchema]: 业务表详细信息模型列表。
        """
        gen_table_all = await GenTableCRUD(auth=auth).get_gen_table_all() or []
        result = []
        for gen_table in gen_table_all:
            try:
                table_out = GenTableOutSchema.model_validate(gen_table)
                result.append(table_out)
            except Exception as e:
                log.error(f"转换业务表时出错: {e!s}")
                continue
        return result

    @classmethod
    @handle_service_exception
    async def preview_code_service(cls, auth: AuthSchema, table_id: int) -> dict[str, Any]:
        """
        预览代码（根据模板渲染内存结果）。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_id (int): 业务表ID。

        返回:
        - dict[str, Any]: 文件名到渲染内容的映射。
        """
        gen_table = GenTableOutSchema.model_validate(
            await GenTableCRUD(auth).get_gen_table_by_id(table_id)
        )
        await cls.set_pk_column(gen_table)
        env = Jinja2TemplateUtil.get_env()
        context = Jinja2TemplateUtil.prepare_context(gen_table)
        template_list = Jinja2TemplateUtil.get_template_list()
        preview_code_result = {}
        for template in template_list:
            try:
                render_content = await env.get_template(template).render_async(**context)
                preview_code_result[template] = render_content
            except Exception as e:
                log.error(f"渲染模板 {template} 时出错: {e!s}")
                # 即使某个模板渲染失败，也继续处理其他模板
                preview_code_result[template] = f"渲染错误: {e!s}"
        return preview_code_result

    @classmethod
    @handle_service_exception
    async def generate_code_service(cls, auth: AuthSchema, table_name: str) -> bool:
        """生成代码至指定路径（安全写入+可跳过覆盖）。
        - 安全：限制写入在项目根目录内；越界路径自动回退到项目根目录。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_name (str): 业务表名。

        返回:
        - bool: 生成是否成功。
        """
        # 验证表名非空
        if not table_name or not table_name.strip():
            raise CustomException(msg="表名不能为空")
        env = Jinja2TemplateUtil.get_env()
        render_info = await cls.__get_gen_render_info(auth, table_name)
        gen_table_schema: GenTableOutSchema = render_info[3]

        from app.api.v1.module_system.menu.crud import MenuCRUD
        from app.api.v1.module_system.menu.schema import MenuCreateSchema
        from app.utils.common_util import CamelCaseUtil

        # 构建权限前缀
        permission_prefix = f"{gen_table_schema.module_name}:{gen_table_schema.business_name}"
        # 创建菜单 CRUD 实例
        menu_crud = MenuCRUD(auth)
        if not gen_table_schema.business_name:
            raise CustomException(msg="业务名称不能为空")
        if not gen_table_schema.function_name:
            raise CustomException(msg="功能名称不能为空")
        if not gen_table_schema.package_name:
            raise CustomException(msg="包名不能为空")
        # 1. 先检查并创建菜单（目录菜单、功能菜单、按钮权限）
        # 检查是否需要创建目录菜单
        if gen_table_schema.parent_menu_id:
            # 如果传了上级菜单ID（菜单类型=1），则不创建目录菜单，直接使用该ID作为功能菜单的父ID
            dir_menu_id = gen_table_schema.parent_menu_id
        else:
            # 如果没传上级菜单ID，则需要创建新的模块目录菜单（类型=1：目录）
            existing_dir_menu = await menu_crud.get(name=gen_table_schema.business_name)
            if existing_dir_menu:
                dir_menu_id = existing_dir_menu.id
            else:
                dir_parent_menu = await menu_crud.create(
                    MenuCreateSchema(
                        name=gen_table_schema.package_name,
                        type=1,
                        order=9999,
                        permission=None,
                        icon="menu",
                        route_name=CamelCaseUtil.snake_to_camel(gen_table_schema.package_name),
                        route_path=f"/{gen_table_schema.package_name}",
                        component_path=None,
                        redirect=f"/{gen_table_schema.package_name}/{gen_table_schema.business_name}",
                        hidden=False,
                        keep_alive=True,
                        always_show=False,
                        title=gen_table_schema.package_name,
                        params=None,
                        affix=False,
                        parent_id=gen_table_schema.parent_menu_id,  # 这里应该是None，因为上面已经判断过了
                        status="0",
                        description=f"{gen_table_schema.business_name}目录",
                    )
                )
                dir_menu_id = dir_parent_menu.id

        # 检查功能菜单是否已存在，如果存在则抛出错误
        existing_func_menu = await menu_crud.get(name=gen_table_schema.function_name, type=2)
        if existing_func_menu:
            raise CustomException(
                msg=f"功能菜单名称 '{gen_table_schema.function_name}' 已存在，不能重复创建"
            )
        # 创建功能菜单（类型=2：菜单）
        parent_menu = await menu_crud.create(
            MenuCreateSchema(
                name=gen_table_schema.function_name,
                type=2,
                order=9999,
                permission=f"{permission_prefix}:query",
                icon="menu",
                route_name=CamelCaseUtil.snake_to_camel(gen_table_schema.business_name),
                route_path=f"/{gen_table_schema.package_name}/{gen_table_schema.business_name}",
                component_path=f"{gen_table_schema.module_name}/{gen_table_schema.business_name}/index",
                redirect=None,
                hidden=False,
                keep_alive=True,
                always_show=False,
                title=gen_table_schema.function_name,
                params=None,
                affix=False,
                parent_id=dir_menu_id,  # 使用目录菜单ID或用户指定的parent_menu_id作为父ID
                status="0",
                description=f"{gen_table_schema.function_name}功能菜单",
            )
        )
        # 创建按钮权限（类型=3：按钮/权限）
        buttons = [
            {
                "name": f"{gen_table_schema.function_name}查询",
                "permission": f"{permission_prefix}:query",
                "order": 1,
            },
            {
                "name": f"{gen_table_schema.function_name}详情",
                "permission": f"{permission_prefix}:detail",
                "order": 2,
            },
            {
                "name": f"{gen_table_schema.function_name}新增",
                "permission": f"{permission_prefix}:create",
                "order": 3,
            },
            {
                "name": f"{gen_table_schema.function_name}修改",
                "permission": f"{permission_prefix}:update",
                "order": 4,
            },
            {
                "name": f"{gen_table_schema.function_name}删除",
                "permission": f"{permission_prefix}:delete",
                "order": 5,
            },
            {
                "name": f"{gen_table_schema.function_name}批量状态修改",
                "permission": f"{permission_prefix}:patch",
                "order": 6,
            },
            {
                "name": f"{gen_table_schema.function_name}导出",
                "permission": f"{permission_prefix}:export",
                "order": 7,
            },
            {
                "name": f"{gen_table_schema.function_name}导入",
                "permission": f"{permission_prefix}:import",
                "order": 8,
            },
            {
                "name": f"{gen_table_schema.function_name}下载导入模板",
                "permission": f"{permission_prefix}:download",
                "order": 9,
            },
        ]
        for button in buttons:
            # 检查按钮权限是否已存在
            await menu_crud.create(
                MenuCreateSchema(
                    name=button["name"],
                    type=3,
                    order=button["order"],
                    permission=button["permission"],
                    icon=None,
                    route_name=None,
                    route_path=None,
                    component_path=None,
                    redirect=None,
                    hidden=False,
                    keep_alive=True,
                    always_show=False,
                    title=button["name"],
                    params=None,
                    affix=False,
                    parent_id=parent_menu.id,
                    status="0",
                    description=f"{gen_table_schema.function_name}功能按钮",
                )
            )
            log.info(f"成功创建按钮权限: {button['name']}")
        log.info(f"成功创建{gen_table_schema.function_name}菜单及按钮权限")

        # 2. 菜单创建成功后，再生成页面代码
        for template in render_info[0]:
            try:
                render_content = await env.get_template(template).render_async(**render_info[2])

                file_name = Jinja2TemplateUtil.get_file_name(template, gen_table_schema)
                full_path = BASE_DIR.parent.joinpath(file_name)
                gen_path = str(full_path)

                if not gen_path:
                    raise CustomException(msg="【代码生成】生成路径为空")

                # 确保目录存在
                os.makedirs(os.path.dirname(gen_path), exist_ok=True)

                await anyio.Path(gen_path).write_text(render_content, encoding="utf-8")

                module_init_path = BASE_DIR.parent.joinpath(
                    f"backend/app/api/v1/{gen_table_schema.module_name}/__init__.py"
                )
                if not module_init_path.exists():
                    # 创建module_name目录的__init__.py文件
                    os.makedirs(os.path.dirname(module_init_path), exist_ok=True)
                    await anyio.Path(module_init_path).write_text(
                        "# -*- coding: utf-8 -*-", encoding="utf-8"
                    )
            except Exception as e:
                raise CustomException(
                    msg=f"渲染模板失败，表名：{gen_table_schema.table_name}，详细错误信息：{e!s}"
                )

        return True

    @classmethod
    @handle_service_exception
    async def batch_gen_code_service(cls, auth: AuthSchema, table_names: list[str]) -> bytes:
        """
        批量生成代码并打包为ZIP。
        - 备注：内存生成并压缩，兼容多模板类型；供下载使用。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_names (list[str]): 业务表名列表。

        返回:
        - bytes: 包含所有生成代码的ZIP文件内容。
        """
        # 验证表名列表非空
        if not table_names:
            raise CustomException(msg="表名列表不能为空")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for table_name in table_names:
                if not table_name.strip():
                    continue
                try:
                    env = Jinja2TemplateUtil.get_env()
                    render_info = await cls.__get_gen_render_info(auth, table_name)
                    for template_file, output_file in zip(
                        render_info[0], render_info[1], strict=False
                    ):
                        render_content = await env.get_template(template_file).render_async(
                            **render_info[2]
                        )
                        zip_file.writestr(output_file, render_content)
                except Exception as e:
                    log.error(f"批量生成代码时处理表 {table_name} 出错: {e!s}")
                    # 继续处理其他表，不中断整个过程
                    continue
        zip_data = zip_buffer.getvalue()
        zip_buffer.close()
        return zip_data

    @classmethod
    @handle_service_exception
    async def sync_db_service(cls, auth: AuthSchema, table_name: str) -> None:
        """
        同步数据库表结构到业务表。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_name (str): 业务表名。

        返回:
        - None
        """
        # 验证表名非空
        if not table_name or not table_name.strip():
            raise CustomException(msg="表名不能为空")
        gen_table = await GenTableCRUD(auth).get_gen_table_by_name(table_name)
        if not gen_table:
            raise CustomException(msg="业务表不存在")
        table = GenTableOutSchema.model_validate(gen_table)
        if not table.id:
            raise CustomException(msg="业务表ID不能为空")
        table_columns = table.columns or []
        table_column_map = {column.column_name: column for column in table_columns}
        # 确保db_table_columns始终是列表类型，避免None值
        db_table_columns = (
            await GenTableColumnCRUD(auth).get_gen_db_table_columns_by_name(table_name) or []
        )
        db_table_columns = [col for col in db_table_columns if col is not None]
        db_table_column_names = [column.column_name for column in db_table_columns]
        try:
            for column in db_table_columns:
                GenUtils.init_column_field(column, table)
                if column.column_name in table_column_map:
                    prev_column = table_column_map[column.column_name]
                    if hasattr(prev_column, "id") and prev_column.id:
                        column.id = prev_column.id
                    if hasattr(prev_column, "dict_type") and prev_column.dict_type:
                        column.dict_type = prev_column.dict_type
                    if hasattr(prev_column, "query_type") and prev_column.query_type:
                        column.query_type = prev_column.query_type
                    if hasattr(prev_column, "html_type") and prev_column.html_type:
                        column.html_type = prev_column.html_type
                    is_pk_bool = False
                    if hasattr(prev_column, "is_pk"):
                        is_pk_bool = (
                            prev_column.is_pk
                            if isinstance(prev_column.is_pk, bool)
                            else str(prev_column.is_pk) == "1"
                        )
                    if hasattr(prev_column, "is_nullable") and not is_pk_bool:
                        column.is_nullable = prev_column.is_nullable
                    if hasattr(prev_column, "python_field"):
                        column.python_field = prev_column.python_field or column.python_field
                    if hasattr(column, "id") and column.id:
                        await GenTableColumnCRUD(auth).update_gen_table_column_crud(
                            column.id, column
                        )
                    else:
                        await GenTableColumnCRUD(auth).create_gen_table_column_crud(column)
                else:
                    # 设置table_id以确保新字段能正确关联到表
                    column.table_id = table.id
                    await GenTableColumnCRUD(auth).create_gen_table_column_crud(column)
            del_columns = [
                column
                for column in table_columns
                if column.column_name not in db_table_column_names
            ]
            if del_columns:
                for column in del_columns:
                    if hasattr(column, "id") and column.id:
                        await GenTableColumnCRUD(auth).delete_gen_table_column_by_column_id_crud([
                            column.id
                        ])
        except Exception as e:
            raise CustomException(msg=f"同步失败: {e!s}")

    @classmethod
    async def set_pk_column(cls, gen_table: GenTableOutSchema) -> None:
        """设置主键列信息（主表/子表）。
        - 备注：同时兼容`pk`布尔与`is_pk == '1'`字符串两种标识。

        参数:
        - gen_table (GenTableOutSchema): 业务表详细信息模型。

        返回:
        - None
        """
        if gen_table.columns:
            for column in gen_table.columns:
                # 修复：确保正确检查主键标识
                if getattr(column, "pk", False) or getattr(column, "is_pk", "") == "1":
                    gen_table.pk_column = column
                    break
        # 如果没有找到主键列且有列存在，使用第一个列作为主键
        if gen_table.pk_column is None and gen_table.columns:
            gen_table.pk_column = gen_table.columns[0]

    @classmethod
    async def __get_gen_render_info(cls, auth: AuthSchema, table_name: str) -> list[Any]:
        """
        获取生成代码渲染模板相关信息。

        参数:
        - auth (AuthSchema): 认证对象。
        - table_name (str): 业务表名称。

        返回:
        - list[Any]: [模板列表, 输出文件名列表, 渲染上下文, 业务表对象]。

        异常:
        - CustomException: 当业务表不存在或数据转换失败时抛出。
        """
        gen_table_model = await GenTableCRUD(auth=auth).get_gen_table_by_name(table_name)
        # 检查表是否存在
        if gen_table_model is None:
            raise CustomException(msg=f"业务表 {table_name} 不存在")
        gen_table = GenTableOutSchema.model_validate(gen_table_model)
        await cls.set_pk_column(gen_table)
        context = Jinja2TemplateUtil.prepare_context(gen_table)
        template_list = Jinja2TemplateUtil.get_template_list()
        output_files = [
            Jinja2TemplateUtil.get_file_name(template, gen_table) for template in template_list
        ]
        return [template_list, output_files, context, gen_table]


class GenTableColumnService:
    """代码生成业务表字段服务层"""

    @classmethod
    @handle_service_exception
    async def get_gen_table_column_list_by_table_id_service(
        cls, auth: AuthSchema, table_id: int
    ) -> list[dict[str, Any]]:
        """获取业务表字段列表信息（输出模型）。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_id (int): 业务表ID。

        返回:
        - list[dict[str, Any]]: 业务表字段列表，每个元素为字段详细信息字典。
        """
        gen_table_column_list_result = await GenTableColumnCRUD(auth).list_gen_table_column_crud({
            "table_id": table_id
        })
        result = [
            GenTableColumnOutSchema.model_validate(gen_table_column).model_dump()
            for gen_table_column in gen_table_column_list_result
        ]
        return result
