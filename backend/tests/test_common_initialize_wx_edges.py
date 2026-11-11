"""common_util / initialize / wx 小程序边缘。"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import app.utils.common_util as U


def test_import_helpers() -> None:
    assert U.import_module("os.path.join", "os") is not None
    with pytest.raises(ModuleNotFoundError):
        U.import_module("no_such_mod.x", "x")
    with pytest.raises(AttributeError):
        U.import_module("os.no_such_attr", "x")


async def test_async_import_attribute_error() -> None:
    with pytest.raises(AttributeError):
        await U.import_modules_async(["os.no_such"], "x")
    await U.import_modules_async([""], "x")


def test_tree_and_serialize() -> None:
    nodes = [{"id": 1, "parent_id": None, "name": "a"}]
    tree = U.traversal_to_tree(nodes)
    assert tree and "children" in tree[0]
    assert U.CamelCaseUtil.snake_to_camel("a_b") == "AB"
    assert U.SnakeCaseUtil.camel_to_snake("aB") == "a_b"
    assert U.SqlalchemyUtil.get_server_default_null("postgres") is not None
    assert U.SqlalchemyUtil.get_boolean_server_default("mysql", True) is not None
