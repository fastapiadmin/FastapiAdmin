"""存储基类配置/端点/高级字段覆盖。"""

from __future__ import annotations

import pytest

from app.modules.task.storage.core.base import (
    ADVANCED_FIELD_DEFS,
    StorageObject,
    StoragePage,
    StorageProtocol,
    decrypt_password,
    encrypt_password,
    normalize_endpoint,
    parse_advanced_config,
)


def test_endpoint_and_password() -> None:
    assert normalize_endpoint(None) is None
    assert normalize_endpoint("") == ""
    assert normalize_endpoint("s3.example.com") == "https://s3.example.com"
    assert normalize_endpoint("s3.example.com", "http") == "http://s3.example.com"
    assert normalize_endpoint("http://x") == "http://x"
    token = encrypt_password("secret")
    assert decrypt_password(token) == "secret"
    assert encrypt_password(None) == ""
    assert decrypt_password(None) == ""


def test_advanced_config_and_field_defs() -> None:
    assert parse_advanced_config(StorageProtocol.LOCAL, {}) is None
    s3 = parse_advanced_config(StorageProtocol.S3, {"addressing_style": "path"})
    assert s3 is not None and s3.addressing_style == "path"
    assert "s3" in ADVANCED_FIELD_DEFS
    keys = {d.key: d for d in ADVANCED_FIELD_DEFS["s3"]}
    assert keys["addressing_style"].type == "select"
    assert keys["signature_version"].options


def test_storage_object_page() -> None:
    o = StorageObject(name="a", key="a", size=1)
    p = StoragePage(items=[o], has_next=True, next_cursor="c")
    assert p.items[0].name == "a" and p.has_next is True


def test_adapter_bucket_and_multipart() -> None:
    from app.core.exceptions import CustomException
    from app.modules.task.storage.core.base import BaseStorageAdapter, StorageAdapterConfig
    cfg=StorageAdapterConfig(protocol=StorageProtocol.S3,port=443,bucket="b",username="u",password="p")
    class Dummy(BaseStorageAdapter):
        def _sync_test_connection(self): return True
        def _sync_upload(self, a, b): return b
        def _sync_download(self, a, b): return b
        def _sync_delete(self, a): return None
        def _sync_exists(self, a): return False
        def _sync_list(self, a): return []
        def _sync_mkdir(self, a): return None
        def _sync_rmdir(self, a): return None
        def _sync_rename(self, a, b): return None
        def _sync_copy(self, a, b): return None
    a=Dummy(cfg)
    assert a._require_bucket()=="b"
    a.set_bucket("b2"); assert a.bucket_name=="b2"
    a.bucket_name=""
    try:
        a._require_bucket()
    except CustomException:
        pass
    else:
        raise AssertionError("expected")
    cfg.multipart_part_size=50; cfg.multipart_concurrency=6; cfg.multipart_memory_budget=512
    assert a._multipart_settings()==(50*1024*1024,6,True)
    cfg.transfer_mode="stream"
    assert a._multipart_settings()[2] is False


def test_entries_from_keys() -> None:
    from app.modules.task.storage.core.base import BaseStorageAdapter
    items=BaseStorageAdapter._entries_from_keys(["a/b/","a/b/c","a/d","a/b",""])
    assert [x.key for x in items if x.is_dir]==["a","a/b"]
    assert [x.key for x in items if not x.is_dir]==["a/b","a/b/c","a/d"]


def test_recursive_dir_ops(tmp_path) -> None:
    from app.modules.task.storage.core.base import BaseStorageAdapter, StorageAdapterConfig, StorageObject
    class D(BaseStorageAdapter):
        def __init__(self,cfg): super().__init__(cfg); self.calls=[]
        def _sync_test_connection(self): return True
        def _sync_upload(self,a,b): self.calls.append(("up",a,b)); return b
        def _sync_download(self,a,b): return b
        def _sync_delete(self,a): self.calls.append(("del",a))
        def _sync_exists(self,a): return False
        def _sync_list(self,a): return []
        def _sync_mkdir(self,a): self.calls.append(("mkdir",a))
        def _sync_rmdir(self,a): self.calls.append(("rmdir",a))
        def _sync_rename(self,a,b): return None
        def _sync_copy(self,a,b): self.calls.append(("copy",a,b))
        def _sync_list_recursive(self,prefix):
            return [StorageObject(name="sub",key="src/sub",is_dir=True),StorageObject(name="a",key="src/sub/a",is_dir=False)]
    cfg=StorageAdapterConfig(protocol=StorageProtocol.LOCAL,port=0,bucket="")
    a=D(cfg)
    a._sync_copy_dir("src/","dst/")
    assert ("mkdir","dst/sub") in a.calls and ("copy","src/sub/a","dst/sub/a") in a.calls
    a.calls.clear(); a._sync_move_dir("src","dst")
    assert any(c[0]=="copy" for c in a.calls) and any(c[0]=="del" for c in a.calls)
    a.calls.clear(); a._sync_delete_dir("src")
    assert any(c[0]=="del" for c in a.calls)
    with pytest.raises(Exception):
        a._sync_upload_dir(str(tmp_path/"missing"),"r",1)


def test_bulk_upload_download(tmp_path) -> None:
    from app.modules.task.storage.core.base import BaseStorageAdapter, StorageAdapterConfig, StorageObject
    class D(BaseStorageAdapter):
        def __init__(self,cfg): super().__init__(cfg); self.fail=False; self.entries=[]
        def _sync_test_connection(self): return True
        def _sync_upload(self,a,b):
            if self.fail: raise RuntimeError("up")
            return b
        def _sync_download(self,a,b):
            if self.fail: raise RuntimeError("down")
            Path(b).write_text("x"); return b
        def _sync_delete(self,a): pass
        def _sync_exists(self,a): return False
        def _sync_list(self,a): return []
        def _sync_mkdir(self,a): pass
        def _sync_rmdir(self,a): pass
        def _sync_rename(self,a,b): pass
        def _sync_copy(self,a,b): pass
        @property
        def concurrency_safe(self): return True
        def _sync_list_recursive(self,prefix): return self.entries
    cfg=StorageAdapterConfig(protocol=StorageProtocol.LOCAL,port=0,bucket="")
    d=tmp_path/"src"; d.mkdir(); (d/"a.txt").write_text("a"); (d/"sub").mkdir(); (d/"sub"/"b.txt").write_text("b")
    a=D(cfg)
    assert a._sync_upload_dir(str(d),"r",2)==2
    assert a._sync_upload_dir(str(tmp_path/"empty"),"r",2)==0 if (tmp_path/"empty").mkdir() is None else True
    a.fail=True
    with pytest.raises(RuntimeError): a._sync_upload_dir(str(d),"r",2)
    a.fail=False; a.entries=[StorageObject(name="a",key="r/a",is_dir=False)]
    assert a._sync_download_dir("r",str(tmp_path/"out"),2)==1
    a.entries=[]; assert a._sync_download_dir("r",str(tmp_path/"out"),2)==0
    a.entries=[StorageObject(name="a",key="r/a",is_dir=False)]; a.fail=True
    with pytest.raises(RuntimeError): a._sync_download_dir("r",str(tmp_path/"out2"),2)
