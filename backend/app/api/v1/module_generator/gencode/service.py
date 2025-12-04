# -*- coding: utf-8 -*-

import io
import os
import zipfile
from typing import Any
from sqlglot.expressions import Add, Alter, Create, Delete, Drop, Expression, Insert, Table, TruncateTable, Update
from sqlglot import parse as sqlglot_parse

from app.config.path_conf import BASE_DIR
from app.config.setting import settings
from app.core.logger import log
from app.core.exceptions import CustomException
from app.core.base_params import PaginationQueryParam

from app.api.v1.module_system.auth.schema import AuthSchema
from .tools.jinja2_template_util import Jinja2TemplateUtil
from .tools.gen_util import GenUtils
from .schema import GenTableSchema, GenTableOutSchema, GenTableColumnSchema,  GenTableColumnOutSchema, GenTableQueryParam
from .crud import GenTableColumnCRUD, GenTableCRUD


def handle_service_exception(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f'{func.__name__}执行失败: {str(e)}')
    return wrapper


class GenTableService:
    """代码生成业务表服务层"""

    @classmethod
    @handle_service_exception
    async def get_gen_table_detail_service(cls, auth: AuthSchema, table_id: int) -> dict:
        """获取业务表详细信息（含字段与其他表列表）。
        - 备注：优先解析`options`为`GenTableOptionSchema`，设置`parent_menu_id`等选项；保证`columns`与`tables`结构完整。
        """
        gen_table = await cls.get_gen_table_by_id_service(auth, table_id)
        return GenTableOutSchema.model_validate(gen_table).model_dump()

    @classmethod
    @handle_service_exception
    async def get_gen_table_list_service(cls, auth: AuthSchema, search: GenTableQueryParam) -> list[dict]:
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
    async def get_gen_table_page_service(cls, auth: AuthSchema, page: PaginationQueryParam, search: GenTableQueryParam) -> dict:
        """获取代码生成业务表分页列表信息。
        - 备注：结合分页参数与查询参数，返回包含分页信息的字典结果。
        """
        search_dict = search.__dict__ if search else None
        return await GenTableCRUD(auth).gen_table_page_crud(search=search_dict, page=page)
        

    @classmethod
    @handle_service_exception
    async def get_gen_db_table_list_service(cls, auth: AuthSchema, search: GenTableQueryParam) -> list[Any]:
        """获取数据库表列表（跨方言）。
        - 备注：返回已转换为字典的结构，适用于前端直接展示；排序参数保留扩展位但当前未使用。
        """
        gen_db_table_list_result = await GenTableCRUD(auth=auth).get_db_table_list(search)
        return gen_db_table_list_result

    @classmethod
    @handle_service_exception
    async def get_gen_db_table_page_service(cls, auth: AuthSchema, page: PaginationQueryParam, search: GenTableQueryParam) -> dict:
        """获取数据库表分页列表（跨方言）。
        - 备注：结合分页参数与查询参数，返回包含分页信息的字典结果。
        """
        return await GenTableCRUD(auth).db_table_page_crud(search=search, page=page)
        

    @classmethod
    @handle_service_exception
    async def get_gen_db_table_list_by_name_service(cls, auth: AuthSchema, table_names: list[str]) -> list[GenTableOutSchema]:
        """根据表名称组获取数据库表信息。
        - 校验：如有不存在的表名，抛出明确异常；返回统一的`GenTableOutSchema`列表。
        """
        # 验证输入参数
        if not table_names:
            raise CustomException(msg="表名列表不能为空")
            
        gen_db_table_list_result = await GenTableCRUD(auth).get_db_table_list_by_names(table_names)

        # 修复：将GenDBTableSchema对象转换为字典后再传递给GenTableOutSchema
        result = []
        for gen_table in gen_db_table_list_result:
            # 确保table_name不为None
            if gen_table.table_name is not None:
                result.append(GenTableOutSchema(**gen_table.model_dump()))
        
        return result

    @classmethod
    @handle_service_exception
    async def import_gen_table_service(cls, auth: AuthSchema, gen_table_list: list[GenTableOutSchema])  -> bool | None:
        """导入表结构到生成器（持久化并初始化列）。
        - 备注：避免重复导入；为每列调用`GenUtils.init_column_field`填充默认属性，保留语义一致性。
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
                add_gen_table = await GenTableCRUD(auth).add_gen_table(GenTableSchema.model_validate(table.model_dump()))
                gen_table_columns = await GenTableColumnCRUD(auth).get_gen_db_table_columns_by_name(table_name)
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
            raise CustomException(msg=f'导入失败, {str(e)}')

    @classmethod
    @handle_service_exception
    async def create_table_service(cls, auth: AuthSchema, sql: str) -> bool | None:
        """创建表结构并导入至代码生成模块。
        - 校验：使用`sqlglot`确保仅包含`CREATE TABLE`语句；失败抛出明确异常。
        - 唯一性检查：在创建前检查该表是否已存在于数据库中。
        """
        # 验证SQL非空
        if not sql or not sql.strip():
            raise CustomException(msg='SQL语句不能为空')
            
        try:
            # 解析SQL语句
            sql_statements = sqlglot_parse(sql, dialect=settings.DATABASE_TYPE)
            if not sql_statements:
                raise CustomException(msg='无法解析SQL语句，请检查SQL语法')
            
            # 校验sql语句是否为合法的建表语句
            if not cls.__is_valid_create_table(sql_statements):
                raise CustomException(msg='sql语句不是合法的建表语句')
            
            # 获取要创建的表名
            table_names = cls.__get_table_names(sql_statements)            
            # 创建CRUD实例
            gen_table_crud = GenTableCRUD(auth=auth)
            
            # 检查每个表是否已存在
            for table_name in table_names:
                # 检查数据库中是否已存在该表
                if await gen_table_crud.check_table_exists(table_name):
                    raise CustomException(msg=f'表 {table_name} 已存在，请检查并修改表名后重试')
                
                # 检查代码生成模块中是否已导入该表
                existing_table = await gen_table_crud.get_gen_table_by_name(table_name)
                if existing_table:
                    raise CustomException(msg=f'表 {table_name} 已在代码生成模块中存在，请检查并修改表名后重试')
            
            # 表不存在，执行SQL语句创建表
            result = await gen_table_crud.create_table_by_sql(sql_statements)
            if not result:
                raise CustomException(msg=f'创建表 {table_names} 失败，请检查SQL语句')
            
            # 导入表结构到代码生成模块 - 简化逻辑，移除多余的None检查
            gen_table_list = await cls.get_gen_db_table_list_by_name_service(auth, table_names)
            
            import_result = await cls.import_gen_table_service(auth, gen_table_list)

            return import_result
            
        except Exception as e:
            raise CustomException(msg=f'创建表结构失败: {str(e)}')
    
    @classmethod
    def __is_valid_create_table(cls, sql_statements: list[Expression | None]) -> bool:
        """
        校验SQL语句是否为合法的建表语句。
    
        参数:
        - sql_statements (list[Expression | None]): SQL的AST列表。
    
        返回:
        - bool: 校验结果。
        """
        validate_create = [isinstance(sql_statement, Create) for sql_statement in sql_statements]
        validate_forbidden_keywords = [
            isinstance(
                sql_statement,
                (Add, Alter, Delete, Drop, Insert, TruncateTable, Update),
            )
            for sql_statement in sql_statements
        ]
        if not any(validate_create) or any(validate_forbidden_keywords):
            return False
        return True
    
    @classmethod
    def __get_table_names(cls, sql_statements: list[Expression | None]) -> list[str]:
        """
        获取SQL语句中所有的建表表名。
    
        参数:
        - sql_statements (list[Expression | None]): SQL的AST列表。
    
        返回:
        - list[str]: 建表表名列表。
        """
        table_names = []
        for sql_statement in sql_statements:
            if isinstance(sql_statement, Create):
                table = sql_statement.find(Table)
                if table and table.name:
                    table_names.append(table.name)
        return list(set(table_names))

    @classmethod
    @handle_service_exception
    async def update_gen_table_service(cls, auth: AuthSchema, data: GenTableSchema, table_id: int) -> dict[str, Any]:
        """编辑业务表信息（含选项与字段）。
        - 备注：将`params`序列化写入`options`以持久化；仅更新存在`id`的列，避免误创建。
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
                        if hasattr(gen_table_column, 'id') and gen_table_column.id:
                            column_schema = GenTableColumnSchema(**gen_table_column.model_dump())
                            await GenTableColumnCRUD(auth).update_gen_table_column_crud(gen_table_column.id, column_schema)
                return GenTableOutSchema.model_validate(result).model_dump()
            except Exception as e:
                raise CustomException(msg=str(e))
        else:
            raise CustomException(msg='业务表不存在')

    @classmethod
    @handle_service_exception
    async def delete_gen_table_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除业务表信息（先删字段，再删表）。"""
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
    async def get_gen_table_by_id_service(cls, auth: AuthSchema, table_id: int) -> GenTableOutSchema:
        """获取需要生成代码的业务表详细信息。
        - 备注：去除SQLAlchemy内部状态；将`None`值转为适配前端的默认值；解析`options`补充选项。
        """
        gen_table = await GenTableCRUD(auth=auth).get_gen_table_by_id(table_id)
        if not gen_table:
            raise CustomException(msg='业务表不存在')
        
        result = GenTableOutSchema.model_validate(gen_table)
        return result

    @classmethod
    @handle_service_exception
    async def get_gen_table_all_service(cls, auth: AuthSchema) -> list[GenTableOutSchema]:
        """获取所有业务表信息（列表）。"""
        gen_table_all = await GenTableCRUD(auth=auth).get_gen_table_all() or []
        result = []
        for gen_table in gen_table_all:
            try:
                table_out = GenTableOutSchema.model_validate(gen_table)
                result.append(table_out)
            except Exception as e:
                log.error(f"转换业务表时出错: {str(e)}")
                continue
        return result

    @classmethod
    @handle_service_exception
    async def preview_code_service(cls, auth: AuthSchema, table_id: int) -> dict[str, Any]:
        """
        预览代码（根据模板渲染内存结果）。
        - 备注：构建Jinja2上下文；根据模板类型与前端类型选择模板清单；返回文件名到内容映射。
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
                log.error(f"渲染模板 {template} 时出错: {str(e)}")
                # 即使某个模板渲染失败，也继续处理其他模板
                preview_code_result[template] = f"渲染错误: {str(e)}"
        return preview_code_result

    @classmethod
    @handle_service_exception
    async def generate_code_service(cls, auth: AuthSchema, table_name: str) -> bool:
        """生成代码至指定路径（安全写入+可跳过覆盖）。
        - 安全：限制写入在项目根目录内；越界路径自动回退到项目根目录。
        """
        # 验证表名非空
        if not table_name or not table_name.strip():
            raise CustomException(msg='表名不能为空')
            
        env = Jinja2TemplateUtil.get_env()
        render_info = await cls.__get_gen_render_info(auth, table_name)
        gen_table_schema = render_info[3]
        for template in render_info[0]:
            try:
                render_content = await env.get_template(template).render_async(**render_info[2])
                gen_path = cls.__get_gen_path(gen_table_schema, template)
                if not gen_path:
                    raise CustomException(msg='【代码生成】生成路径为空')

                # 确保目录存在
                os.makedirs(os.path.dirname(gen_path), exist_ok=True)

                with open(gen_path, 'w', encoding='utf-8') as f:
                    f.write(render_content)
            except Exception as e:
                raise CustomException(msg=f'渲染模板失败，表名：{gen_table_schema.table_name}，详细错误信息：{str(e)}')
        return True

    @classmethod
    @handle_service_exception
    async def batch_gen_code_service(cls, auth: AuthSchema, table_names: list[str]) -> bytes:
        """
        批量生成代码并打包为ZIP。
        - 备注：内存生成并压缩，兼容多模板类型；供下载使用。
        """
        # 验证表名列表非空
        if not table_names:
            raise CustomException(msg="表名列表不能为空")
            
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for table_name in table_names:
                if not table_name.strip():
                    continue
                    
                try:
                    env = Jinja2TemplateUtil.get_env()
                    render_info = await cls.__get_gen_render_info(auth, table_name)
                    for template_file, output_file in zip(render_info[0], render_info[1]):
                        render_content = await env.get_template(template_file).render_async(**render_info[2])
                        zip_file.writestr(output_file, render_content)
                except Exception as e:
                    log.error(f"批量生成代码时处理表 {table_name} 出错: {str(e)}")
                    # 继续处理其他表，不中断整个过程
                    continue

        zip_data = zip_buffer.getvalue()
        zip_buffer.close()
        return zip_data

    @classmethod
    @handle_service_exception
    async def sync_db_service(cls, auth: AuthSchema, table_name: str) -> None:
        """同步数据库表结构至生成器（保留用户配置）。
        - 备注：按数据库实际字段重建或更新生成器字段；保留字典/查询/展示等用户自定义属性；清理已删除字段。
        """
        # 验证表名非空
        if not table_name or not table_name.strip():
            raise CustomException(msg='表名不能为空')
            
        gen_table = await GenTableCRUD(auth).get_gen_table_by_name(table_name)
        if not gen_table:
            raise CustomException(msg='业务表不存在')
        table = GenTableOutSchema.model_validate(gen_table)
        if not table.id:
            raise CustomException(msg='业务表ID不能为空')
        table_columns = table.columns or []
        table_column_map = {column.column_name: column for column in table_columns}
        # 确保db_table_columns始终是列表类型，避免None值
        db_table_columns = await GenTableColumnCRUD(auth).get_gen_db_table_columns_by_name(table_name) or []
        db_table_columns = [col for col in db_table_columns if col is not None]
        db_table_column_names = [column.column_name for column in db_table_columns]
        try:
            for column in db_table_columns:
                # 仅在缺省时初始化默认属性（包含 table_id 关联）
                GenUtils.init_column_field(column, table)
                # 利用schema层的默认值，移除多余的None检查
                if column.column_name in table_column_map:
                    prev_column = table_column_map[column.column_name]
                    # 复用旧记录ID，确保执行更新
                    if hasattr(prev_column, 'id') and prev_column.id:
                        column.id = prev_column.id

                    # 保留用户配置的显示与查询属性 - 使用getattr确保安全访问
                    if hasattr(prev_column, 'dict_type') and prev_column.dict_type:
                        column.dict_type = prev_column.dict_type
                    if hasattr(prev_column, 'query_type') and prev_column.query_type:
                        column.query_type = prev_column.query_type
                    if hasattr(prev_column, 'html_type') and prev_column.html_type:
                        column.html_type = prev_column.html_type

                    # 保留关键用户自定义属性 - 安全处理is_pk
                    is_pk_bool = False
                    if hasattr(prev_column, 'is_pk'):
                        # 处理不同类型的is_pk值
                        if isinstance(prev_column.is_pk, bool):
                            is_pk_bool = prev_column.is_pk
                        else:
                            is_pk_bool = str(prev_column.is_pk) == '1'
                    
                    # 安全处理nullable属性
                    if hasattr(prev_column, 'is_nullable') and not is_pk_bool:
                        column.is_nullable = prev_column.is_nullable
                    
                    # 保留其他重要用户设置
                    if hasattr(prev_column, 'python_field'):
                        column.python_field = prev_column.python_field or column.python_field

                    if hasattr(column, 'id') and column.id:
                        await GenTableColumnCRUD(auth).update_gen_table_column_crud(column.id, column)
                    else:
                        await GenTableColumnCRUD(auth).create_gen_table_column_crud(column)
                else:
                    # 设置table_id以确保新字段能正确关联到表
                    column.table_id = table.id
                    await GenTableColumnCRUD(auth).create_gen_table_column_crud(column)
            del_columns = [column for column in table_columns if column.column_name not in db_table_column_names]
            if del_columns:
                for column in del_columns:
                    if hasattr(column, 'id') and column.id:
                        await GenTableColumnCRUD(auth).delete_gen_table_column_by_column_id_crud([column.id])
        except Exception as e:
            raise CustomException(msg=f'同步失败: {str(e)}')

    @classmethod
    async def set_pk_column(cls, gen_table: GenTableOutSchema) -> None:
        """设置主键列信息（主表/子表）。
        - 备注：同时兼容`pk`布尔与`is_pk == '1'`字符串两种标识。
        """
        if gen_table.columns:
            for column in gen_table.columns:
                # 修复：确保正确检查主键标识
                if getattr(column, 'pk', False) or getattr(column, 'is_pk', '') == '1':
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
        output_files = [Jinja2TemplateUtil.get_file_name(template, gen_table) for template in template_list]

        return [template_list, output_files, context, gen_table]

    @classmethod
    def __get_gen_path(cls, gen_table: GenTableOutSchema, template: str) -> str | None:
        """根据GenTableOutSchema对象和模板名称生成路径。"""
        try:
            file_name = Jinja2TemplateUtil.get_file_name(template, gen_table)
            # 默认写入到项目根目录（backend的上一级）
            project_root = str(BASE_DIR.parent)
            full_path = os.path.join(project_root, file_name)
            
            # 确保路径在项目根目录内，防止路径遍历攻击
            if not os.path.abspath(full_path).startswith(os.path.abspath(project_root)):
                log.error(f"路径越界，回退到项目根目录: {file_name}")
                # 回退到项目根目录下的generated文件夹
                full_path = os.path.join(project_root, "generated", os.path.basename(file_name))
            
            return full_path
        except Exception as e:
            log.error(f"生成路径时出错: {str(e)}")
            return None


class GenTableColumnService:
    """代码生成业务表字段服务层"""

    @classmethod
    @handle_service_exception
    async def get_gen_table_column_list_by_table_id_service(cls, auth: AuthSchema, table_id: int) -> list[dict[str, Any]]:
        """获取业务表字段列表信息（输出模型）。"""
        gen_table_column_list_result = await GenTableColumnCRUD(auth).list_gen_table_column_crud({"table_id": table_id})
        result = [GenTableColumnOutSchema.model_validate(gen_table_column).model_dump() for gen_table_column in gen_table_column_list_result]
        return result