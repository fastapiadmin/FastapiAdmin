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
