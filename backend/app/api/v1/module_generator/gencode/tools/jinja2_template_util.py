# -*- coding: utf-8 -*-

from datetime import datetime
from jinja2.environment import Environment
from jinja2 import Environment, FileSystemLoader, Template
from typing import Any

from app.common.constant import GenConstant
from app.config.path_conf import TEMPLATE_DIR
from app.config.setting import settings
from app.utils.common_util import CamelCaseUtil, SnakeCaseUtil
from app.utils.string_util import StringUtil

from app.api.v1.module_generator.gencode.schema import GenTableOutSchema, GenTableColumnOutSchema


class Jinja2TemplateUtil:
    """
    模板处理工具类
    """

    # 项目路径
    FRONTEND_PROJECT_PATH = 'frontend'
    BACKEND_PROJECT_PATH = 'backend'
    # 默认上级菜单，系统工具
    DEFAULT_PARENT_MENU_ID = 7
    
    # 环境对象
    _env = None
    
    @classmethod
    def get_env(cls):
        """
        获取模板环境对象。
        
        参数:
        - 无
        
        返回:
        - Environment: Jinja2 环境对象。
        """
        try:
            if cls._env is None:
                cls._env = Environment(
                    loader=FileSystemLoader(TEMPLATE_DIR),
                    autoescape=False, # 自动转义HTML
                    trim_blocks=True,   # 删除多余的空行
                    lstrip_blocks=True,  # 删除行首空格
                    keep_trailing_newline=True,  # 保留行尾换行符
                    enable_async=True,  # 开启异步支持  
                )
                cls._env.filters.update(
                    {
                        'camel_to_snake': SnakeCaseUtil.camel_to_snake,
                        'snake_to_camel': CamelCaseUtil.snake_to_camel,
                        'get_sqlalchemy_type': cls.get_sqlalchemy_type
                    }
                )
            return cls._env
        except Exception as e:
            raise RuntimeError(f'初始化Jinja2模板引擎失败: {e}')
    
    @classmethod
    def get_template(cls, template_path: str) -> Template:
        """
        获取模板。
        
        参数:
        - template_path (str): 模板路径。
        
        返回:
        - Template: Jinja2 模板对象。
        
        异常:
        - TemplateNotFound: 模板未找到时抛出。
        """
        return cls.get_env().get_template(template_path)
    
    @classmethod
    def prepare_context(cls, gen_table: GenTableOutSchema)  -> dict[str, Any]:
        """
        准备模板变量。
        
        参数:
        - gen_table (GenTableOutSchema): 生成表的配置信息。
        
        返回:
        - Dict[str, Any]: 模板上下文字典。
        """
        # 处理options为None的情况
        # if not gen_table.options:
        #     raise ValueError('请先完善生成配置信息')
        class_name = gen_table.class_name or ''
        module_name = gen_table.module_name or ''
        business_name = gen_table.business_name or ''
        package_name = gen_table.package_name or ''
        function_name = gen_table.function_name or ''
        
        context = {
            'table_name': gen_table.table_name or '',
            'table_comment': gen_table.table_comment or '',
            'function_name': function_name if StringUtil.is_not_empty(function_name) else '【请填写功能名称】',
            'class_name': class_name,
            'module_name': module_name,
            'business_name': business_name,
            'base_package': cls.get_package_prefix(package_name),
            'package_name': package_name,
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'pk_column': gen_table.pk_column,
            'model_import_list': cls.get_model_import_list(gen_table),
            'schema_import_list': cls.get_schema_import_list(gen_table),
            'permission_prefix': cls.get_permission_prefix(module_name, business_name),
            'columns': gen_table.columns or [],
            'table': gen_table,
            'dicts': cls.get_dicts(gen_table),
            'db_type': settings.DATABASE_TYPE,
            'column_not_add_show': GenConstant.COLUMNNAME_NOT_ADD_SHOW,
            'column_not_edit_show': GenConstant.COLUMNNAME_NOT_EDIT_SHOW,
            'parent_menu_id': int(gen_table.parent_menu_id) if gen_table.parent_menu_id is not None else int(cls.DEFAULT_PARENT_MENU_ID),
        }

        return context
    
    @classmethod
    def get_template_list(cls):
        """
        获取模板列表。
        
        参数:
        - 无
        返回:
        - List[str]: 模板路径列表。
        """
        templates = [
            'python/controller.py.j2',
            'python/service.py.j2',
            'python/crud.py.j2',
            'python/schema.py.j2',
            'python/model.py.j2',
            'python/__init__.py.j2',
            'sql/sql.sql.j2',
            'ts/api.ts.j2',
            'vue/index.vue.j2',
        ]
        return templates
    

    @classmethod
    def get_file_name(cls, template: str, gen_table: GenTableOutSchema):
        """
        根据模板生成文件名。

        参数:
        - template (str): 模板路径字符串。
        - gen_table (GenTableOutSchema): 生成表的配置信息。

        返回:
        - str: 模板生成的文件名。
        
        异常:
        - ValueError: 当无法生成有效文件名时抛出。
        """
        module_name = gen_table.module_name or ''
        business_name = gen_table.business_name or ''
        
        # 验证必要的参数
        if not module_name or not business_name:
            raise ValueError(f"无法为模板 {template} 生成文件名：模块名或业务名未设置")

        # 映射表方式简化
        template_mapping = {
            'controller.py.j2': f'{cls.BACKEND_PROJECT_PATH}/app/api/v1/{module_name}/{business_name}/controller.py',
            'service.py.j2': f'{cls.BACKEND_PROJECT_PATH}/app/api/v1/{module_name}/{business_name}/service.py',
            'crud.py.j2': f'{cls.BACKEND_PROJECT_PATH}/app/api/v1/{module_name}/{business_name}/crud.py',
            'schema.py.j2': f'{cls.BACKEND_PROJECT_PATH}/app/api/v1/{module_name}/{business_name}/schema.py',
            'model.py.j2': f'{cls.BACKEND_PROJECT_PATH}/app/api/v1/{module_name}/{business_name}/model.py',
            '__init__.py.j2': f'{cls.BACKEND_PROJECT_PATH}/app/api/v1/{module_name}/{business_name}/__init__.py',
            'sql.sql.j2': f'{cls.BACKEND_PROJECT_PATH}/sql/menu/{module_name}/{business_name}.sql',
            'api.ts.j2': f'{cls.FRONTEND_PROJECT_PATH}/src/api/{module_name}/{business_name}.ts',
            'index.vue.j2': f'{cls.FRONTEND_PROJECT_PATH}/src/views/{module_name}/{business_name}/index.vue'
        }
        
        # 查找匹配的模板路径
        for key, path in template_mapping.items():
            if key in template:
                return path
        
        # 默认处理
        template_name = template.split('/')[-1].replace('.j2', '')
        return f'{cls.BACKEND_PROJECT_PATH}/generated/{template_name}'

    @classmethod
    def get_package_prefix(cls, package_name: str) -> str:
        """
        获取包前缀。

        参数:
        - package_name (str): 包名。
        
        返回:
        - str: 包前缀。
        """
        # 修复：当包名中不存在'.'时，直接返回原包名
        return package_name[: package_name.rfind('.')] if '.' in package_name else package_name

    @classmethod
    def get_schema_import_list(cls, gen_table: GenTableOutSchema):
        """
        获取schema模板导入包列表

        :param gen_table: 生成表的配置信息
        :return: 导入包列表
        """
        columns = gen_table.columns or []
        import_list = set()
        for column in columns:
            if column.python_type in GenConstant.TYPE_DATE:
                import_list.add(f'from datetime import {column.python_type}')
            elif column.python_type == GenConstant.TYPE_DECIMAL:
                import_list.add('from decimal import Decimal')
        if gen_table.sub:
            if gen_table.sub_table and gen_table.sub_table.columns:
                sub_columns = gen_table.sub_table.columns or []
                for sub_column in sub_columns:
                    if sub_column.python_type in GenConstant.TYPE_DATE:
                        import_list.add(f'from datetime import {sub_column.python_type}')
                    elif sub_column.python_type == GenConstant.TYPE_DECIMAL:
                        import_list.add('from decimal import Decimal')
        return cls.merge_same_imports(list(import_list), 'from datetime import')

    @classmethod
    def get_model_import_list(cls, gen_table: GenTableOutSchema):
        """
        获取do模板导入包列表

        :param gen_table: 生成表的配置信息
        :return: 导入包列表
        """
        columns = gen_table.columns or []
        import_list = set()
        
        for column in columns:
            if column.column_type:
                data_type = cls.get_db_type(column.column_type)
                if data_type in GenConstant.COLUMNTYPE_GEOMETRY:
                    import_list.add('from geoalchemy2 import Geometry')
                import_list.add(
                    f'from sqlalchemy import {StringUtil.get_mapping_value_by_key_ignore_case(GenConstant.DB_TO_SQLALCHEMY, data_type)}'
                )
        if gen_table.sub:
            import_list.add('from sqlalchemy import ForeignKey')
            if gen_table.sub_table and gen_table.sub_table.columns:
                sub_columns = gen_table.sub_table.columns or []
                for sub_column in sub_columns:
                    if sub_column.column_type:
                        data_type = cls.get_db_type(sub_column.column_type)
                        import_list.add(
                            f'from sqlalchemy import {StringUtil.get_mapping_value_by_key_ignore_case(GenConstant.DB_TO_SQLALCHEMY, data_type)}'
                        )
        return cls.merge_same_imports(list(import_list), 'from sqlalchemy import')

    @classmethod
    def get_db_type(cls, column_type: str) -> str:
        """
        获取数据库字段类型。

        参数:
        - column_type (str): 字段类型字符串。
        
        返回:
        - str: 数据库类型（去除长度等修饰）。
        """
        if '(' in column_type:
            return column_type.split('(')[0]
        return column_type
    
    @classmethod
    def merge_same_imports(cls, imports: list[str], import_start: str) -> list[str]:
        """
        合并相同的导入语句。

        参数:
        - imports (list[str]): 导入语句列表。
        - import_start (str): 导入语句的起始字符串。
        
        返回:
        - list[str]: 合并后的导入语句列表。
        """
        merged_imports = []
        _imports = []
        for import_stmt in imports:
            if import_stmt.startswith(import_start):
                imported_items = import_stmt.split('import')[1].strip()
                _imports.extend(imported_items.split(', '))
            else:
                merged_imports.append(import_stmt)

        if _imports:
            merged_datetime_import = f'{import_start} {", ".join(_imports)}'
            merged_imports.append(merged_datetime_import)

        return merged_imports
    
    @classmethod
    def get_dicts(cls, gen_table: GenTableOutSchema):
        """
        获取字典列表。

        参数:
        - gen_table (GenTableOutSchema): 生成表的配置信息。
        
        返回:
        - str: 以逗号分隔的字典类型字符串。
        """
        columns = gen_table.columns or []
        dicts = set()
        cls.add_dicts(dicts, columns)
        # 处理sub_table为None的情况
        if gen_table.sub_table is not None:
            # 处理sub_table.columns为None的情况
            sub_columns = gen_table.sub_table.columns or []
            cls.add_dicts(dicts, sub_columns)
        return ', '.join(dicts)

    @classmethod
    def add_dicts(cls, dicts: set[str], columns: list[GenTableColumnOutSchema]):
        """
        添加字典类型到集合。

        参数:
        - dicts (set[str]): 字典类型集合。
        - columns (list[GenTableColumnOutSchema]): 字段列表。
        
        返回:
        - set[str]: 更新后的字典类型集合。
        """
        for column in columns:
            super_column = column.super_column if column.super_column is not None else '0'
            dict_type = column.dict_type or ''
            html_type = column.html_type or ''
            
            if (
                not super_column
                and StringUtil.is_not_empty(dict_type)
                and StringUtil.equals_any_ignore_case(
                    html_type, [GenConstant.HTML_SELECT, GenConstant.HTML_RADIO, GenConstant.HTML_CHECKBOX]
                )
            ):
                dicts.add(f"'{dict_type}'")

    @classmethod
    def get_permission_prefix(cls, module_name: str | None, business_name: str | None) -> str:
        """
        获取权限前缀。

        参数:
        - module_name (str | None): 模块名。
        - business_name (str | None): 业务名。
        
        返回:
        - str: 权限前缀字符串。
        """
        return f'{module_name}:{business_name}'
    
    @classmethod
    def get_sqlalchemy_type(cls, column):
        """
        获取 SQLAlchemy 类型。

        参数:
        - column_type (Any): 列类型或包含 `column_type` 属性的对象。
        
        返回:
        - str: SQLAlchemy 类型字符串。
        """
        if '(' in column:
            column_type_list = column.split('(')
            if column_type_list[0] in GenConstant.COLUMNTYPE_STR:
                sqlalchemy_type = (
                    StringUtil.get_mapping_value_by_key_ignore_case(
                        GenConstant.DB_TO_SQLALCHEMY, column_type_list[0]
                    )
                    + '('
                    + column_type_list[1]
                )
            else:
                sqlalchemy_type = StringUtil.get_mapping_value_by_key_ignore_case(
                    GenConstant.DB_TO_SQLALCHEMY, column_type_list[0]
                )
        else:
            sqlalchemy_type = StringUtil.get_mapping_value_by_key_ignore_case(
                GenConstant.DB_TO_SQLALCHEMY, column
            )

        return sqlalchemy_type