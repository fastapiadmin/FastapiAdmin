"""代码生成主流程成功路径（隔离文件系统/菜单/模板）。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.modules.generator.gencode import service as mod
from app.modules.generator.gencode.schema import GenTableOutSchema
from app.modules.generator.gencode.service import GenTableService


async def test_generate_code_success(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    table = GenTableOutSchema(id=1, table_name="demo", table_comment="Demo", package_name="module_demo", module_name="demo", function_name="演示", business_name="demo")
    async def render_info(name): return [["a.py"], ["a.py"], {}, table, table]
    s = GenTableService.__new__(GenTableService); s.auth = SimpleNamespace(user=SimpleNamespace(id=1)); s.db = object()
    s._GenTableService__get_gen_render_info = render_info
    async def pkg(*a): return "module_demo"
    s._effective_package_name = pkg
    async def noop(*a, **k): return None
    s._write_plugin_migration = noop
    s._assert_parent_menu_is_catalog = noop
    async def dir_menu(*a): return 1
    s._get_or_create_package_directory_menu = dir_menu
    class T:
        async def render_async(self, **kw): return "x = 1"
    class Env:
        def get_template(self, name): return T()
    class J:
        @staticmethod
        def get_env(): return Env()
        @staticmethod
        def get_file_name(t, g): return "out.py"
        @staticmethod
        def prepare_context(t): return {}
        @staticmethod
        def sentinel_render_schema(t): return t
        @staticmethod
        def safe_render_schema(t): return t
        @staticmethod
        def iter_render_dynamic_values(t): return []
        @staticmethod
        def get_sub_table_template_list(): return []
        @staticmethod
        def prepare_sub_render_context(*a): return {}
    monkeypatch.setattr(mod, "Jinja2TemplateUtil", J)
    monkeypatch.setattr(mod, "BASE_DIR", tmp_path / "backend")
    (tmp_path / "backend").mkdir()
    monkeypatch.setattr(mod, "assert_python_structure", lambda *a, **k: None)
    monkeypatch.setattr(mod, "assert_text_structure", lambda *a, **k: None)
    class Menu:
        def __init__(self, *a): self.created=[]
        async def get(self, **kw): return None
        async def create(self, data): self.created.append(data); return SimpleNamespace(id=2)
    monkeypatch.setattr(mod, "MenuCRUD", Menu)
    assert await s.generate_code("demo") is True


async def test_batch_gen_code(monkeypatch: pytest.MonkeyPatch) -> None:
    import io, zipfile
    from app.modules.generator.gencode.schema import GenTableOutSchema
    table = GenTableOutSchema(id=1, table_name="demo", sub=False)
    s = GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    async def info(name):
        if name == "bad": raise RuntimeError("bad")
        return [["a.py"], ["out/a.py"], {}, table, table]
    s._GenTableService__get_gen_render_info = info
    class T:
        async def render_async(self, **kw): return "x"
    class Env:
        def get_template(self, name): return T()
    class J:
        @staticmethod
        def get_env(): return Env()
        @staticmethod
        def prepare_sub_render_context(*a): return {}
        @staticmethod
        def get_sub_table_template_list(): return []
        @staticmethod
        def get_file_name(*a): return "out.py"
    import app.modules.generator.gencode.service as mod
    monkeypatch.setattr(mod, "Jinja2TemplateUtil", J)
    data, failed = await s.batch_gen_code(["demo", "bad"])
    assert failed == ["bad"]
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert "out/a.py" in z.namelist()


async def test_batch_gen_code_all_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.exceptions import CustomException
    s = GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    async def info(name): raise RuntimeError("bad")
    s._GenTableService__get_gen_render_info = info
    import app.modules.generator.gencode.service as mod
    class J:
        @staticmethod
        def get_env(): return object()
    monkeypatch.setattr(mod, "Jinja2TemplateUtil", J)
    with pytest.raises(CustomException, match="未能生成"):
        await s.batch_gen_code(["bad"])
