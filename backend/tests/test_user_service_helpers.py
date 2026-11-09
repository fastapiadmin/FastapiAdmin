"""用户服务导入/导出/模板分支。"""

from __future__ import annotations

from io import BytesIO

import pytest
from types import SimpleNamespace
from openpyxl import load_workbook
from starlette.datastructures import UploadFile

from app.core.exceptions import CustomException
from app.modules.system.user.service import UserService


def test_import_gender() -> None:
    assert UserService._import_gender("男") == "0"
    assert UserService._import_gender("女") == "1"
    assert UserService._import_gender("未知") == "2"
    assert UserService._import_gender("0") == "0"
    assert UserService._import_gender(None) == "1"


def test_import_template_and_export() -> None:
    tpl = UserService.get_import_template()
    assert len(tpl) > 100
    wb = load_workbook(BytesIO(tpl))
    assert wb.active is not None

    async def _export():
        return await UserService.export_list([{"id": 1, "username": "u", "status": 0, "gender": "1", "is_superuser": False, "created_by": {"name": "admin"}}])
    import asyncio
    data = asyncio.run(_export())
    assert len(data) > 100


class FakeFile:
    def __init__(self, data: bytes): self.data = data; self.closed = False
    async def read(self): return self.data
    async def close(self): self.closed = True


async def test_batch_import_rejects_empty_and_invalid() -> None:
    svc = UserService.__new__(UserService)
    from openpyxl import Workbook
    wb = Workbook(); wb.active.append(["账号"]); b = BytesIO(); wb.save(b)
    with pytest.raises(CustomException, match="导入文件为空"):
        await svc.batch_import(FakeFile(b.getvalue()))
    with pytest.raises(CustomException, match="格式错误"):
        await svc.batch_import(FakeFile(b"not excel"))


async def test_batch_import_missing_headers() -> None:
    from openpyxl import Workbook
    wb = Workbook(); ws = wb.active; ws.append(["账号"]); ws.append(["u"])
    b = BytesIO(); wb.save(b)
    svc = UserService.__new__(UserService)
    with pytest.raises(CustomException, match="缺少必要的列"):
        await svc.batch_import(FakeFile(b.getvalue()))


async def test_process_import_row_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    row={"username":"user1","name":"N","dept_id":1,"email":"a@b.com","mobile":"13800000000","gender":"男","status":"正常"}
    class D:
        def __init__(self,*a): pass
        async def get(self,**kw): return object()
    class U:
        def __init__(self,*a): self.updated=False; self.created=False
        async def get(self,**kw): return SimpleNamespace(id=1,is_superuser=False)
        async def update(self,**kw): self.updated=True
        async def create(self,**kw): self.created=True; return SimpleNamespace(id=2)
    class P:
        @staticmethod
        async def ahash_password(**kw): return "Hashed123!x"
    monkeypatch.setattr(mod,"DeptCRUD",D); monkeypatch.setattr(mod,"UserCRUD",U); monkeypatch.setattr(mod,"PwdUtil",P)
    s=UserService.__new__(UserService); s.auth=object(); s.db=object()
    async def noop(*a,**k): return None
    s._set_user_roles=noop; s._set_user_positions=noop
    assert (await s._process_import_row(1,{**row,"username":""},False))[1].startswith("第1行")
    assert (await s._process_import_row(1,{**row,"name":""},False))[1].startswith("第1行")
    class DNone(D):
        async def get(self,**kw): return None
    monkeypatch.setattr(mod,"DeptCRUD",DNone)
    assert "不存在" in (await s._process_import_row(1,row,False))[1]
    monkeypatch.setattr(mod,"DeptCRUD",D)
    assert (await s._process_import_row(1,row,True))[0]==1
    assert (await s._process_import_row(1,row,False))[0]==0
    class UNew(U):
        async def get(self,**kw): return None
    monkeypatch.setattr(mod,"UserCRUD",UNew)
    assert (await s._process_import_row(1,row,False))[0]==1


async def test_process_import_row_superuser(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    row={"username":"user1","name":"N","dept_id":1,"email":None,"mobile":None,"gender":"未知","status":"停用"}
    class D:
        def __init__(self,*a): pass
        async def get(self,**kw): return object()
    class U:
        def __init__(self,*a): pass
        async def get(self,**kw): return SimpleNamespace(id=1,is_superuser=True)
    class P:
        @staticmethod
        async def ahash_password(**kw): return "Hashed123!x"
    monkeypatch.setattr(mod,"DeptCRUD",D); monkeypatch.setattr(mod,"UserCRUD",U); monkeypatch.setattr(mod,"PwdUtil",P)
    s=UserService.__new__(UserService); s.auth=object(); s.db=object()
    out=await s._process_import_row(2,row,True)
    assert out[0]==0 and "超级管理员" in out[1]


async def test_batch_import_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    class F:
        async def read(self): return b"x"
        async def close(self): return None
    class X:
        rows=[]
        @staticmethod
        async def aread_excel_to_dicts(contents): return X.rows
    monkeypatch.setattr(mod,"ExcelUtil",X)
    s=UserService.__new__(UserService); s.auth=object(); s.db=object()
    with pytest.raises(CustomException, match="为空"):
        await s.batch_import(F())
    X.rows=[{"账号":"user1"}]
    with pytest.raises(CustomException, match="缺少必要的列"):
        await s.batch_import(F())
    X.rows=[{"部门编号":1,"账号":"user1","昵称":"N","邮箱":None,"手机号":None,"性别":"男","状态":"正常"}]
    assert "成功导入" in await s.batch_import(F())
    async def row(i,r,u): return (1,None) if i==2 else (0,"err")
    s._process_import_row=row
    X.rows=[{"部门编号":1,"账号":"user1","昵称":"N","邮箱":None,"手机号":None,"性别":"男","状态":"正常"}]*2
    out=await s.batch_import(F())
    assert "成功导入 1" in out and "err" in out


async def test_export_list(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.user.service as mod
    class X:
        @staticmethod
        def export_to_excel(data, headers): return b"x"
    monkeypatch.setattr(mod,"ExcelUtil",X)
    with pytest.raises(CustomException, match="没有数据"):
        await UserService.export_list([])
    assert await UserService.export_list([{"username":"u"}])==b"x"
