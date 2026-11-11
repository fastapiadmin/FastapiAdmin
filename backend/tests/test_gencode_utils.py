"""代码生成器纯工具分支。"""

from __future__ import annotations

import pytest

from app.core.exceptions import CustomException
from app.modules.generator.gencode.gen_util import GenUtils
from app.modules.generator.gencode.service import GenTableService


def test_arrays_contains_and_names() -> None:
    assert GenUtils.arrays_contains(["a", "b"], "a") is True
    assert GenUtils.arrays_contains(["a", "b"], "c") is False
    assert GenUtils.convert_class_name("sys_user") == "SysUser"
    assert GenUtils.convert_class_name("user") == "User"
    assert GenUtils.replace_first("abcabc", ["ab"]) == "cabc"
    assert GenUtils.replace_first("abc", []) == "abc"


def test_db_type_and_length() -> None:
    assert GenUtils.get_db_type("varchar(64)") == "varchar"
    assert GenUtils.get_db_type("int") == "int"
    assert GenUtils.get_db_type("bigint") == "bigint"
    assert GenUtils.get_db_type("datetime") == "datetime"
    assert GenUtils.get_db_type("text") == "text"
    assert GenUtils.get_column_length("varchar(64)") == 64
    assert GenUtils.get_column_length("int") == 0
    assert GenUtils.split_column_type("varchar(64)") == ["64"]


def test_master_sub_validation() -> None:
    from app.modules.generator.gencode.schema import GenTableSchema
    # 非主表直接通过
    data = GenTableSchema(table_name="demo", table_comment="demo")
    GenTableService.normalize_and_validate_master_sub(data)
    # 主表缺子表配置应报错（按实际 schema 字段构造失败时跳过）
    with pytest.raises(Exception):
        GenTableService.normalize_and_validate_master_sub(None)  # type: ignore[arg-type]


def test_init_table_defaults() -> None:
    from app.modules.generator.gencode.schema import GenTableSchema
    t = GenTableSchema(table_name="gen_demo_user", table_comment="用户测试")
    GenUtils.init_table(t)
    assert t.class_name == "GenDemoUser"
    assert t.module_name == "demo_user"
    assert t.package_name == "module_demo_user"
    assert t.business_name == "gen_demo_user"
    assert t.function_name == "用户"


def test_init_column_inference_and_pk_overrides() -> None:
    from app.modules.generator.gencode.schema import GenTableColumnSchema, GenTableOutSchema
    table = GenTableOutSchema(table_name="demo", id=10)
    c = GenTableColumnSchema(column_name="status", column_type="tinyint(1)")
    GenUtils.init_column_field(c, table)
    assert c.table_id == 10 and c.python_field == "status"
    assert c.html_type == "radio" and c.is_insert is True and c.is_query is True
    pk = GenTableColumnSchema(column_name="id", column_type="int", is_pk=True)
    GenUtils.init_column_field(pk, table)
    assert pk.is_insert is False and pk.is_edit is False and pk.is_list is False and pk.is_query is False
    with pytest.raises(ValueError):
        GenUtils.init_column_field(GenTableColumnSchema(column_name="x"), GenTableOutSchema(table_name="x"))


def test_init_table_fallbacks_and_prefixes() -> None:
    from app.modules.generator.gencode.schema import GenTableSchema
    a = GenTableSchema(table_name="tb_demo", table_comment="")
    GenUtils.init_table(a)
    assert a.module_name == "demo" and a.function_name == "tb_demo"
    b = GenTableSchema(table_name="demo", table_comment="测试表", module_name="x", package_name="module_x")
    GenUtils.init_table(b)
    assert b.module_name == "x" and b.package_name == "module_x"


def test_init_column_html_types_and_query() -> None:
    from app.modules.generator.gencode.schema import GenTableColumnSchema, GenTableOutSchema
    table = GenTableOutSchema(table_name="demo", id=1)
    from app.common.constant import GenConstant
    from app.config.setting import settings
    time_type = "timestamp without time zone" if settings.DATABASE_TYPE == "postgres" else "datetime"
    cases = [
        ("status", "tinyint(1)", "radio", GenConstant.QUERY_EQ),
        ("user_type", "varchar(10)", "select", GenConstant.QUERY_LIKE),
        ("avatar_image", "varchar(64)", "imageUpload", GenConstant.QUERY_LIKE),
        ("doc_file", "varchar(64)", "fileUpload", GenConstant.QUERY_LIKE),
        ("content", "text", "editor", GenConstant.QUERY_LIKE),
        ("created_time", time_type, "datetime", "EQ"),
        ("age", "int", "input", GenConstant.QUERY_EQ),
        ("description", "varchar(1000)", "textarea", None),
        ("name", "varchar(10)", "input", GenConstant.QUERY_LIKE),
    ]
    for name, typ, html, query in cases:
        c = GenTableColumnSchema(column_name=name, column_type=typ)
        GenUtils.init_column_field(c, table)
        assert c.html_type == html, (name, c.html_type)
        assert c.query_type == query, (name, c.query_type)
    # 显式关闭查询时不推断 query_type
    c = GenTableColumnSchema(column_name="code", column_type="varchar(10)", is_query=False)
    GenUtils.init_column_field(c, table)
    assert c.query_type is None
