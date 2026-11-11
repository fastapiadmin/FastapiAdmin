"""菜单 schema 归一化分支。"""

from __future__ import annotations

import pytest


def test_menu_update_normalize() -> None:
    from app.modules.system.menu.schema import MenuCreateSchema, MenuUpdateSchema
    m = MenuUpdateSchema(name="x", type=None, order=1, show_text_badge=None)
    assert m.type is None
    m2 = MenuUpdateSchema(name="x", type=1, order=1, route_name="X", route_path="/x", redirect="/x", show_text_badge="  a  ")
    assert m2.show_text_badge == "a"
    with pytest.raises(Exception):
        MenuUpdateSchema(name="x", type=1, order=1, parent_id="bad")
    with pytest.raises(Exception):
        MenuCreateSchema(name="x", type=1, order=1, parent_id="bad")
    with pytest.raises(Exception):
        MenuUpdateSchema(name="x", type=2, order=1, route_name="X", route_path="/x", component_path="/x")
    with pytest.raises(Exception):
        MenuUpdateSchema(name="x", type=2, order=1, route_name="X", route_path="/x", redirect="/x", component_path="/x")
