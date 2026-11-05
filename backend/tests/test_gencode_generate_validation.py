"""代码生成写入前校验。"""

from __future__ import annotations

import pytest

from app.core.exceptions import CustomException
from app.modules.generator.gencode.schema import GenTableOutSchema
from app.modules.generator.gencode.service import GenTableService


def _svc():
    return GenTableService.__new__(GenTableService)


async def test_generate_rejects_empty_table() -> None:
    with pytest.raises(CustomException, match="表名不能为空"):
        await _svc().generate_code("")


async def test_generate_rejects_missing_module_and_function(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.generator.gencode import service as mod
    svc = _svc()
    table = GenTableOutSchema(table_name="demo", package_name="module_demo", module_name=None, function_name=None)
    async def render_info(name): return [[], [], [], table, table]
    svc._GenTableService__get_gen_render_info = render_info
    async def pkg(*a): return "module_demo"
    svc._effective_package_name = pkg
    class J:
        @staticmethod
        def get_env(): return object()
    monkeypatch.setattr(mod, "Jinja2TemplateUtil", J)
    with pytest.raises(CustomException, match="模块名不能为空"):
        await svc.generate_code("demo")
    table.module_name = "demo"
    with pytest.raises(CustomException, match="功能名称不能为空"):
        await svc.generate_code("demo")
