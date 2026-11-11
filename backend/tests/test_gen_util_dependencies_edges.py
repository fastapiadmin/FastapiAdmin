"""代码生成类型工具 / 认证依赖边缘。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.modules.generator.gencode.gen_util as G
from app.core.exceptions import CustomException
import app.core.dependencies as D


def test_type_helpers() -> None:
    assert G.GenUtils.get_db_type("varchar(20) COLLATE x UNSIGNED") == "varchar"
    assert G.GenUtils.get_db_type("integer[]") == "array"
    assert G.GenUtils.get_db_type("ARRAY[INTEGER]") == "array"
    assert G.GenUtils.get_db_type("") == ""
    assert G.GenUtils.get_column_length("varchar(20)") == 20
    assert G.GenUtils.get_column_length("") == 0
    assert G.GenUtils.get_column_length("x(bad)") == 0


async def test_authenticate_guards(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(CustomException):
        await D._authenticate("", None, None)
    with pytest.raises(CustomException):
        await D._authenticate("Bearer ", None, None)
    monkeypatch.setattr(D, "decode_access_token", lambda *a, **k: None)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, None)
    payload = SimpleNamespace(is_refresh=True, sub="s")
    monkeypatch.setattr(D, "decode_access_token", lambda *a, **k: payload)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, None)
    payload = SimpleNamespace(is_refresh=False, sub=None)
    monkeypatch.setattr(D, "decode_access_token", lambda *a, **k: payload)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, None)


async def test_authenticate_session_guards(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = SimpleNamespace(is_refresh=False, sub="s")
    monkeypatch.setattr(D, "decode_access_token", lambda *a, **k: payload)
    class R:
        def __init__(self, *a): pass
        async def get(self, *a): return None
    monkeypatch.setattr(D, "RedisCURD", R)
    with pytest.raises(CustomException):
        await D._authenticate("x", None, object())


def test_gen_util_column_init(monkeypatch) -> None:
    from app.modules.generator.gencode.schema import GenTableColumnSchema
    import app.modules.generator.gencode.gen_util as G
    for db in ("mysql", "postgres"):
        monkeypatch.setattr(G.settings, "DATABASE_TYPE", db)
        c = GenTableColumnSchema(column_name="g", column_type="geometry", python_type="")
        G.GenUtils.init_column_field(c, type("T", (), {"table_name": "t", "id": 1})())
        assert c.python_type in ("bytes", "list")
    assert G.GenUtils.get_column_length("decimal(10,2)") == 10
    assert G.GenUtils.get_column_length("decimal(bad)") == 0
