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


def test_app_menu_scope_matches_mobile_tabs() -> None:
    seed = json.loads(MENU_SEED.read_text(encoding="utf-8"))
    app_menus = [n for n in seed if n.get("scope") == "app"]
    assert [n.get("name") for n in app_menus] == ["首页", "工作台", "我的"]
    assert [n.get("route_name") for n in app_menus] == ["AppHome", "AppWork", "AppMine"]


def test_official_site_is_external_link_not_embedded_page() -> None:
    seed = json.loads(MENU_SEED.read_text(encoding="utf-8"))
    nodes = list(_walk(seed))
    assert not any(n.get("component_path") == "module_swagger/docs/index" for n in nodes)
    official = next(n for n in nodes if n.get("route_name") == "OfficialSite")
    assert official["type"] == 4
    assert official["link"] == "https://service.fastapiadmin.com/"
    assert official["is_iframe"] is False


def test_cronjob_menu_is_merged() -> None:
    seed = json.loads(MENU_SEED.read_text(encoding="utf-8"))
    cronjob = next(n for n in _walk(seed) if n.get("route_name") == "Cronjob")
    assert cronjob["type"] == 2
    assert cronjob["component_path"] == "module_task/cronjob/index"
    assert cronjob["permission"] is None
    assert cronjob["redirect"] is None
    assert not any(n.get("route_name") in {"Job", "Node"} for n in _walk(seed))
    permissions = {n.get("permission") for n in cronjob["children"]}
    assert "module_task:cronjob:job:query" in permissions
    assert "module_task:cronjob:node:create" in permissions


def test_system_menu_is_grouped() -> None:
    seed = json.loads(MENU_SEED.read_text(encoding="utf-8"))
    system = next(n for n in seed if n.get("name") == "系统管理")
    assert [n.get("name") for n in system["children"]] == ["组织与权限", "系统配置", "内容与审计"]
    for group in system["children"]:
        assert group["type"] == 1
        assert group["children"]
        for child in group["children"]:
            assert child["route_path"].startswith("/system/")


def test_ai_memory_menu_is_renamed() -> None:
    seed = json.loads(MENU_SEED.read_text(encoding="utf-8"))
    memory = next(n for n in _walk(seed) if n.get("route_name") == "Memory")
    assert memory["name"] == "AI 会话记录"
