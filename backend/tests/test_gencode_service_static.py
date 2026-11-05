"""代码生成器服务静态规则覆盖。"""

from __future__ import annotations

import pytest

from app.core.exceptions import CustomException
from app.modules.generator.gencode.schema import GenTableColumnSchema, GenTableOutSchema, GenTableSchema
from app.modules.generator.gencode.service import GenTableService


def test_route_and_catalog_keys() -> None:
    assert GenTableService._menu_route_first_segment(None, "system", None) == "module_system"
    assert GenTableService._menu_route_first_segment(None, "module_system", None) == "module_system"
    svc = GenTableService.__new__(GenTableService)
    assert svc._catalog_menu_dir_key(None, "module_system", "user") == "user"
    with pytest.raises(CustomException):
        svc._catalog_menu_dir_key(None, "", "user")
    with pytest.raises(CustomException):
        svc._catalog_menu_dir_key(None, "module_system", "")


def test_master_sub_rules() -> None:
    GenTableService.normalize_and_validate_master_sub(GenTableSchema(table_name="m"))
    with pytest.raises(CustomException, match="同时填写"):
        GenTableService.normalize_and_validate_master_sub(GenTableSchema(table_name="m", sub_table_name="s"))
    with pytest.raises(CustomException, match="不能与主表"):
        GenTableService.normalize_and_validate_master_sub(GenTableSchema(table_name="m", sub_table_name="m", sub_table_fk_name="m_id"))


def test_assert_master_sub_config() -> None:
    GenTableService._assert_master_sub_config_valid(GenTableOutSchema(table_name="m"))
    with pytest.raises(CustomException, match="同时填写"):
        GenTableService._assert_master_sub_config_valid(GenTableOutSchema(table_name="m", sub_table_name="s"))
    with pytest.raises(CustomException, match="无法生成"):
        GenTableService._assert_master_sub_config_valid(GenTableOutSchema(table_name="m", sub_table_name="s", sub_table_fk_name="m_id"))


async def test_set_pk_column() -> None:
    svc = GenTableService.__new__(GenTableService)
    t = GenTableOutSchema(table_name="m", columns=[GenTableColumnSchema(column_name="id"), GenTableColumnSchema(column_name="name")])
    await svc.set_pk_column(t)
    assert t.pk_column.column_name == "id"
    t2 = GenTableOutSchema(table_name="m", columns=[])
    await svc.set_pk_column(t2)
    assert t2.pk_column is None


async def test_preview_code_missing_and_render(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.generator.gencode import service as svc_mod
    from app.modules.generator.gencode.schema import GenTableOutSchema
    class CRUD:
        def __init__(self,*a): pass
        async def get_gen_table_by_id(self, id, preload=None): return None
    monkeypatch.setattr(svc_mod, "GenTableCRUD", CRUD)
    svc = GenTableService.__new__(GenTableService); svc.auth = object(); svc.db = object()
    with pytest.raises(CustomException, match="业务表不存在"):
        await svc.preview_code(1)

    table = GenTableOutSchema(table_name="demo", package_name="module_demo")
    class CRUD2:
        def __init__(self,*a): pass
        async def get_gen_table_by_id(self, id, preload=None): return table
    monkeypatch.setattr(svc_mod, "GenTableCRUD", CRUD2)
    async def set_pk(t): pass
    async def hydrate(t): pass
    async def pkg(*a): return "module_demo"
    svc.set_pk_column = set_pk; svc.hydrate_sub_table = hydrate; svc._effective_package_name = pkg
    class Tpl:
        async def render_async(self, **ctx): return "code"
    class Env:
        def get_template(self, name): return Tpl()
    class J:
        @staticmethod
        def get_env(): return Env()
        @staticmethod
        def prepare_context(t): return {}
        @staticmethod
        def get_template_list(): return ["a.py"]
        @staticmethod
        def get_file_name(t, g): return "a.py"
    monkeypatch.setattr(svc_mod, "Jinja2TemplateUtil", J)
    out = await svc.preview_code(1)
    assert out == {"a.py": "code"}
