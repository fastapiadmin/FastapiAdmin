"""上传工具文件树/删除边界。"""

from __future__ import annotations

from app.utils.upload_util import UploadUtil


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
