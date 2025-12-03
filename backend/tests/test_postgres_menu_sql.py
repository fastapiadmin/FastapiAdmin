# -*- coding: utf-8 -*-
"""
测试PostgreSQL菜单SQL生成
"""
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.v1.module_generator.gencode.tools.jinja2_template_util import Jinja2TemplateUtil
from app.api.v1.module_generator.gencode.schema import GenTableOutSchema

def test_postgres_menu_sql_generation():
    """
    测试PostgreSQL菜单SQL生成
    """
    # 模拟GenTableOutSchema对象
    gen_table = GenTableOutSchema(
        id=1,
        table_name="test_table",
        table_comment="测试表",
        business_name="test_table",
        function_name="测试表",
        module_name="test_module",
        parent_menu_id=7,  # 使用当前默认的目录ID
        status="0",
        created_time=None,
        updated_time=None,
        columns=[],
        pk_column=None,
        sub_table=None,
        sub=False
    )
    
    # 准备上下文
    context = Jinja2TemplateUtil.prepare_context(gen_table)
    # 手动设置数据库类型为PostgreSQL
    context['db_type'] = 'postgres'
    
    # 获取模板
    template = Jinja2TemplateUtil.get_template('sql/sql.sql.j2')
    
    # 渲染模板
    postgres_sql = template.render(context)
    
    # 打印生成的SQL
    print("=== PostgreSQL菜单SQL ===")
    print(postgres_sql)
    print("\n" + "="*50 + "\n")
    
    # 验证SQL语法
    assert "RETURNING id INTO parent_id;" in postgres_sql, "PostgreSQL SQL中缺少RETURNING子句"
    assert "INSERT INTO" in postgres_sql, "PostgreSQL SQL中缺少INSERT语句"
    assert "gen_random_uuid()" in postgres_sql, "PostgreSQL SQL中缺少gen_random_uuid()函数"
    assert str(gen_table.parent_menu_id) in postgres_sql, f"PostgreSQL SQL中未找到正确的parent_menu_id: {gen_table.parent_menu_id}"
    
    print("PostgreSQL菜单SQL生成测试通过！")
    print(f"父菜单ID: {gen_table.parent_menu_id}")
    print(f"功能名称: {gen_table.function_name}")
    print(f"模块名称: {gen_table.module_name}")
    print(f"业务名称: {gen_table.business_name}")

if __name__ == "__main__":
    test_postgres_menu_sql_generation()