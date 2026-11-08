"""存储节点配置构造/默认标记。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.modules.task.storage.core.base import StorageProtocol
from app.modules.task.storage.node.service import StorageNodeService


def _src(**over):
    data=dict(protocol="s3",host="h",port=0,username="u",bucket="b",endpoint="e",scheme="https",region="r",path_prefix=None,is_secure=False,implicit_tls=False,encrypt_type=1,connection_mode=0,encoding="UTF-8",multipart_part_size=50,multipart_concurrency=6,multipart_memory_budget=512,advanced_config=None)
    data.update(over); return SimpleNamespace(**data)


def test_build_config_defaults_and_fields() -> None:
    cfg=StorageNodeService._build_config_from(_src(),"p")
    assert cfg.protocol is StorageProtocol.S3 and cfg.port == 443 and cfg.password == "p"
    local=StorageNodeService._build_config_from(_src(protocol="local",port=0,advanced_config={"x":1}),"")
    assert local.port == 0 and local.advanced_config == {"x":1}
    ftp=StorageNodeService._build_config_from(_src(protocol="ftp",port=None),"")
    assert ftp.port == 21


async def test_clear_other_default(monkeypatch: pytest.MonkeyPatch) -> None:
    calls=[]
    class DB:
        async def execute(self, stmt): calls.append(stmt)
    s=StorageNodeService.__new__(StorageNodeService); s.db=DB(); s.auth=object()
    await s._clear_other_default()
    await s._clear_other_default(1)
    assert len(calls)==2


def test_build_config_other_ports() -> None:
    assert StorageNodeService._build_config_from(_src(protocol="sftp",port=None),"p").port == 22
    assert StorageNodeService._build_config_from(_src(protocol="ftps",port=None),"p").port == 990


async def test_export_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        async def get_list(self): return []
    s=StorageNodeService.__new__(StorageNodeService); s.auth=object(); s.db=object()
    s._crud=lambda: C()
    out = await s.export_config(); assert out["nodes"] == [] and out["version"] == 1


async def test_node_queries(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.task.storage.node.schema import StorageNodeOutSchema
    from app.core.base_schema import PageResultSchema
    node=StorageNodeOutSchema(name="n",protocol="s3",port=443,bucket="b",username="u",password="x",endpoint="https://e")
    class C:
        async def get_or_404(self,**kw): return node
        async def page(self,**kw): return PageResultSchema(page_no=1,page_size=10,total=1,has_next=False,items=[node])
        async def get_list(self,**kw): return [node]
    s=StorageNodeService.__new__(StorageNodeService); s.auth=object(); s.db=object()
    s._crud=lambda: C()
    assert (await s.detail(1)).name=="n"
    assert (await s.page(None,1,10)).total==1
    assert len(await s.get_list())==1


def _node():
    from app.modules.task.storage.node.schema import StorageNodeOutSchema
    return StorageNodeOutSchema(id=1,name="n",protocol="s3",port=443,bucket="b",username="u",password="x",endpoint="https://e")


async def test_node_create_update_delete(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.task.storage.node.schema import StorageNodeCreateSchema, StorageNodeUpdateSchema
    import app.modules.task.storage.node.service as mod
    node=_node()
    class C:
        def __init__(self,*a): self.deleted=None
        async def get(self,**kw): return None
        async def create(self,**kw): return node
        async def get_or_404(self,**kw): return node
        async def update(self,**kw): return None
        async def delete(self,ids): self.deleted=ids
    c=C()
    class DB:
        async def execute(self,stmt): return None
    s=StorageNodeService.__new__(StorageNodeService); s.auth=object(); s.db=DB()
    s._crud=lambda: c
    monkeypatch.setattr(mod,"encrypt_password",lambda p:"enc")
    data=StorageNodeCreateSchema(name="n",protocol="s3",port=443,bucket="b",username="u",password="p",endpoint="https://e",is_default=True)
    assert (await s.create(data)).name=="n"
    with pytest.raises(CustomException, match="不能为空"):
        await s.delete([])
    await s.delete([1]); assert c.deleted==[1]
