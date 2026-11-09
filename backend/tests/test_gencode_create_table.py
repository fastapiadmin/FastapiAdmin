"""代码生成建表 SQL 白名单校验。"""

from __future__ import annotations

import pytest

from app.core.exceptions import CustomException
from app.modules.generator.gencode import service as mod
from app.modules.generator.gencode.service import GenTableService


def _svc():
    s = GenTableService.__new__(GenTableService); s.auth = object(); s.db = object(); return s


async def test_create_table_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    s = _svc()
    with pytest.raises(CustomException, match="不能为空"):
        await s.create_table("")
    with pytest.raises(CustomException, match="缺少 CREATE"):
        await s.create_table("SELECT 1")
    with pytest.raises(CustomException, match="禁止"):
        await s.create_table("DROP TABLE x; CREATE TABLE y (id INT);")


async def test_create_table_exists_and_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self,*a): self.exists=False
        async def check_table_exists(self,name): return self.exists
        async def get_gen_table_by_name(self,name): return None
        async def execute_sql(self,sql): return True
    c=C()
    monkeypatch.setattr(mod,"GenTableCRUD",lambda *a: c)
    s=_svc()
    async def imported(tables): return True
    s.import_gen_table=imported
    async def by_names(names): return []
    s.get_gen_db_table_list_by_name=by_names
    assert await s.create_table("CREATE TABLE demo (id INT);") is True
    c.exists=True
    with pytest.raises(CustomException, match="已存在"):
        await s.create_table("CREATE TABLE demo (id INT);")


async def test_create_table_alter_and_execute_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self,*a): pass
        async def check_table_exists(self,name): return False
        async def get_gen_table_by_name(self,name): return None
        async def execute_sql(self,sql): return False
    monkeypatch.setattr(mod,"GenTableCRUD",lambda *a: C())
    s=_svc()
    with pytest.raises(CustomException, match="执行SQL"):
        await s.create_table("CREATE TABLE demo (id INT);")
    with pytest.raises(CustomException):
        await s.create_table("CREATE TABLE demo (id INT); ALTER TABLE demo DROP COLUMN id;")


async def test_create_table_imports(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self,*a): pass
        async def check_table_exists(self,name): return False
        async def get_gen_table_by_name(self,name): return None
        async def execute_sql(self,sql): return True
    monkeypatch.setattr(mod,"GenTableCRUD",lambda *a:C())
    s=_svc(); called=[]
    async def by_names(names):
        called.append(names); return ["cfg"]
    async def imported(tables): called.append(tables)
    s.get_gen_db_table_list_by_name=by_names; s.import_gen_table=imported
    assert await s.create_table("CREATE TABLE demo (id INT);") is True
    assert called == [["demo"], ["cfg"]]


async def test_create_table_alter_fk_allowed(monkeypatch: pytest.MonkeyPatch) -> None:
    sqls=[]
    class C:
        def __init__(self,*a): pass
        async def check_table_exists(self,name): return False
        async def get_gen_table_by_name(self,name): return None
        async def execute_sql(self,sql): sqls.append(sql); return True
    monkeypatch.setattr(mod,"GenTableCRUD",lambda *a:C())
    s=_svc(); s.get_gen_db_table_list_by_name=lambda names: _empty()
    async def imported(t): return None
    s.import_gen_table=imported
    assert await s.create_table("CREATE TABLE demo (id INT); ALTER TABLE demo ADD CONSTRAINT fk FOREIGN KEY (id) REFERENCES x(id);") is True
    assert len(sqls)>=2


async def _empty(): return []


async def test_create_table_comment_only() -> None:
    s=_svc()
    with pytest.raises(CustomException, match="缺少 CREATE"):
        await s.create_table("COMMENT ON TABLE x IS 'x';")


async def test_create_table_parse_error() -> None:
    s=_svc()
    with pytest.raises(Exception):
        await s.create_table("this is not sql")
