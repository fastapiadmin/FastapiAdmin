"""辅助函数 — 把 pip-licenses 输出的原始 JSON 转换成模板友好的精简数据。

为什么不直接渲染原始 JSON:
- LicenseText 全文可能数 MB
- 模板只需要摘要信息 (Name/Version/License)
- 按 License 分组便于阅读
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict


class PackageInfo(TypedDict):
    name: str
    version: str
    license: str


class LicenseGroup(TypedDict):
    license: str
    packages: list[PackageInfo]


_LICENSES_JSON_PATH = Path(__file__).parent / "oss_licenses.json"


def load_oss_licenses() -> list[LicenseGroup]:
    """
    加载项目依赖的开源许可证清单，按许可证类型分组。

    返回:
    - list[LicenseGroup]: 形如 [{"license": "MIT", "packages": [{"name": ..., "version": ...}, ...]}, ...]
    """
    raw = json.loads(_LICENSES_JSON_PATH.read_text(encoding="utf-8"))
    groups: dict[str, list[PackageInfo]] = {}
    for pkg in raw:
        license_name = pkg.get("License") or "Unknown"
        groups.setdefault(license_name, []).append(
            PackageInfo(
                name=pkg["Name"],
                version=pkg.get("Version", "-"),
                license=license_name,
            )
        )
    sorted_groups: list[LicenseGroup] = []
    for license_name in sorted(groups.keys(), key=str.lower):
        pkgs = sorted(groups[license_name], key=lambda p: p["name"].lower())
        sorted_groups.append(LicenseGroup(license=license_name, packages=pkgs))
    return sorted_groups
