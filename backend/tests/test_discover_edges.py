"""动态路由发现失败提示/冲突检测。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import APIRouter, FastAPI

import app.core.discover as D


def test_import_failure_hints() -> None:
    assert "ModuleNotFound" in D._import_failure_hint(ModuleNotFoundError("x"))
    assert "ImportError" in D._import_failure_hint(ImportError("x"))
    assert "语法" in D._import_failure_hint(SyntaxError("x"))
    assert "权限" in D._import_failure_hint(PermissionError("x"))
    assert "未分类" in D._import_failure_hint(RuntimeError("x"))


def test_route_conflicts() -> None:
    app = SimpleNamespace(routes=[
        SimpleNamespace(methods={"GET"}, path="/x/{id}", name="a"),
        SimpleNamespace(methods={"GET"}, path="/x/{uid}", name="b"),
    ])
    with pytest.raises(RuntimeError):
        D.check_route_conflicts(app)
    app2 = SimpleNamespace(routes=[SimpleNamespace(methods={"GET"}, path="/y", name="c")])
    D.check_route_conflicts(app2)


def test_build_cache() -> None:
    reg = D.DynamicRouterRegistry(); reg._cache = SimpleNamespace()
    assert reg._build() is reg._cache
