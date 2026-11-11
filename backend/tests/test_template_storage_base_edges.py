"""模板安全/存储基类边缘。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.modules.generator.gencode.template_safety as T
from app.modules.task.storage.core.base import BaseStorageAdapter


def test_template_safety_edges() -> None:
    assert T.is_safe_identifier(None) is False
    assert T.unescape_template_text(None) == ""
    assert T.html_escape(None) == ""
    assert T.vue_label(None) == ""
    assert T.is_valid_column_type(None) is False
    assert T.is_valid_column_type("varchar(10)") is True
    assert T.pick_sqlalchemy_type("integer[]", None, db_type="postgres").startswith("ARRAY(")
    assert T.pick_sqlalchemy_type("ARRAY[]", None, db_type="postgres")
    assert T.pick_sqlalchemy_type("tinyint(1)", None, db_type="mysql") == "Boolean"
    assert T.pick_sqlalchemy_type("character", None, db_type="postgres") is not None
    with pytest.raises(SyntaxError):
        T.assert_python_syntax("a = (", filename="x.py")


def test_storage_delete_dir_edges() -> None:
    class A(BaseStorageAdapter):
        def _sync_list_recursive(self, p):
            return [SimpleNamespace(is_dir=True, key="d/sub"), SimpleNamespace(is_dir=False, key="d/a")]
        def _sync_rmdir(self, p): raise RuntimeError("x")
        def _sync_delete(self, p): pass
        def _sync_upload(self, *a): pass
        def _sync_download(self, *a): pass
        def _sync_copy(self, *a): pass
        def _sync_exists(self, *a): return False
        def _sync_list(self, *a): return []
        def _sync_mkdir(self, *a): pass
        def _sync_rename(self, *a): pass
        def _sync_test_connection(self): return True
    a = object.__new__(A)
    a._sync_delete_dir("d")
    assert a._sync_delete_dir("d") is None
