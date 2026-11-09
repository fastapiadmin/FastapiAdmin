"""上传工具文件树/删除边界。"""

from __future__ import annotations

from app.utils.upload_util import UploadUtil
import pytest


def test_get_file_tree(tmp_path) -> None:
    (tmp_path / "a.txt").write_text("x")
    sub = tmp_path / "sub"; sub.mkdir(); (sub / "b.txt").write_text("y")
    tree = UploadUtil.get_file_tree(str(tmp_path))
    assert tree
    names = [n["name"] for n in tree]
    assert "a.txt" in names and "sub" in names


def test_delete_file(tmp_path) -> None:
    p = tmp_path / "x.txt"; p.write_text("x")
    assert UploadUtil.delete_file(p) is True
    assert UploadUtil.delete_file(p) is True

async def test_upload_file_success(tmp_path, monkeypatch) -> None:
    from io import BytesIO
    from fastapi import UploadFile
    from app.utils.upload_util import UploadUtil
    monkeypatch.setattr("app.utils.upload_util.settings.UPLOAD_FILE_PATH", tmp_path)
    monkeypatch.setattr(UploadUtil, "validate_file_content_type", staticmethod(lambda *a: True))
    name, path, url = await UploadUtil.upload_file(UploadFile(filename="a.png", file=BytesIO(b"png")), "http://x", upload_type="file")
    assert name and path.exists() and path.read_text() == "png" and url.startswith("http://x")


async def test_upload_file_resource_path(tmp_path, monkeypatch) -> None:
    from io import BytesIO
    from fastapi import UploadFile
    from app.utils.upload_util import UploadUtil
    monkeypatch.setattr("app.utils.upload_util.settings.UPLOAD_FILE_PATH", tmp_path)
    monkeypatch.setattr(UploadUtil, "validate_file_content_type", staticmethod(lambda *a: True))
    name, path, _ = await UploadUtil.upload_file(UploadFile(filename="b.png", file=BytesIO(b"png")), "http://x", upload_type="resource", target_path="docs")
    assert "resource" in str(path) and "docs" in str(path)


async def test_upload_file_rejects(tmp_path, monkeypatch) -> None:
    from io import BytesIO
    from fastapi import UploadFile
    from app.core.exceptions import CustomException
    from app.utils.upload_util import UploadUtil
    monkeypatch.setattr("app.utils.upload_util.settings.UPLOAD_FILE_PATH", tmp_path)
    with pytest.raises(CustomException):
        await UploadUtil.upload_file(UploadFile(filename="../x.txt", file=BytesIO(b"x")), "http://x")
    with pytest.raises(CustomException):
        await UploadUtil.upload_file(UploadFile(filename="", file=BytesIO(b"x")), "http://x")
