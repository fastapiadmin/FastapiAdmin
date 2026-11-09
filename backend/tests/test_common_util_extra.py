"""通用模块导入/文件路径/序列化工具。"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.core.exceptions import CustomException
from app.utils import common_util as C
from app.utils.common_util import SqlalchemyUtil


def test_import_module_errors() -> None:
    with pytest.raises(ModuleNotFoundError):
        C.import_module("no_such_module_xyz.Class", "X")
    with pytest.raises(AttributeError):
        C.import_module("json.NoSuchAttr", "X")
    assert C.import_module("json.dumps", "X") is __import__("json").dumps


def test_get_filepath_from_url() -> None:
    p = C.get_filepath_from_url("/api?task_id=1&file_name=a.txt&task_path=up")
    assert p.name == "a.txt" and "1" in str(p) and "up" in str(p)


def test_sqlalchemy_util_serialization() -> None:
    from app.modules.system.user.model import UserModel
    u = UserModel(username="u", name="N")
    assert SqlalchemyUtil.base_to_dict(u)["username"] == "u"
    assert SqlalchemyUtil.base_to_dict({"a_b": 1}, "snake_to_camel") == {"AB": 1}
    assert SqlalchemyUtil.base_to_dict({"AB": 1}, "camel_to_snake") == {"ab": 1}
    assert SqlalchemyUtil.serialize_result([u])[0]["name"] == "N"
    assert SqlalchemyUtil.serialize_result({"a": 1}) == {"a": 1}
    assert SqlalchemyUtil.get_server_default_null("postgresql") is not None


def test_compute_menu_route_first_segment() -> None:
    assert C.compute_menu_route_first_segment(None, "module_x", None) == "module_x"
    assert C.compute_menu_route_first_segment(None, "x", None) == "module_x"
    with pytest.raises(CustomException):
        C.compute_menu_route_first_segment(None, "", None)
