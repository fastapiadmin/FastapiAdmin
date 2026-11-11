"""ImportUtil.find_models 去重/导入错误分支。"""

from __future__ import annotations

import importlib
from types import SimpleNamespace

import pytest

from app.utils.import_util import ImportUtil


def _clear() -> None:
    try:
        ImportUtil.find_models.cache_clear()
    except Exception:
        pass


def test_duplicate_paths_and_names(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    _clear()
    (tmp_path / "model.py").write_text("")
    monkeypatch.setattr(ImportUtil, "find_project_root", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(ImportUtil, "is_valid_model", classmethod(lambda cls, o, b: True))
    monkeypatch.setattr(ImportUtil, "_find_apscheduler_model", classmethod(lambda cls, *a: None))
    A = type("A", (), {"__tablename__": "a"})
    C = type("C", (), {"__tablename__": "a"})
    D = type("D", (), {"__tablename__": None})
    mod = SimpleNamespace(A=A, B=A, C=C, D=D)
    monkeypatch.setattr(importlib, "import_module", lambda name: mod)
    def walk(root):
        yield str(tmp_path), [], ["model.py"]
        yield str(tmp_path), [], ["model.py"]
    monkeypatch.setattr("app.utils.import_util.os.walk", walk)
    models = ImportUtil.find_models(object)
    assert A in models


def test_import_errors(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    _clear()
    (tmp_path / "model.py").write_text("")
    monkeypatch.setattr(ImportUtil, "find_project_root", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(ImportUtil, "is_valid_model", classmethod(lambda cls, o, b: True))
    monkeypatch.setattr(ImportUtil, "_find_apscheduler_model", classmethod(lambda cls, *a: None))
    import importlib as il
    def boom(name): raise ImportError("boom")
    monkeypatch.setattr(il, "import_module", boom)
    with pytest.raises(ImportError):
        ImportUtil.find_models(object)
