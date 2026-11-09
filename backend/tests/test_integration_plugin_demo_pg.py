"""示例插件 HTTP 接口集成（若插件路由已注册）。"""

from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 PostgreSQL：设置 RUN_INTEGRATION=1 且 TEST_DB_TYPE=postgres",
)


def _base(test_client) -> str:
    paths = test_client.get("/openapi.json").json()["paths"]
    candidates = sorted(p for p in paths if "demo" in p and "template" not in p and "export" not in p and "import" not in p)
    if not candidates:
        pytest.skip("示例插件未注册路由")
    for p in candidates:
        if p.endswith("/list"):
            return p[: -len("/list")]
    return candidates[0].rsplit("/", 1)[0]


def test_demo_crud_api(test_client, auth_headers) -> None:
    base = _base(test_client)
    payload = {"name": "it_demo", "status": 0, "description": "it"}
    created = test_client.post(f"{base}/create", json=payload, headers=auth_headers)
    assert created.status_code in (200, 201), created.text
    oid = created.json()["data"]["id"]
    try:
        assert test_client.get(f"{base}/detail/{oid}", headers=auth_headers).status_code == 200
        listing = test_client.get(f"{base}/list", params={"page_no": 1, "page_size": 10}, headers=auth_headers)
        assert listing.status_code == 200 and listing.json()["data"]["total"] >= 1
        updated = test_client.put(f"{base}/update/{oid}", json={**payload, "name": "it_demo2"}, headers=auth_headers)
        assert updated.status_code == 200
        batch = test_client.patch(f"{base}/status/batch", json={"ids": [oid], "status": 1}, headers=auth_headers)
        assert batch.status_code == 200
    finally:
        assert test_client.request("DELETE", f"{base}/delete", json=[oid], headers=auth_headers).status_code == 200


def test_demo_template_and_missing(test_client, auth_headers) -> None:
    base = _base(test_client)
    template = test_client.post(f"{base}/download/template", headers=auth_headers)
    assert template.status_code == 200 and template.content
    assert test_client.get(f"{base}/detail/99999999", headers=auth_headers).status_code in (400, 404)


def test_demo_import_export(test_client, auth_headers) -> None:
    base = _base(test_client)
    export = test_client.post(f"{base}/export", json={"page_no": 1, "page_size": 10}, headers=auth_headers)
    assert export.status_code == 200 and export.content


def test_demo_import(test_client, auth_headers) -> None:
    from io import BytesIO
    from openpyxl import Workbook
    base = _base(test_client)
    wb = Workbook(); ws = wb.active
    ws.append(["名称", "状态", "描述"])
    ws.append(["it_import_demo", "正常", "imported"])
    buf = BytesIO(); wb.save(buf); buf.seek(0)
    resp = test_client.post(f"{base}/import", files={"file": ("demo.xlsx", buf.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}, headers=auth_headers)
    assert resp.status_code == 200, resp.text
    assert "成功导入 1" in resp.json()["data"]
    listing = test_client.get(f"{base}/list", params={"page_no": 1, "page_size": 10, "name": "it_import_demo"}, headers=auth_headers)
    items = listing.json()["data"]["items"]
    assert items
    ids = [x["id"] for x in items if x["name"] == "it_import_demo"]
    if ids:
        test_client.request("DELETE", f"{base}/delete", json=ids, headers=auth_headers)


def _xlsx(rows, headers) -> bytes:
    from io import BytesIO
    from openpyxl import Workbook
    wb = Workbook(); ws = wb.active; ws.append(headers)
    for r in rows: ws.append(r)
    buf = BytesIO(); wb.save(buf); return buf.getvalue()


def test_demo_import_errors(test_client, auth_headers) -> None:
    base = _base(test_client)
    empty = test_client.post(f"{base}/import", files={"file": ("e.xlsx", _xlsx([], ["名称", "状态", "描述"]), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}, headers=auth_headers)
    assert empty.status_code == 400
    missing = test_client.post(f"{base}/import", files={"file": ("m.xlsx", _xlsx([["x"]], ["名称"]), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}, headers=auth_headers)
    assert missing.status_code == 400
    bad = test_client.post(f"{base}/import", files={"file": ("b.xlsx", _xlsx([["it_bad", "未知", "d"]], ["名称", "状态", "描述"]), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}, headers=auth_headers)
    assert bad.status_code == 200 and "状态必须" in bad.json()["data"]


def test_demo_service_errors(test_client, auth_headers) -> None:
    from app.core.exceptions import CustomException
    from app.modules.task.storage.node.service import StorageNodeService  # noqa: F401
    from app.plugin.module_example.demo.schema import DemoCreateSchema, DemoUpdateSchema
    from app.plugin.module_example.demo.service import DemoService
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlalchemy.pool import NullPool
    from app.config.setting import settings
    auth = __import__("types").SimpleNamespace(user=__import__("types").SimpleNamespace(id=0))
    async def run():
        e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
        f = async_sessionmaker(e, expire_on_commit=False)
        try:
            async with f() as db:
                svc = DemoService(auth, db)
                with pytest.raises(CustomException):
                    await svc.detail(99999999)
                with pytest.raises(CustomException):
                    await svc.update(99999999, DemoUpdateSchema(name="xx"))
                with pytest.raises(CustomException):
                    await svc.delete([])
                with pytest.raises(CustomException):
                    await svc.delete([99999999])
                assert await svc.get_list() is not None
        finally:
            await e.dispose()
    asyncio.run(run())


def test_demo_service_export_import_errors(test_client) -> None:
    from io import BytesIO
    from fastapi import UploadFile
    from app.core.exceptions import CustomException
    from app.plugin.module_example.demo.service import DemoService
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlalchemy.pool import NullPool
    from app.config.setting import settings
    auth = __import__("types").SimpleNamespace(user=__import__("types").SimpleNamespace(id=0))
    async def run():
        e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
        f = async_sessionmaker(e, expire_on_commit=False)
        try:
            async with f() as db:
                svc = DemoService(auth, db)
                out = await svc.batch_export([{"id": 1, "name": "n", "status": 0, "created_id": {"name": "u"}}, {"id": 2, "name": "n2", "status": 1}])
                assert out
                with pytest.raises(Exception):
                    await svc.batch_import(UploadFile(filename="e.xlsx", file=BytesIO(b"not-excel")))
        finally:
            await e.dispose()
    asyncio.run(run())


def test_demo_service_crud_errors(test_client) -> None:
    from app.plugin.module_example.demo.schema import DemoCreateSchema, DemoUpdateSchema
    from app.plugin.module_example.demo.service import DemoService
    from app.core.exceptions import CustomException
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlalchemy.pool import NullPool
    from app.config.setting import settings
    name = "it_dup_demo"
    auth = __import__("types").SimpleNamespace(user=__import__("types").SimpleNamespace(id=0))
    async def run():
        e = create_async_engine(settings.ASYNC_DB_URI, poolclass=NullPool)
        f = async_sessionmaker(e, expire_on_commit=False)
        try:
            async with f() as db:
                svc = DemoService(auth, db)
                obj = await svc.create(DemoCreateSchema(name=name))
                await db.commit()
                with pytest.raises(CustomException):
                    await svc.create(DemoCreateSchema(name=name))
                with pytest.raises(CustomException):
                    await svc.update(99999999, DemoUpdateSchema(name="xx"))
                with pytest.raises(CustomException):
                    await svc.delete([99999999])
                await svc.delete([obj.id])
                await db.commit()
        finally:
            await e.dispose()
    asyncio.run(run())
