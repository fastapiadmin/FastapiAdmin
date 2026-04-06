"""扫描 ``app.plugin`` 下 ``module_*`` 插件目录，并解析可选 ``plugin.toml``。"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any


def _loads_toml(raw: bytes) -> dict[str, Any]:
    text = raw.decode("utf-8")
    if sys.version_info >= (3, 11):
        import tomllib

        return tomllib.loads(text)
    import tomli as tomllib  # type: ignore[import-not-found, unused-ignore]

    return tomllib.loads(text)


def plugin_root_dir() -> Path:
    """``app.plugin`` 包所在目录（即 ``app/plugin``）。"""
    pkg = importlib.import_module("app.plugin")
    return Path(next(iter(pkg.__path__)))


def iter_module_plugin_dirs() -> list[Path]:
    """
    列出 ``module_*`` 顶级插件目录，按目录名排序。

    返回:
    - list[Path]: 每个元素为 ``.../app/plugin/module_xxx`` 目录路径。
    """
    root = plugin_root_dir()
    out: list[Path] = []
    for p in sorted(root.iterdir()):
        if p.is_dir() and p.name.startswith("module_") and not p.name.startswith("module__"):
            out.append(p)
    return out


def parse_plugin_toml(path: Path) -> dict[str, Any]:
    """
    读取并解析 ``plugin.toml``。

    参数:
    - path (Path): ``plugin.toml`` 文件路径。

    返回:
    - dict[str, Any]: TOML 顶层表。

    异常:
    - OSError / tomllib 解析错误：向上抛出。
    """
    return _loads_toml(path.read_bytes())


def build_plugin_info(module_dir: Path) -> dict[str, Any]:
    """
    构建单个插件的展示信息（供管理端与 OpenAPI 使用）。

    参数:
    - module_dir (Path): ``.../module_xxx`` 目录。

    返回:
    - dict: 含 ``module_dir``、``route_prefix``、``has_manifest`` 及 manifest 字段。
    """
    name = module_dir.name
    segment = name[7:] if name.startswith("module_") else ""
    route_prefix = f"/{segment}" if segment else "/"

    info: dict[str, Any] = {
        "module_dir": name,
        "route_prefix": route_prefix,
        "has_manifest": False,
        "name": None,
        "title": None,
        "version": None,
        "description": None,
        "optional": None,
        "tags": None,
        "manifest_name_mismatch": None,
    }

    manifest_path = module_dir / "plugin.toml"
    if not manifest_path.is_file():
        return info

    info["has_manifest"] = True
    data = parse_plugin_toml(manifest_path)
    info["name"] = data.get("name")
    info["title"] = data.get("title")
    info["version"] = data.get("version")
    info["description"] = data.get("description")
    info["optional"] = data.get("optional")
    tags = data.get("tags")
    info["tags"] = tags if isinstance(tags, list) else None

    declared = info["name"]
    if isinstance(declared, str) and declared and declared != segment:
        info["manifest_name_mismatch"] = True
    else:
        info["manifest_name_mismatch"] = False

    return info


def list_plugin_infos() -> list[dict[str, Any]]:
    """
    列出所有 ``module_*`` 插件的汇总信息（含可选 manifest）。

    返回:
    - list[dict[str, Any]]: 按 ``module_dir`` 排序的列表。
    """
    return [build_plugin_info(d) for d in iter_module_plugin_dirs()]
