"""代码生成 Jinja 工具纯函数。"""

from __future__ import annotations

from app.modules.generator.gencode.jinja2_template_util import Jinja2TemplateUtil as J


def test_normalize_column_type() -> None:
    assert J.normalize_db_column_type_for_mapping("VARCHAR(20)") == "VARCHAR(20)"
    assert J.normalize_db_column_type_for_mapping("  int  ") == "int"
    assert J.normalize_db_column_type_for_mapping(None) == ""


def test_business_name_slug_and_path() -> None:
    assert J.business_name_to_slug("用户 信息") == "_____"
    assert J.business_name_to_path("用户 信息") == "entity"
    assert J.business_name_to_slug("UserInfo") == "UserInfo"
    assert J.business_name_to_path("UserInfo") == "userinfo"


def test_package_and_permission_prefix() -> None:
    assert J.get_package_prefix("module_system") == "module_system"
    assert J.get_package_prefix("module_business") == "module_business"
    assert J.get_permission_prefix("system", "user") == "system:user"
    assert J.get_permission_prefix(None, "user") == ":user"


def test_merge_same_imports() -> None:
    out = J.merge_same_imports(["from a import X", "from a import Y", "import os"], "from")
    assert "import os" in out
    assert any("X" in x and "Y" in x for x in out)


def test_db_type_and_dicts() -> None:
    assert J.get_db_type("int4") == "int4"
    assert J.get_db_type("timestamp") == "timestamp"
    from app.modules.generator.gencode.schema import GenTableOutSchema
    assert J.get_dicts(GenTableOutSchema(table_name="t", columns=[])) == ""


def test_schema_model_imports_and_context() -> None:
    from app.modules.generator.gencode.schema import GenTableOutSchema, GenTableColumnSchema
    table = GenTableOutSchema(table_name="demo", class_name="Demo", package_name="module_demo", module_name="demo", business_name="demo", function_name="Demo", columns=[GenTableColumnSchema(column_name="id", column_type="int", is_pk=True, html_type="input")])
    schemas = J.get_schema_import_list(table)
    models = J.get_model_import_list(table)
    assert isinstance(schemas, set) and isinstance(models, list)


def test_schema_import_branches() -> None:
    from app.modules.generator.gencode.schema import GenTableOutSchema, GenTableColumnSchema
    cols = [
        GenTableColumnSchema(column_name="id", column_type="int", is_pk=True, html_type="input"),
        GenTableColumnSchema(column_name="status", column_type="varchar(10)", html_type="select", dict_type="sys_status"),
        GenTableColumnSchema(column_name="avatar", column_type="varchar(255)", html_type="imageUpload"),
        GenTableColumnSchema(column_name="extra", column_type="json", python_type="dict"),
    ]
    table = GenTableOutSchema(table_name="demo", class_name="Demo", package_name="module_demo", module_name="demo", business_name="demo", function_name="Demo", columns=cols)
    assert isinstance(J.get_schema_import_list(table), set)
    assert isinstance(J.get_model_import_list(table), list)
    assert isinstance(J.get_model_import_list(table, is_sub_entity=True), list)
