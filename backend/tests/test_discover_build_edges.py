"""动态路由构建异常分支。"""

from __future__ import annotations

import importlib
from types import SimpleNamespace

import pytest

import app.core.discover as D


def _setup(tmp_path, dirs):
    for d in dirs:
        p = tmp_path / d / "controller.py"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text("")
    return tmp_path


def _patch(monkeypatch, tmp_path, fail=None):
    base = SimpleNamespace(__path__=[str(tmp_path)])
    real = importlib.import_module
    def fake(name):
        if name == "app.plugin":
            return base
        if fail and name.endswith(fail):
            raise ModuleNotFoundError("x")
        if name.endswith("controller"):
            return SimpleNamespace()
        return real(name)
    monkeypatch.setattr(importlib, "import_module", fake)


def test_bad_top_dir(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    _setup(tmp_path, ["weird"])
    _patch(monkeypatch, tmp_path)
    D.dynamic_router._cache = None
    assert D.dynamic_router._build() is not None


def test_no_router_and_empty_container(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    _setup(tmp_path, ["module_x"])
    _patch(monkeypatch, tmp_path)
    D.dynamic_router._cache = None
    assert D.dynamic_router._build() is not None


def test_import_failure(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    _setup(tmp_path, ["module_y"])
    _patch(monkeypatch, tmp_path, fail="module_y.controller")
    D.dynamic_router._cache = None
    with pytest.raises(RuntimeError):
        D.dynamic_router._build()
