"""用户服务导入/导出/模板分支。"""

from __future__ import annotations

from io import BytesIO

import pytest
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
