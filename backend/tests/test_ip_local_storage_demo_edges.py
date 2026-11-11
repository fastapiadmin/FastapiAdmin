"""IP 归属地/本地上传适配器/示例处理器边缘。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.utils.ip_local_util as I
from app.core.exceptions import CustomException
from app.modules.task.storage.core.local_adapter import LocalStorageAdapter
from app.modules.task.cronjob.node.handlers import demo_handler as D


def test_searcher_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(I, "_searcher", None)
    monkeypatch.setattr(I, "_searcher_init_failed", False)
    monkeypatch.setattr(I.xdb_util, "load_content_from_file", lambda p: (_ for _ in ()).throw(RuntimeError("x")))
    assert I._get_searcher() is None
    assert I._get_searcher() is None
    monkeypatch.setattr(I, "_searcher", object())
    assert I._get_searcher() is not None
    monkeypatch.setattr(I, "_searcher", None)
    monkeypatch.setattr(I, "_searcher_init_failed", False)
    monkeypatch.setattr(I.xdb_util, "load_content_from_file", lambda p: b"x")
    monkeypatch.setattr(I.xdb, "new_with_buffer", lambda *a: SimpleNamespace(search=lambda ip: "x"))
    assert I._get_searcher() is not None


def test_query_offline_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(I, "_get_searcher", lambda: None)
    assert I.IpLocalUtil._query_offline("1.1.1.1") == I.LOCATION_UNKNOWN
    monkeypatch.setattr(I, "_get_searcher", lambda: SimpleNamespace(search=lambda ip: (_ for _ in ()).throw(RuntimeError("x"))))
    assert I.IpLocalUtil._query_offline("1.1.1.1") == I.LOCATION_UNKNOWN
    assert I.IpLocalUtil._query_offline("::1") == I.LOCATION_UNKNOWN


def test_local_adapter_errors(tmp_path) -> None:
    a = LocalStorageAdapter(__import__("app.modules.task.storage.core.base", fromlist=["StorageAdapterConfig"]).StorageAdapterConfig(protocol="local", host=str(tmp_path), port=0))
    with pytest.raises(CustomException):
        a._abs_path("../x")
    with pytest.raises(Exception):
        a._sync_upload(str(tmp_path / "missing"), "a.txt")
    with pytest.raises(Exception):
        a._sync_download("missing", str(tmp_path / "x"))
    with pytest.raises(Exception):
        a._sync_list("missing")
    f = tmp_path / "f"; f.write_text("x")
    with pytest.raises(Exception):
        a._sync_mkdir("f")
    d = tmp_path / "d"; d.mkdir(); (d / "x").write_text("x")
    with pytest.raises(Exception):
        a._sync_rmdir("d")
    with pytest.raises(Exception):
        a._sync_rename("missing", "x")
    with pytest.raises(Exception):
        a._sync_copy("missing", "x")


def test_demo_handler_ops() -> None:
    assert D.demo_handler(1, a=2)
    assert D.process_data([]) == {"error": "数据为空"}
    assert D.process_data([1, 2], "sum")["result"] == 3
    assert D.process_data([1, 2], "avg")["result"] == 1.5
    assert D.process_data([1, 2], "max")["result"] == 2
    assert D.process_data([1, 2], "min")["result"] == 1
    assert D.process_data([1, 2], "count")["result"] == 2
    assert "不支持" in D.process_data([1], "x")["error"]
