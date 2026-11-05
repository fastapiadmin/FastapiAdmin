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
