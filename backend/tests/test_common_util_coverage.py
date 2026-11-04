"""common_util 常用树/字节/查询转换分支测试。"""

from types import SimpleNamespace

import pytest
from pydantic import BaseModel, Field

from app.core.exceptions import CustomException
from app.utils.common_util import (
    bytes2file_response,
    bytes2human,
    compute_menu_route_first_segment,
    get_child_id_map,
    get_child_recursion,
    get_parent_id_map,
    get_parent_recursion,
    get_random_character,
    recursive_to_tree,
    search_to_dict,
    traversal_to_tree,
    uuid4_str,
)


class _Query(BaseModel):
    name: str | None = Field(default=None, json_schema_extra={"q": "like"})
    created_time: list[str] | None = None
    begin_date_start: str | None = None
    begin_date_end: str | None = None


def test_ids_random_and_uuid() -> None:
    assert len(get_random_character()) == 32
    assert len(uuid4_str()) == 36


def test_search_to_dict() -> None:
    assert search_to_dict(None, {"x": 1}) == {"x": 1}
    assert search_to_dict(None) is None
    q = _Query(name="a", created_time=["x", "y"], begin_date_start="s", begin_date_end="e")
    d = search_to_dict(q)
    assert d is not None
    assert d["name"] == ("like", "a")
    assert d["created_time"] == ("between", ["x", "y"])
    assert d["begin_date"] == ("between", ["s", "e"])


def test_parent_child_maps_and_recursion() -> None:
    rows = [SimpleNamespace(id=1, parent_id=None), SimpleNamespace(id=2, parent_id=1), SimpleNamespace(id=3, parent_id=2)]
    pmap = get_parent_id_map(rows)
    assert pmap == {1: None, 2: 1, 3: 2}
    assert get_parent_recursion(3, pmap) == [3, 2, 1]
    with pytest.raises(CustomException):
        get_parent_recursion(2, {2: 2})
    cmap = get_child_id_map(rows)
    assert cmap[1] == [2] and cmap[2] == [3]
    assert get_child_recursion(1, cmap) == [1, 2, 3]


def test_trees() -> None:
    nodes = [
        {"id": 1, "parent_id": None},
        {"id": 2, "parent_id": 1},
        {"id": 3, "parent_id": 99},
    ]
    tree = traversal_to_tree(nodes)
    assert {n["id"] for n in tree} == {1, 3}
    assert tree[0]["children"][0]["id"] == 2
    assert recursive_to_tree(nodes)[0]["children"][0]["id"] == 2
    assert recursive_to_tree([]) == []


def test_bytes_and_stream() -> None:
    assert bytes2human(0) == "0.0B"
    assert bytes2human(1024) == "1.0KB"
    assert bytes2human(1024**2) == "1.0MB"
    assert list(bytes2file_response(b"abc")) == [b"abc"]


def test_menu_route_segment() -> None:
    assert compute_menu_route_first_segment(None, "system", None) == "module_system"
    assert compute_menu_route_first_segment(None, "module_system", None) == "module_system"
    with pytest.raises(CustomException):
        compute_menu_route_first_segment(None, "", None)
