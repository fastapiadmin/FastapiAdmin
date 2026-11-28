"""菜单权限种子与公共文件权限回归测试。"""

import json
from pathlib import Path

MENU_SEED = Path(__file__).resolve().parents[1] / "sql" / "sys_menu.json"


def _walk(nodes):
    for node in nodes:
        yield node
        yield from _walk(node.get("children") or [])


def test_common_file_permissions_are_assignable() -> None:
    permissions = {n.get("permission") for n in _walk(json.loads(MENU_SEED.read_text(encoding="utf-8")))}
    assert "module_common:file:upload" in permissions
    assert "module_common:file:download" in permissions


def test_detail_permissions_exist() -> None:
    permissions = {n.get("permission") for n in _walk(json.loads(MENU_SEED.read_text(encoding="utf-8")))}
    assert "module_system:log:detail" in permissions
    assert "module_monitor:cache:detail" in permissions



def test_ops_module_permissions_removed() -> None:
    permissions = {n.get("permission") for n in _walk(json.loads(MENU_SEED.read_text(encoding="utf-8")))}
    assert not any((p or "").startswith("module_ops:") for p in permissions)
