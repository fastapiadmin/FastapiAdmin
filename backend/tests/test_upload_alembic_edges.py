"""上传工具/公告迁移升级降级分支。"""

from __future__ import annotations

import importlib
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import app.utils.upload_util as U
from app.core.exceptions import CustomException


def test_upload_small_helpers(tmp_path) -> None:
    assert U.UploadUtil.generate_safe_filename("nofile", ".txt")
    assert U.UploadUtil.check_file_machine("abc") is False
    assert U.UploadUtil.check_file_random_code("abc") is False
    d = tmp_path / "d"; d.mkdir()
    assert U.UploadUtil.delete_file(d) is False


async def test_upload_file_errors(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(U.settings, "UPLOAD_FILE_PATH", tmp_path)
    class F:
        def __init__(self, name): self.filename = name
        async def read(self, n=-1): return b""
        async def seek(self, pos): return 0
    with pytest.raises(CustomException):
        await U.UploadUtil.upload_file(F("noext"), "http://x")
    with pytest.raises(CustomException):
        await U.UploadUtil.upload_file(F(""), "http://x")
    monkeypatch.setattr(U.UploadUtil, "validate_file_content_type", staticmethod(lambda *a: None))
    monkeypatch.setattr(U.UploadUtil, "check_file_size", staticmethod(lambda *a: None))
    ext = U.settings.ALLOWED_EXTENSIONS[0]
    assert await U.UploadUtil.upload_file(F("a" + ext), "http://x", upload_type="resource", target_path="sub")


def test_migration_upgrade_downgrade(monkeypatch: pytest.MonkeyPatch) -> None:
    mod = importlib.import_module("app.alembic.versions.2026_11_03_0900_a1b2c3d4e5f6")
    op = MagicMock()
    class B:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def create_index(self, *a, **k): pass
        def drop_index(self, *a, **k): pass
        def f(self, x): return x
    op.batch_alter_table.return_value = B()
    op.f.side_effect = lambda x: x
    monkeypatch.setattr(mod, "op", op)
    mod.upgrade(); mod.downgrade()
