"""上传工具纯函数与文件安全分支。"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.utils.upload_util import UploadUtil


def test_filename_safety_and_extension() -> None:
    assert UploadUtil.sanitize_filename("") == ""
    assert UploadUtil.sanitize_filename("../../a.txt") == "a.txt"
    assert UploadUtil.sanitize_filename("...") .startswith("file_")
    assert UploadUtil.check_path_traversal("a.txt") is True
    assert UploadUtil.check_path_traversal("../a") is False
    assert UploadUtil.get_extension_from_filename("A.JPG") == ".jpg"
    assert UploadUtil.get_extension_from_filename("noext") == ""
    assert UploadUtil.is_dangerous_extension(".EXE") is True
    assert UploadUtil.is_dangerous_extension(".jpg") is False


def test_detect_file_types() -> None:
    assert UploadUtil.detect_file_type(b"\xff\xd8\xff") == "image/jpeg"
    assert UploadUtil.detect_file_type(b"\x89PNG\r\n\x1a\n") == "image/png"
    assert UploadUtil.detect_file_type(b"GIF89a") == "image/gif"
    assert UploadUtil.detect_file_type(b"%PDF-1") == "application/pdf"
    assert UploadUtil.detect_file_type(b"PK\x03\x04[Content_Types].xml") == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert UploadUtil.detect_file_type(b"PK\x03\x04") == "application/zip"
    assert UploadUtil.detect_file_type(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1") == "application/msword"
    assert UploadUtil.detect_file_type(b"unknown") is None


def test_validate_extension_and_content() -> None:
    assert UploadUtil.validate_file_extension(".jpg") is True
    with pytest.raises(CustomException, match="不允许上传"):
        UploadUtil.validate_file_extension(".exe")
    with pytest.raises(CustomException, match="不支持"):
        UploadUtil.validate_file_extension(".unknown")
    assert UploadUtil.validate_file_content_type(b"plain", ".txt") is True


def test_size_and_safe_name_and_checks() -> None:
    assert UploadUtil.check_file_size(SimpleNamespace(size=1)) is True
    with pytest.raises(CustomException, match="文件大小"):
        UploadUtil.check_file_size(SimpleNamespace(size=settings.MAX_FILE_SIZE + 1))
    name = UploadUtil.generate_safe_filename("a" * 80 + ".txt", ".txt")
    assert len(name) > 10 and name.endswith(".txt")
    assert UploadUtil.check_file_timestamp("a_20260101120000A001.txt") is True
    assert UploadUtil.check_file_timestamp("bad.txt") is False
    assert UploadUtil.check_file_machine("aA.txt") is False
    assert UploadUtil.check_file_random_code("a001.txt") is True
    assert UploadUtil.check_file_random_code("a000.txt") is False


def test_target_path_and_delete(tmp_path: Path) -> None:
    assert UploadUtil._sanitize_target_path("") == ""
    assert UploadUtil._sanitize_target_path("/a//./b.txt") == "a/b.txt"
    with pytest.raises(CustomException, match="非法"):
        UploadUtil._sanitize_target_path("../x")
    f = tmp_path / "x"; f.write_text("x")
    assert UploadUtil.delete_file(f) is True
    assert UploadUtil.delete_file(f) is True
    assert UploadUtil.check_file_exists(str(f)) is False
